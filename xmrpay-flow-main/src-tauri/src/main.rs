#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::fs;
use serde::{Serialize, Deserialize};
use tauri::Manager;
use aes_gcm::{Aes256Gcm, Key, Nonce, KeyInit};
use aes_gcm::aead::{Aead, AeadCore};
use argon2::{Argon2, PasswordHash, PasswordHasher, PasswordVerifier};
use rand::{RngCore, rngs::OsRng};
use base64::{engine::general_purpose, Engine as _};
use std::sync::{Arc, Mutex};

mod zk_provider;
mod plugin_manager;
mod zk_loader;
mod node_manager;
use zk_provider::{ZkProvider, BulletproofsProvider, MockZkProvider};
use plugin_manager::PluginManager;
use node_manager::{NodeManager, NodeStatus};

#[derive(Serialize, Deserialize, Debug)]
pub struct ZkProofRequest {
    pub proof_type: String,
    pub params: serde_json::Value,
    pub secret_ref: Option<String>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct ZkProofResponse {
    pub proof: String,
    pub public_inputs: Vec<String>,
    pub verified: bool,
}

#[tauri::command]
fn list_zk_plugins(state: tauri::State<'_, PluginManager>) -> Result<Vec<String>, String> {
    state.list_available_plugins()
}

#[tauri::command]
fn load_zk_plugin(state: tauri::State<'_, PluginManager>, plugin_id: String) -> Result<crate::zk_loader::ZkCircuit, String> {
    state.load_plugin(&plugin_id)
}

#[tauri::command]
fn start_sovereign_node(state: tauri::State<'_, NodeManager>, route: String) -> Result<String, String> {
    state.start_node(&route)
}

#[tauri::command]
fn stop_sovereign_node(state: tauri::State<'_, NodeManager>) -> Result<String, String> {
    state.stop_node()
}

#[tauri::command]
fn get_node_status(state: tauri::State<'_, NodeManager>) -> NodeStatus {
    state.get_status()
}

#[tauri::command]
fn toggle_darkfi(state: tauri::State<'_, PluginManager>, enabled: bool) -> Result<bool, String> {
    state.set_enabled(enabled);
    Ok(enabled)
}

#[tauri::command]
fn generate_zk_proof(state: tauri::State<'_, PluginManager>, request: ZkProofRequest) -> Result<ZkProofResponse, String> {
    if !state.is_enabled() {
        return Err("DarkFi is currently disabled in settings.".to_string());
    }
    let provider: Box<dyn ZkProvider> = if request.proof_type == "mock" {
        Box::new(MockZkProvider)
    } else {
        Box::new(BulletproofsProvider)
    };
    provider.generate_proof(request)
}

#[tauri::command]
fn verify_zk_proof(state: tauri::State<'_, PluginManager>, proof: String, inputs: Vec<String>) -> Result<bool, String> {
    if !state.is_enabled() {
        return Err("DarkFi is currently disabled in settings.".to_string());
    }
    let provider: Box<dyn ZkProvider> = Box::new(BulletproofsProvider);
    provider.verify_proof(&proof, &inputs)
}

fn derive_key(passphrase: &str, salt: &[u8]) -> Result<Vec<u8>, String> {
    let mut config = Argon2::default();
    let mut output_key = [0u8; 32];
    config.hash_password_into(passphrase.as_bytes(), salt, &mut output_key)
        .map_err(|e| format!("KDF Error: {}", e))?;
    Ok(output_key.to_vec())
}

fn encrypt_data(data: &str, passphrase: &str) -> Result<String, String> {
    let mut salt = [0u8; 16];
    let mut nonce_bytes = [0u8; 12];
    OsRng.fill_bytes(&mut salt);
    OsRng.fill_bytes(&mut nonce_bytes);
    let key_bytes = derive_key(passphrase, &salt)?;
    let key = Key::<Aes256Gcm>::from_slice(&key_bytes);
    let cipher = Aes256Gcm::new(key);
    let nonce = Nonce::from_slice(&nonce_bytes);
    let ciphertext = cipher.encrypt(nonce, data.as_bytes())
        .map_err(|e| format!("Encryption Error: {}", e))?;
    let mut final_blob = Vec::new();
    final_blob.extend_from_slice(&salt);
    final_blob.extend_from_slice(&nonce_bytes);
    final_blob.extend_from_slice(&ciphertext);
    Ok(general_purpose::STANDARD.encode(final_blob))
}

fn decrypt_data(encrypted_blob: &str, passphrase: &str) -> Result<String, String> {
    let data = general_purpose::STANDARD.decode(encrypted_blob)
        .map_err(|e| format!("Base64 Error: {}", e))?;
    if data.len() < 28 {
        return Err("Invalid encrypted blob".to_string());
    }
    let salt = &data[0..16];
    let nonce_bytes = &data[16..28];
    let ciphertext = &data[28..];
    let key_bytes = derive_key(passphrase, salt)?;
    let key = Key::<Aes256Gcm>::from_slice(&key_bytes);
    let cipher = Aes256Gcm::new(key);
    let nonce = Nonce::from_slice(nonce_bytes);
    let plaintext = cipher.decrypt(nonce, ciphertext)
        .map_err(|e| format!("Decryption Error: {}", e))?;
    String::from_utf8(plaintext).map_err(|e| format!("UTF-8 Error: {}", e))
}

#[tauri::command]
fn encrypt_seed(seed: String, passphrase: String) -> Result<String, String> {
    encrypt_data(&seed, &passphrase)
}

#[tauri::command]
fn decrypt_seed(encrypted_seed: String, passphrase: String) -> Result<String, String> {
    decrypt_data(&encrypted_seed, &passphrase)
}

fn main() {
    tauri::Builder::default()
        .manage(PluginManager::new(std::path::PathBuf::from("/home/node/.openclaw/workspace/darkfi_plugins")))
        .manage(NodeManager::new("/usr/local/bin/darkfid".to_string()))
        .invoke_handler(tauri::generate_handler![
            encrypt_seed,
            decrypt_seed,
            generate_zk_proof,
            verify_zk_proof,
            toggle_darkfi,
            list_zk_plugins,
            load_zk_plugin,
            start_sovereign_node,
            stop_sovereign_node,
            get_node_status,
        ])
        .run(tauri::generate_context!())
        .expect("Error while running Tauri application");
}
