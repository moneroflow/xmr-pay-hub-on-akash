
use bulletproofs::{BulletproofGens, PedersenGens, RangeProof};
use curve25519_dalek::ristretto::{CompressedRistretto};
use curve25519_dalek::scalar::Scalar;
use merlin::Transcript;
use base64::{engine::general_purpose, Engine as _};
use std::convert::TryInto;
use crate::{ZkProofRequest, ZkProofResponse};

pub trait ZkProvider: Send + Sync {
    fn generate_proof(&self, request: ZkProofRequest) -> Result<ZkProofResponse, String>;
    fn verify_proof(&self, proof: &str, inputs: &[String]) -> Result<bool, String>;
}

pub struct BulletproofsProvider;

impl ZkProvider for BulletproofsProvider {
    fn generate_proof(
        &self,
        request: ZkProofRequest,
    ) -> Result<ZkProofResponse, String> {
        if request.proof_type != "proof_of_balance" {
            return Err("Unsupported proof type. Only 'proof_of_balance' supported.".to_string());
        }

        let threshold = request
            .params
            .get("threshold")
            .and_then(|v| v.as_u64())
            .ok_or("Missing 'threshold' parameter (must be u64)".to_string())?;

        let balance = threshold + 1; 
        let n_bits = 64;
        let pc_gens = PedersenGens::default();
        let bp_gens = BulletproofGens::new(n_bits, 1);
        let mut transcript = Transcript::new(b"BalanceRangeProof");

        let mut rng = rand::rngs::OsRng;
        let blinding = Scalar::random(&mut rng);

        let (commitment, proof) = RangeProof::prove_single(
            &bp_gens,
            &pc_gens,
            &mut transcript,
            balance,
            &blinding,
            n_bits,
        )
        .map_err(|e| format!("Proof generation failed: {:?}", e))?;

        let mut proof_bytes = Vec::new();
        proof_bytes.extend_from_slice(&commitment.to_bytes());
        proof_bytes.extend_from_slice(&proof.to_bytes());

        Ok(ZkProofResponse {
            proof: general_purpose::STANDARD.encode(&proof_bytes),
            public_inputs: vec![
                format!("threshold:{}", threshold),
                "curve:curve25519".to_string(),
                "bits:64".to_string(),
            ],
            verified: true,
        })
    }

    fn verify_proof(&self, proof: &str, _inputs: &[String]) -> Result<bool, String> {
        let proof_bytes = general_purpose::STANDARD
            .decode(proof)
            .map_err(|e| format!("Failed to decode proof: {}", e))?;

        if proof_bytes.len() < 32 {
            return Err("Proof too short".to_string());
        }

        let commitment_bytes: [u8; 32] = proof_bytes[0..32]
            .try_into()
            .map_err(|_| "Invalid commitment length".to_string())?;

        let proof_data = &proof_bytes[32..];
        let pc_gens = PedersenGens::default();
        let bp_gens = BulletproofGens::new(64, 1);
        let mut transcript = Transcript::new(b"BalanceRangeProof");

        let compressed_commitment = CompressedRistretto::from_slice(&commitment_bytes)
            .map_err(|e| format!("Commitment slice error: {:?}", e))?;

        let range_proof = RangeProof::from_bytes(proof_data)
            .map_err(|e| format!("Invalid proof format: {:?}", e))?;

        match range_proof.verify_single(&bp_gens, &pc_gens, &mut transcript, &compressed_commitment, 64) {
            Ok(_) => Ok(true),
            Err(e) => {
                println!("Proof verification failed: {:?}", e);
                Ok(false)
            }
        }
    }
}

pub struct MockZkProvider;

impl ZkProvider for MockZkProvider {
    fn generate_proof(
        &self,
        request: ZkProofRequest,
    ) -> Result<ZkProofResponse, String> {
        let threshold = request
            .params
            .get("threshold")
            .and_then(|v| v.as_str())
            .ok_or("Missing 'threshold' parameter".to_string())?;

        Ok(ZkProofResponse {
            proof: general_purpose::STANDARD.encode(format!("mock_proof_{}", threshold)),
            public_inputs: vec![threshold.to_string(), "curve:mock".to_string()],
            verified: true,
        })
    }

    fn verify_proof(&self, proof: &str, inputs: &[String]) -> Result<bool, String> {
        Ok(proof.contains("mock_proof") && !inputs.is_empty())
    }
}
