# 🌌 DarkFi Integration Framework

## 🎯 Objective
Implement a modular, trustless privacy layer within the MoneroFlow native application. The DarkFi framework allows the application to generate and verify Zero-Knowledge Proofs (ZKPs) to prove financial thresholds (e.g., balance verification) without revealing sensitive wallet data or addresses.

## 🛠️ Technical Architecture

### 1. Core Design (Rust Backend)
The framework is implemented as a trait-based provider system in the Tauri backend to ensure maximum isolation and performance.

- **`ZkProvider` Trait**: The base interface for all ZK operations. Defines methods for `generate_proof` and `verify_proof`.
- **`PluginManager`**: Orchestrates the lifecycle of ZK plugins.
    - **Plugin Path**: `/home/node/.openclaw/workspace/darkfi_plugins`
    - **State Management**: Managed via Tauri's `.manage()` state, allowing global access across all IPC commands.
    - **Toggling**: Supports a global `enabled` flag to instantly disable ZK features for security or performance.

### 2. Integrated Providers
- **`BulletproofsProvider`**: The production implementation using Bulletproofs for efficient range proofs (64-bit).
- **`MockZkProvider`**: Used for testing and UI development to simulate proof generation without heavy computation.

### 3. Tauri IPC Boundary (Frontend $\leftrightarrow$ Backend)
The following commands are exposed to the React frontend for seamless integration:
- `list_zk_plugins`: Returns a list of all available ZK circuits/plugins.
- `load_zk_plugin`: Loads a specific circuit into memory.
- `generate_zk_proof`: Generates a proof based on a `ZkProofRequest` (includes proof type and params).
- `verify_zk_proof`: Validates a proof against public inputs.
- `toggle_darkfi`: Enables or disables the entire ZK subsystem.

## 🔒 Security Properties
- **Backend Isolation**: All proof generation and verification happen in native Rust. No sensitive witness data or private keys are ever passed to the JavaScript environment.
- **Symmetric Encryption**: Integration with the `Argon2id` + `AES-256-GCM` seed encryption layer ensures that the data used to generate proofs is decrypted only in memory during the proof process.
- **Transport Security**: Proofs are serialized as Base64 strings for safe transport across the Tauri IPC bridge.

## 📈 Current Status
- [x] Trait-based Provider Architecture
- [x] Bulletproofs Integration
- [x] Mock Provider for Testing
- [x] Plugin Manager & Dynamic Loading
- [x] Tauri Command Mapping
- [ ] Multi-circuit support for diverse proof types (e.g., identity proofs)
- [ ] Integration with live Monero node data for automated proof generation
