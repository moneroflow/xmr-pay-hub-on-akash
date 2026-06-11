
use std::process::{Command, Child};
use std::sync::{Arc, RwLock};
use serde::{Serialize, Deserialize};
use std::io;

#[derive(Serialize, Deserialize, Debug, Clone, Copy)]
pub enum NodeStatus {
    Offline,
    Starting,
    Online,
    Error,
}

pub struct NodeManager {
    binary_path: String,
    process: Arc<RwLock<Option<Child>>>,
    status: Arc<RwLock<NodeStatus>>,
}

impl NodeManager {
    pub fn new(binary_path: String) -> Self {
        Self {
            binary_path,
            process: Arc::new(RwLock::new(None)),
            status: Arc::new(RwLock::new(NodeStatus::Offline)),
        }
    }

    pub fn start_node(&self, route: &str) -> Result<String, String> {
        let mut status = self.status.write().unwrap();
        *status = NodeStatus::Starting;

        let child = Command::new(&self.binary_path)
            .arg("--route")
            .arg(route)
            .spawn()
            .map_err(|e| format!("Failed to spawn node: {}", e))?;

        *self.process.write().unwrap() = Some(child);
        
        std::thread::sleep(std::time::Duration::from_secs(1));
        *status = NodeStatus::Online;

        Ok("Node started successfully".to_string())
    }

    pub fn stop_node(&self) -> Result<String, String> {
        if let Some(mut child) = self.process.write().unwrap().take() {
            let _ = child.kill();
            let mut status = self.status.write().unwrap();
            *status = NodeStatus::Offline;
            Ok("Node stopped".to_string())
        } else {
            Err("No node running".to_string())
        }
    }

    pub fn get_status(&self) -> NodeStatus {
        *self.status.read().unwrap()
    }
}
