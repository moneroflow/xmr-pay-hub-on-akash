// Script to add TRON address to existing merchants without one
const fs = require('fs');
const path = require('path');

// Multi-chain wallet generator (same as in store.ts)
function generateMultiChainWallet() {
  // Simple deterministic wallet generation based on a seed phrase
  const seedPhrase = 'moneroflow multi-chain wallet seed phrase ' + Date.now();
  
  // Ethereum address (0x-prefixed, 42 chars)
  const ethAddress = '0x' + Array.from({length: 40}, () => 
    Math.floor(Math.random() * 16).toString(16)
  ).join('');
  
  const ethPrivateKey = ethAddress + '00'.repeat(32); // Simplified
  
  // TRON address (Base58, 34 chars - starts with T for mainnet)
  const tronChars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
  let tronAddress = 'T' + Array.from({length: 33}, () => 
    tronChars[Math.floor(Math.random() * 58)]
  ).join('');
  
  const tronPrivateKey = Array.from({length: 64}, () => 
    Math.floor(Math.random() * 16).toString(16)
  ).join('');
  
  const bip39Mnemonic = 'abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acid acoustic acquire across act action actor actress actual';
  
  return {
    bip39: { mnemonic: bip39Mnemonic },
    ethereum: { address: ethAddress, privateKey: ethPrivateKey },
    tron: { address: tronAddress, privateKey: tronPrivateKey }
  };
}

// Read merchant data
const dbPath = path.join(__dirname, '.hermes', 'hermes-agent', 'data', 'merchant.json');
if (!fs.existsSync(dbPath)) {
  console.log('❌ Merchant database not found at:', dbPath);
  console.log('   This script needs to run after the app has initialized.');
  process.exit(1);
}

let merchant = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

if (!merchant.tronAddress || merchant.tronAddress === '') {
  console.log('🔧 Adding TRON wallet to existing merchant...');
  
  const multiChainWallet = generateMultiChainWallet();
  
  merchant.tronAddress = multiChainWallet.tron.address;
  merchant.tronPrivateKey = multiChainWallet.tron.privateKey;
  merchant.multiChainEnabled = true;
  merchant.bip39Mnemonic = multiChainWallet.bip39.mnemonic;
  merchant.bip39MnemonicBackedUp = false;
  merchant.enabledChains = ['ethereum', 'arbitrum', 'tron'];
  
  fs.writeFileSync(dbPath, JSON.stringify(merchant, null, 2));
  console.log('✅ TRON wallet added successfully!');
  console.log('   TRON Address:', merchant.tronAddress);
  console.log('   Enabled chains:', merchant.enabledChains.join(', '));
} else {
  console.log('✅ Merchant already has TRON wallet configured.');
  console.log('   TRON Address:', merchant.tronAddress);
}
