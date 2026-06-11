#!/usr/bin/env python3
"""
Consolidate seed phrase backup section in SettingsPage.tsx
Merge Monero and Multi-Chain seed backups into one unified interface
"""

import re
import sys

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Define the seeds to find and replace

# Old Browser Wallet section (after viewOnlySetupComplete check)
old_browser_wallet = '''          {walletMode === 'viewonly' && merchant.viewOnlySetupComplete && (
            <div className="p-5 rounded-xl bg-card border border-border space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-foreground">Browser Wallet</h3>
                <Badge className="bg-success/10 text-success border-success/20 text-xs">
                  <Eye className="w-3 h-3 mr-1" /> Active
                </Badge>
              </div>

              {/* Primary Address — always visible */}
              <div className="space-y-1.5">
                <label className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider">Primary Address</label>
                <div className="flex items-center gap-2">
                  <p className="font-mono text-[11px] text-foreground bg-background border border-border rounded-lg p-3 flex-1 break-all leading-relaxed">{merchant.viewOnlyAddress}</p>
                  <Button variant="outline" size="icon" className="shrink-0 border-border hover:border-primary/50 h-8 w-8" onClick={() => { navigator.clipboard.writeText(merchant.viewOnlyAddress); toast.success('Address copied'); }}>
                    <Copy className="w-3.5 h-3.5" />
                  </Button>
                </div>
              </div>

              {/* Seed Phrase Backup Section */}
              {!merchant.viewOnlySeedBackedUp && merchant.viewOnlySeedPhrase ? (
                <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/30 space-y-3">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-destructive" />
                    <p className="text-sm font-semibold text-destructive">⚠️ Back up your seed phrase NOW</p>
                  </div>
                  <p className="text-[11px] text-muted-foreground leading-relaxed">
                    Write down these 25 words in order and store them somewhere safe offline. This is the <strong>only way</strong> to recover your wallet. Once you confirm, this phrase will be hidden permanently.
                  </p>
                  {showKey ? (
                    <>
                      <div className="bg-background border border-border rounded-lg p-3">
                        <p className="font-mono text-xs text-foreground leading-relaxed break-all select-all">{merchant.viewOnlySeedPhrase}</p>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-border text-xs"
                          onClick={() => {
                            navigator.clipboard.writeText(merchant.viewOnlySeedPhrase || '');
                            toast.success('Seed phrase copied — store it safely!');
                          }}
                        >
                          <Copy className="w-3 h-3 mr-1.5" /> Copy
                        </Button>
                        <Button
                          size="sm"
                          className="bg-gradient-orange text-xs"
                          onClick={() => {
                            updateMerchant({ viewOnlySeedBackedUp: true });
                            setShowKey(false);
                            toast.success('Seed phrase marked as backed up');
                          }}
                        >
                          <Check className="w-3 h-3 mr-1.5" /> I've saved it — lock it down
                        </Button>
                      </div>
                    </>
                  ) : (
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-destructive/30 text-destructive hover:bg-destructive/10 text-xs"
                      onClick={() => setShowKey(true)}
                    >
                      <Eye className="w-3 h-3 mr-1.5" /> Reveal Seed Phrase
                    </Button>
                  )}
                </div>
              ) : (
                <div className="p-3 rounded-lg bg-muted/50 border border-border">
                  <p className="text-[11px] text-muted-foreground leading-relaxed">
                    🔐 Seed phrase backed up and secured. If you need to access it again, restore from your backup file.
                  </p>
                </div>
              )}'''

# Old Multi-Chain section (to remove)
old_multichain_wallet = '''          {/* Multi-Chain Wallet */}
          {walletMode === 'viewonly' && merchant.viewOnlySetupComplete && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-foreground">Multi-Chain Wallet</h3>
              </div>
              <MultiChainOptIn />
              
              {/* Show multi-chain addresses if enabled */}
              {merchant.multiChainEnabled && (
                <div className="space-y-2 p-4 rounded-lg bg-card border border-border">
                  {merchant.ethAddress && (
                    <div className="space-y-1">
                      <label className="text-[10px] font-medium text-muted-foreground flex items-center gap-1">
                        ETH / ARB Address
                      </label>
                      <div className="flex items-center gap-2">
                        <p className="font-mono text-[10px] text-foreground bg-background border border-border rounded p-2 flex-1 break-all">{merchant.ethAddress}</p>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="shrink-0 h-6 w-6"
                          onClick={() => {
                            navigator.clipboard.writeText(merchant.ethAddress || '');
                            toast.success('ETH/ARB address copied');
                          }}
                        >
                          <Copy className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                  )}
                  {merchant.tronAddress && (
                    <div className="space-y-1">
                      <label className="text-[10px] font-medium text-muted-foreground">
                        TRX Address
                      </label>
                      <div className="flex items-center gap-2">
                        <p className="font-mono text-[10px] text-foreground bg-background border border-border rounded p-2 flex-1 break-all">{merchant.tronAddress}</p>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="shrink-0 h-6 w-6"
                          onClick={() => {
                            navigator.clipboard.writeText(merchant.tronAddress || '');
                            toast.success('TRX address copied');
                          }}
                        >
                          <Copy className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                  )}
                  
                  {/* BIP-39 Backup Reminder */}
 {!merchant.bip39MnemonicBackedUp && merchant.bip39Mnemonic && (
                    <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/30">
                      <div className="flex items-center gap-2 mb-2">
                        <ShieldAlert className="w-3 h-3 text-destructive" />
                        <p className="text-xs font-semibold text-destructive">Back up multi-chain seed phrase</p>
                      </div>
                      <p className="text-[10px] text-muted-foreground mb-2">
                        Your 24-word BIP-39 seed phrase controls your ETH/ARB/TRX wallets. Write it down now.
                      </p>
                      <Button
                        size="sm"
                        variant="outline"
                        className="border-destructive/30 text-destructive hover:bg-destructive/10 text-xs"
                        onClick={() => requireAdmin(() => {
                          navigator.clipboard.writeText(merchant.bip39Mnemonic || '');
                          toast.success('BIP-39 seed phrase copied — store it safely!');
                        })}
                      >
                        <Copy className="w-3 h-3 mr-1" /> Copy Seed Phrase
                      </Button>
                      <Button
                        size="sm"
                        className="ml-2 bg-gradient-orange text-xs"
                        onClick={() => {
                          updateMerchant({ bip39MnemonicBackedUp: true });
                          toast.success('BIP-39 seed phrase marked as backed up');
                        }}
                      >
                        <Check className="w-3 h-3 mr-1" /> I've saved it
                      </Button>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}'''

# New unified Browser Wallet section with Multi-Chain integrated
new_browser_wallet = '''          {walletMode === 'viewonly' && merchant.viewOnlySetupComplete && (
            <div className="p-5 rounded-xl bg-card border border-border space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-foreground">Browser Wallet</h3>
                <Badge className="bg-success/10 text-success border-success/20 text-xs">
                  <Eye className="w-3 h-3 mr-1" /> Active
                </Badge>
              </div>

              {/* Primary Address — always visible */}
              <div className="space-y-1.5">
                <label className="text-[11px] font-medium text-muted-foreground uppercase tracking-wider">Primary Address</label>
                <div className="flex items-center gap-2">
                  <p className="font-mono text-[11px] text-foreground bg-background border border-border rounded-lg p-3 flex-1 break-all leading-relaxed">{merchant.viewOnlyAddress}</p>
                  <Button variant="outline" size="icon" className="shrink-0 border-border hover:border-primary/50 h-8 w-8" onClick={() => { navigator.clipboard.writeText(merchant.viewOnlyAddress); toast.success('Address copied'); }}>
                    <Copy className="w-3.5 h-3.5" />
                  </Button>
                </div>
              </div>

              {/* Multi-Chain Opt-in */}
              <div className="space-y-2">
                <MultiChainOptIn />
                
                {/* Show multi-chain addresses if enabled */}
                {merchant.multiChainEnabled && (
                  <div className="space-y-2 p-4 rounded-lg bg-muted/30 border border-border mt-2">
                    {merchant.ethAddress && (
                      <div className="space-y-1">
                        <label className="text-[10px] font-medium text-muted-foreground">ETH / ARB Address</label>
                        <div className="flex items-center gap-2">
                          <p className="font-mono text-[10px] text-foreground bg-background border border-border rounded p-2 flex-1 break-all">{merchant.ethAddress}</p>
                          <Button variant="ghost" size="icon" className="shrink-0 h-6 w-6" onClick={() => { navigator.clipboard.writeText(merchant.ethAddress || ''); toast.success('ETH/ARB address copied'); }}>
                            <Copy className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    )}
                    {merchant.tronAddress && (
                      <div className="space-y-1">
                        <label className="text-[10px] font-medium text-muted-foreground">TRX Address</label>
                        <div className="flex items-center gap-2">
                          <p className="font-mono text-[10px] text-foreground bg-background border border-border rounded p-2 flex-1 break-all">{merchant.tronAddress}</p>
                          <Button variant="ghost" size="icon" className="shrink-0 h-6 w-6" onClick={() => { navigator.clipboard.writeText(merchant.tronAddress || ''); toast.success('TRX address copied'); }}>
                            <Copy className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Combined Seed Phrase Backup Section */}
              {(!merchant.viewOnlySeedBackedUp || (merchant.multiChainEnabled && !merchant.bip39MnemonicBackedUp)) && (merchant.viewOnlySeedPhrase || (merchant.multiChainEnabled && merchant.bip39Mnemonic)) ? (
                <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/30 space-y-4">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-destructive" />
                    <p className="text-sm font-semibold text-destructive">⚠️ Back up your seed phrases NOW</p>
                  </div>
                  <p className="text-[11px] text-muted-foreground leading-relaxed">
                    Write down these seed phrases in order and store them somewhere safe offline. This is the <strong>only way</strong> to recover your wallets. Once you confirm, phrases will be hidden permanently.
                  </p>

                  {showKey ? (
                    <div className="space-y-4">
                      {/* Monero (XMR) Seed Phrase - 25 words */}
                      {merchant.viewOnlySeedPhrase && (
                        <div className="bg-background border border-border rounded-lg p-3 space-y-2">
                          <div className="flex items-center gap-2">
                            <span className="text-[10px] font-bold text-primary uppercase tracking-wide">Monero (XMR)</span>
                            <span className="text-[10px] text-muted-foreground">• 25 words • Ed25519</span>
                          </div>
                          <p className="font-mono text-xs text-foreground leading-relaxed break-all select-all">{merchant.viewOnlySeedPhrase}</p>
                        </div>
                      )}

                      {/* Multi-Chain (ETH/TRX/ARB) Seed Phrase - 24 words */}
                      {merchant.multiChainEnabled && merchant.bip39Mnemonic && (
                        <div className="bg-background border border-border rounded-lg p-3 space-y-2">
                          <div className="flex items-center gap-2">
                            <span className="text-[10px] font-bold text-primary uppercase tracking-wide">Multi-Chain</span>
                            <span className="text-[10px] text-muted-foreground">• 24 words • BIP-39 • Controls ETH/TRX/ARB</span>
                          </div>
                          <p className="font-mono text-xs text-foreground leading-relaxed break-all select-all">{merchant.bip39Mnemonic}</p>
                        </div>
                      )}

                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-border text-xs"
                          onClick={() => {
                            const textToCopy = [merchant.viewOnlySeedPhrase, merchant.multiChainEnabled ? merchant.bip39Mnemonic : null].filter(Boolean).join('\\n\\n--- MULTI-CHAIN SEED ---\\n\\n');
                            navigator.clipboard.writeText(textToCopy);
                            toast.success('Seed phrases copied — store them safely!');
                          }}
                        >
                          <Copy className="w-3 h-3 mr-1.5" /> Copy All
                        </Button>
                        <Button
                          size="sm"
                          className="bg-gradient-orange text-xs"
                          onClick={() => {
                            const updates: any = {};
                            if (merchant.viewOnlySeedPhrase) updates.viewOnlySeedBackedUp = true;
                            if (merchant.multiChainEnabled && merchant.bip39Mnemonic) updates.bip39MnemonicBackedUp = true;
                            updateMerchant(updates);
                            setShowKey(false);
                            toast.success('Seed phrases marked as backed up');
                          }}
                        >
                          <Check className="w-3 h-3 mr-1.5" /> I've saved them — lock them down
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-destructive/30 text-destructive hover:bg-destructive/10 text-xs"
                      onClick={() => setShowKey(true)}
                    >
                      <Eye className="w-3 h-3 mr-1.5" /> Reveal Seed Phrases
                    </Button>
                  )}
                </div>
              ) : (
                <div className="p-3 rounded-lg bg-muted/50 border border-border">
                  <p className="text-[11px] text-muted-foreground leading-relaxed">
                    🔐 Seed phrases backed up and secured. If you need to access them again, restore from your backup file.
                  </p>
                </div>
              )}'''

# Perform the replacements
print("Replacing Browser Wallet section...")
content = content.replace(old_browser_wallet, new_browser_wallet)

print("Removing old Multi-Chain Wallet section...")
content = content.replace(old_multichain_wallet, '')

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)

print("✅ Seed phrase backup sections consolidated!")
print("- Monero (XMR) and Multi-Chain seeds now in one interface")
print("- Clear labeling for each seed phrase")
print("- Single backup confirmation for all seeds")
