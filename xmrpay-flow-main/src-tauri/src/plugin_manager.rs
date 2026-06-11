
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use serde::{Serialize, Deserialize};
use crate::zk_provider::{ZkProvider, BulletproofsProvider, MockZkProvider};
use crate::zk_loader::{ZkLoader, ZkCircuit};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct PluginMetadata {
    pub name: String,
    pub version: String,
    pub params: Vec<String>,
    pub circuit_id: String,
}

pub struct PluginManager {
    pub darkfi_enabled: Arc<RwLock<bool>>,
    pub loader: ZkLoader,
    pub plugins: Arc<RwLock<HashMap<String, Box<dyn ZkProvider + Send + Sync>>>>,
}

impl PluginManager {
    pub fn new(app_data_dir: std::path::PathBuf) -> Self {
        let mut plugins: HashMap<String, Box<dyn ZkProvider + Send + Sync>> = HashMap::new();
        plugins.insert("proof_of_balance".to_string(), Box::new(BulletproofsProvider));
        plugins.insert("mock_provider".to_string(), Box::new(MockZkProvider));
        Self {
            darkfi_enabled: Arc::new(RwLock::new(false)),
            loader: ZkLoader::new(app_data_dir),
            plugins: Arc::new(RwLock::new(plugins)),
        }
    }

    pub fn set_enabled(&self, enabled: bool) {
        if let Ok(mut lock) = self.darkfi_enabled.write() {
            *lock = enabled;
        }
    }

    pub fn is_enabled(&self) -> bool {
        *self.darkfi_enabled.read().unwrap()
    }

    pub fn load_plugin(&self, plugin_id: &str) -> Result<ZkCircuit, String> {
        self.loader.load_circuit(plugin_id)
    }

    pub fn list_available_plugins(&self) -> Result<Vec<String>, String> {
        self.loader.list_plugins()
    }
}
