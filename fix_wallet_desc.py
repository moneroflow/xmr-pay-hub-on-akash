#!/usr/bin/env python3
"""
Fix the doubled description text
"""

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Fix the doubled description
old_desc = '''text="Choose how MoneroFlow connects to the Monero network. In-Browser Wallet - Full Self Custody - Full Self Custody is recommended for easy self-custody. Own Node - Full Self Custody (Advanced Only) lets you run your own monero-wallet-rpc."'''

new_desc = '''text="Choose how MoneroFlow connects to the Monero network. Both modes offer full self-custody. In-Browser Wallet - Full Self Custody is recommended for easy setup. Own Node - Full Self Custody (Advanced Only) lets you run your own monero-wallet-rpc."'''

if old_desc in content:
    content = content.replace(old_desc, new_desc)
    print("✅ Description text fixed!")
else:
    print("❌ Description text not found - searching for similar patterns...")
    # Try partial match
    if "In-Browser Wallet - Full Self Custody - Full Self Custody" in content:
        content = content.replace(
            "In-Browser Wallet - Full Self Custody - Full Self Custody",
            "In-Browser Wallet - Full Self Custody"
        )
        print("✅ Fixed doubled wallet name in description")
    else:
        print("❌ Pattern not found")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)
