#!/usr/bin/env python3
"""
Fix Copy All button - add error handling and better copy logic
"""

import re

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Find the Copy All button and replace with improved version
old_copy_all = '''                      <div className="flex gap-2">
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
                        </Button>'''

new_copy_all = '''                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-border text-xs"
                          onClick={() => {
                            try {
                              const seeds = [];
                              if (merchant.viewOnlySeedPhrase) {
                                seeds.push(merchant.viewOnlySeedPhrase);
                              }
                              if (merchant.multiChainEnabled && merchant.bip39Mnemonic) {
                                seeds.push(merchant.bip39Mnemonic);
                              }
                              const textToCopy = seeds.join('\\n\\n--- MULTI-CHAIN SEED ---\\n\\n');
                              navigator.clipboard.writeText(textToCopy)
                                .then(() => toast.success('Seed phrases copied — store them safely!'))
                                .catch(() => {
                                  // Fallback: create temporary textarea
                                  const textarea = document.createElement('textarea');
                                  textarea.value = textToCopy;
                                  textarea.style.position = 'fixed';
                                  textarea.style.opacity = '0';
                                  document.body.appendChild(textarea);
                                  textarea.select();
                                  document.execCommand('copy');
                                  document.body.removeChild(textarea);
                                  toast.success('Seed phrases copied — store them safely! (fallback)');
                                });
                            } catch {
                              toast.error('Failed to copy seed phrases');
                            }
                          }}
                        >
                          <Copy className="w-3 h-3 mr-1.5" /> Copy All
                        </Button>'''

if old_copy_all in content:
    content = content.replace(old_copy_all, new_copy_all)
    print("✅ Copy All button fixed with error handling and fallback")
else:
    print("❌ Old Copy All button pattern not found")
    print("Searching for Copy All button...")
    matches = re.findall(r"Copy All", content)
    print(f"Found {len(matches)} instances of 'Copy All'")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)
