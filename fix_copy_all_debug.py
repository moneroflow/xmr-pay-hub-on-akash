#!/usr/bin/env python3
"""
Fix Copy All button - add debugging and more robust logic
"""

import re

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Find and replace the Copy All onClick handler
old_copy_handler = '''                      <div className="flex gap-2">
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

new_copy_handler = '''                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          className="border-border text-xs"
                          onClick={() => {
                            // Collect seeds
                            const seeds = [];
                            if (merchant.viewOnlySeedPhrase) {
                              seeds.push(merchant.viewOnlySeedPhrase);
                              console.log('[CopyAll] Monero seed available');
                            }
                            if (merchant.multiChainEnabled && merchant.bip39Mnemonic) {
                              seeds.push(merchant.bip39Mnemonic);
                              console.log('[CopyAll] Multi-chain seed available');
                            }

                            console.log('[CopyAll] Seeds to copy:', seeds.length);
                            
                            if (seeds.length === 0) {
                              toast.error('No seed phrases available to copy');
                              return;
                            }

                            const textToCopy = seeds.join('\\n\\n--- MULTI-CHAIN SEED ---\\n\\n');
                            console.log('[CopyAll] Text length:', textToCopy.length);

                            // Try clipboard API first
                            if (navigator.clipboard && navigator.clipboard.writeText) {
                              navigator.clipboard.writeText(textToCopy)
                                .then(() => {
                                  console.log('[CopyAll] Clipboard API success');
                                  toast.success('Seed phrases copied — store them safely!');
                                })
                                .catch((err) => {
                                  console.log('[CopyAll] Clipboard API failed, using fallback:', err);
                                  // Fallback: create temporary textarea
                                  const textarea = document.createElement('textarea');
                                  textarea.value = textToCopy;
                                  textarea.style.position = 'fixed';
                                  textarea.style.opacity = '0';
                                  document.body.appendChild(textarea);
                                  textarea.select();
                                  try {
                                    const success = document.execCommand('copy');
                                    document.body.removeChild(textarea);
                                    if (success) {
                                      console.log('[CopyAll] execCommand copy success');
                                      toast.success('Seed phrases copied — store them safely!');
                                    } else {
                                      console.log('[CopyAll] execCommand copy failed');
                                      toast.error('Copy failed (both methods)');
                                    }
                                  } catch (e) {
                                    console.log('[CopyAll] execCommand error:', e);
                                    document.body?.removeChild?.(textarea);
                                    toast.error('Copy failed (both methods)');
                                  }
                                });
                            } else {
                              // No clipboard API, use fallback directly
                              console.log('[CopyAll] No clipboard API, using fallback');
                              const textarea = document.createElement('textarea');
                              textarea.value = textToCopy;
                              textarea.style.position = 'fixed';
                              textarea.style.opacity = '0';
                              document.body.appendChild(textarea);
                              textarea.select();
                              try {
                                const success = document.execCommand('copy');
                                document.body.removeChild(textarea);
                                if (success) {
                                  console.log('[CopyAll] Fallback copy success');
                                  toast.success('Seed phrases copied — store them safely!');
                                } else {
                                  console.log('[CopyAll] Fallback copy failed');
                                  toast.error('Copy failed');
                                }
                              } catch (e) {
                                console.log('[CopyAll] Fallback error:', e);
                                document.body?.removeChild?.(textarea);
                                toast.error('Copy failed');
                              }
                            }
                          }}
                        >
                          <Copy className="w-3 h-3 mr-1.5" /> Copy All
                        </Button>'''

if old_copy_handler in content:
    content = content.replace(old_copy_handler, new_copy_handler)
    print("✅ Copy All button fixed with console logging and better error handling")
else:
    print("❌ Old Copy All button pattern not found")
    # Try simpler pattern match
    if "onClick={() => {" in content and "Copy All" in content:
        print("⚠️ Found Copy All but pattern doesn't match exactly")
    else:
        print("❌ Might need manual fix")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)
