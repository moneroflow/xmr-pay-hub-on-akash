import { invoke } from '@tauri-apps/api/core';

export interface ZkProofRequest {
  proof_type: string;
  params: any;
  secret_ref?: string;
}

export interface ZkProofResponse {
  proof: string;
  public_inputs: string[];
  verified: boolean;
}

/**
 * ZK-Bridge handles the communication between the React UI 
 * and the native Rust ZK-Hybrid Framework.
 */
export const zkBridge = {
  async generateProof(request: ZkProofRequest): Promise<ZkProofResponse> {
    try {
      return await invoke<ZkProofResponse>('generate_zk_proof', { request });
    } catch (e) {
      console.error('ZK-Bridge Error [generate_zk_proof]:', e);
      throw e;
    }
  },

  async verifyProof(proof: string, inputs: string[]): Promise<boolean> {
    try {
      return await invoke<boolean>('verify_zk_proof', { proof, inputs });
    } catch (e) {
      console.error('ZK-Bridge Error [verify_zk_proof]:', e);
      throw e;
    }
  }
};
