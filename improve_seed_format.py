#!/usr/bin/env python3
"""
Improve seed phrase copy format with clear headings
"""

import re

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Find and replace the textToCopy format
old_format = '''                            const textToCopy = seeds.join('\\n\\n--- MULTI-CHAIN SEED ---\\n\\n');'''

new_format = '''                            const textToCopy = seeds.map((seed, i) => {
                              const header = i === 0 ? 
                                '═════════════════════════════════════════\\n' +
                                '🔒 MONERO (XMR) SEED PHRASE\\n' +
                                '   25 words • Ed25519 curve\\n' +
                                '   Controls: Monero (XMR) wallet only\\n' +
                                '═════════════════════════════════════════' :
                                '═════════════════════════════════════════\\n' +
                                '🔗 MULTI-CHAIN SEED PHRASE\\n' +
                                '   24 words • BIP-39 standard\\n' +
                                '   Controls: Ethereum (ETH), Arbitrum (ARB), Tron (TRX)\\n' +
                                '═════════════════════════════════════════';
                              return header + '\\n\\n' + seed;
                            }).join('\\n\\n\\n');'''

if old_format in content:
    content = content.replace(old_format, new_format)
    print("✅ Seed phrase copy format improved with clear headings")
else:
    print("❌ Seed format pattern not found")
    # Try finding the general copy section
    matches = re.findall(r"textToCopy = .*?join", content)
    print(f"Found {len(matches)} textToCopy assignments")
    if matches:
        print("First match:", matches[0][:100] if matches[0] else "Empty")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)
