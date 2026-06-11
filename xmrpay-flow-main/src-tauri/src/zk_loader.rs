
use serde::{Serialize, Deserialize};
use std::fs;
use std::path::PathBuf;
use std::io::{Read};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ZkCircuit {
    pub id: String,
    pub version: String,
    pub public_input_count: u32,
    pub witness_count: u32,
    pub bytecode: Vec<u8>,
}

pub struct ZkLoader {
    plugins_dir: PathBuf,
}

impl ZkLoader {
    pub fn new(plugins_dir: PathBuf) -> Self {
        Self { plugins_dir }
    }

    pub fn list_plugins(&self) -> Result<Vec<String>, String> {
        let paths = fs::read_dir(&self.plugins_dir)
            .map_err(|e| format!("Failed to read plugins dir: {}", e))?;
        
        let mut plugins = Vec::new();
        for entry in paths {
            if let Ok(entry) = entry {
                let path = entry.path();
                if path.extension().and_then(|s| s.to_str()) == Some("zk") {
                    if let Some(name) = path.file_stem().and_then(|s| s.to_str()) {
                        plugins.push(name.to_string());
                    }
                }
            }
        }
        Ok(plugins)
    }

    pub fn load_circuit(&self, plugin_id: &str) -> Result<ZkCircuit, String> {
        let path = self.plugins_dir.join(format!("{}.zk", plugin_id));
        let bytes = fs::read(path).map_err(|e| format!("Failed to read .zk file: {}", e))?;
        
        let decoded: ZkCircuit = bincode::deserialize(&bytes)
            .map_err(|e| format!("Bincode deserialization failed: {}", e))?;
            
        Ok(decoded)
    }
}
