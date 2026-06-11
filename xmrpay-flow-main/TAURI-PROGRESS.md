# Tauri Build Progress & Compatibility

## Build Strategy: GLIBC Compatibility
To prevent `GLIBC_X.XX not found` errors on client machines (e.g., when building on Ubuntu 24.04 but deploying to Ubuntu 22.04), we follow the **"Oldest Supported Target"** rule.

### The Rule
**Always build binaries on the oldest OS version that the application is intended to support.** 
Since GLIBC is backward-compatible, a binary built on an older OS will run on all newer versions, but not vice-versa.

### Current Workflow
- **Build Environment:** Docker container running `ubuntu:22.04`.
- **Reasoning:** Ensures compatibility across Ubuntu 22.04 (Jammy) and 24.04 (Noble).
- **Tooling:** 
  - Node.js v20 (via NodeSource)
  - Rust (via rustup)
  - Tauri CLI (`npx tauri build`)

### Deployment Path
- **Build Path:** `/home/node/.openclaw/workspace/xmr-pay-hub-on-akash/xmrpay-flow-main/src-tauri/target/release/bundle/deb`
- **Verification:** Run binary on `yogi` (Ubuntu 22.04) to confirm GLIBC resolution.
