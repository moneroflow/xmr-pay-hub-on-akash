#!/usr/bin/env python3
"""
Update wallet type names in SettingsPage
- Change "In-Browser Wallet" to "In-Browser Wallet - Full Self Custody"
- Change "Full Self-Custody" to "Own Node - Full Self Custody (Advanced Only)"
"""

import re

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Define replacements
replacements = {
    # Line 315: Comment
    "/* In-Browser Wallet Mode — FIRST */": "/* In-Browser Wallet - Full Self Custody Mode — FIRST */",

    # Line 330: In-Browser Wallet card title
    "In-Browser Wallet": "In-Browser Wallet - Full Self Custody",

    # Line 359: Full Self-Custody card title
    "Full Self-Custody": "Own Node - Full Self Custody (Advanced Only)",

    # Line 437: Browser Wallet section header
    "Browser Wallet": "Browser Wallet - Full Self Custody",

    # Description text
    "Choose how MoneroFlow connects to the Monero network. In-Browser Wallet is recommended for easy self-custody. Full Self-Custody lets you run your own monero-wallet-rpc.": "Choose how MoneroFlow connects to the Monero network. Both modes offer full self-custody. In-Browser Wallet is recommended for easy setup. Own Node lets you run your own monero-wallet-rpc.",
}

# Apply replacements
changes_made = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        changes_made += 1
        print(f"✓ {old[:50]}...")
    else:
        print(f"✗ Not found: {old[:50]}...")

print(f"\n{changes_made}/{len(replacements)} replacements made")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)

print("\n✅ Wallet names updated successfully!")
