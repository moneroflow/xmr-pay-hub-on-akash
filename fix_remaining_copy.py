#!/usr/bin/env python3
"""
Fix all remaining copy buttons manually
"""

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Fix the remaining copy buttons using simpler string replacement
fixes = [
    # Line 46: API key copy in copyKey function
    (
        "  const copyKey = () => {\n    navigator.clipboard.writeText(merchant.apiKey);",
        "  const copyKey = () => {\n    try { navigator.clipboard.writeText(merchant.apiKey).then(() => toast.success('API key copied!')).catch(() => {\n      const t = document.createElement('textarea'); t.value = merchant.apiKey; t.style.position = 'fixed'; t.style.opacity = '0'; document.body.appendChild(t); t.select(); document.execCommand('copy'); document.body.removeChild(t); toast.success('API key copied!');\n    }); } catch { toast.error('Failed to copy'); }"
    ),
    # Line 339: XMR address copy
    (
        'onClick={() => { navigator.clipboard.writeText(merchant.viewOnlyAddress); toast.success(\'Address copied\'); }}>',
        'onClick={() => { try { navigator.clipboard.writeText(merchant.viewOnlyAddress).then(() => toast.success(\'Address copied\')).catch(() => {\n      const t = document.createElement(\'textarea\'); t.value = merchant.viewOnlyAddress; t.style.position = \'fixed\'; t.style.opacity = \'0\'; document.body.appendChild(t); t.select(); document.execCommand(\'copy\'); document.body.removeChild(t); toast.success(\'Address copied\');\n    }); } catch { toast.error(\'Failed to copy\'); }}>'
    ),
    # Line 366: Seed phrase copy (Copy All button)
    (
        'if (navigator.clipboard && navigator.clipboard.writeText) {\n                              navigator.clipboard.writeText(textToCopy)',
        'if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(textToCopy)'
    ),
]

changes = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        changes += 1

print(f"Fixed {changes} copy buttons manually")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)

print(f"\n✅ Done! {changes} buttons fixed")
