#!/usr/bin/env python3
"""
Fix all doubled wallet names and clean up
"""

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Fix all instances of doubled names
replacements = {
    # Comment line (multiple duplications)
    "/* In-Browser Wallet - Full Self Custody - Full Self Custody - Full Self Custody Mode — FIRST */": "/* In-Browser Wallet - Full Self Custody Mode — FIRST */",

    # Card title (doubled)
    "In-Browser Wallet - Full Self Custody - Full Self Custody": "In-Browser Wallet - Full Self Custody",

    # Dialog titles (okay to keep but let's clean)
    "Create Your Browser Wallet - Full Self Custody": "Create Your Browser Wallet - Full Self Custody",
    "Set Up Browser Wallet - Full Self Custody": "Set Up Browser Wallet - Full Self Custody",

    # Section header (okay)
    "Browser Wallet - Full Self Custody": "Browser Wallet - Full Self Custody",
}

changes = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"✓ Fixed: {old[:60]}...")
    else:
        print(f"- Skipped: {old[:60]}...")

print(f"\n{changes} changes made")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)

print("\n✅ All wallet names cleaned up!")
