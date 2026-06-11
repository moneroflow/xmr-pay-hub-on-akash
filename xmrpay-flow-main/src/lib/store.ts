import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { invoke } from '@tauri-apps/api/core';

interface AppState {
  seed: string | null;
  walletExists: boolean | null;
  zkStatus: 'idle' | 'generating' | 'verified' | 'error';
  setSeed: (seed: string | null) => void;
  checkWallet: () => Promise<void>;
  saveSeed: (seed: string, passphrase: string) => Promise<void>;
  loadSeed: (passphrase: string) => Promise<string | null>;
  setZkStatus: (status: AppState['zkStatus']) => void;
}

export const useStore = create<AppState>()(
  persist(
    (set, get) => ({
      seed: null,
      walletExists: null,
      zkStatus: 'idle',

      setSeed: (seed) => set({ seed }),

      checkWallet: async () => {
        try {
          const exists = await invoke<boolean>('check_wallet_exists');
          set({ walletExists: exists });
        } catch (e) {
          console.error("Tauri bridge error checkWallet:", e);
          set({ walletExists: false });
        }
      },

      saveSeed: async (seed, passphrase) => {
        try {
          await invoke('save_wallet_seed', { seed, passphrase });
          set({ seed, walletExists: true });
        } catch (e) {
          console.error("Tauri bridge error saveSeed:", e);
          throw e;
        }
      },

      loadSeed: async (passphrase) => {
        try {
          const seed = await invoke<string>('load_wallet_seed', { passphrase });
          set({ seed });
          return seed;
        } catch (e) {
          console.error("Tauri bridge error loadSeed:", e);
          throw e;
        }
      },

      setZkStatus: (status) => set({ zkStatus: status }),
    }),
    {
      name: 'moneroflow-state',
    }
  )
);
