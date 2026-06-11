#!/usr/bin/env python3
"""
Fix copy buttons with proper error handling - working version
Uses same pattern as our working Copy All button in PayPage
"""

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Fix inline copy buttons with the proven pattern from PayPage
replacements = [
    # Line 448: XMR address
    (
        r'onClick=\{\(\) => \{ navigator\.clipboard\.writeText\(merchant\.viewOnlyAddress\); toast\.success\([\'"]Address copied[\'"]\); \}\}',
        r'onClick={() => { try { navigator.clipboard.writeText(merchant.viewOnlyAddress).then(() => toast.success("Address copied")).catch(() => { const t = document.createElement("textarea"); t.value = merchant.viewOnlyAddress; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); document.execCommand("copy"); document.body.removeChild(t); toast.success("Address copied"); }); } catch { toast.error("Failed to copy"); } }}'
    ),
    # Line 466: ETH/ARB address
    (
        r'onClick=\{\(\) => \{ navigator\.clipboard\.writeText\(merchant\.ethAddress \|\| [\'"]\*[\'"]\); toast\.success\([\'"]ETH/ARB address copied[\'"]\); \}\}',
        r'onClick={() => { try { navigator.clipboard.writeText(merchant.ethAddress || "").then(() => toast.success("ETH/ARB address copied")).catch(() => { const t = document.createElement("textarea"); t.value = merchant.ethAddress || ""; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); document.execCommand("copy"); document.body.removeChild(t); toast.success("ETH/ARB address copied"); }); } catch { toast.error("Failed to copy"); } }}'
    ),
    # Line 477: TRX address
    (
        r'onClick=\{\(\) => \{ navigator\.clipboard\.writeText\(merchant\.tronAddress \|\| [\'"]\*[\'"]\); toast\.success\([\'"]TRX address copied[\'"]\); \}\}',
        r'onClick={() => { try { navigator.clipboard.writeText(merchant.tronAddress || "").then(() => toast.success("TRX address copied")).catch(() => { const t = document.createElement("textarea"); t.value = merchant.tronAddress || ""; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); document.execCommand("copy"); document.body.removeChild(t); toast.success("TRX address copied"); }); } catch { toast.error("Failed to copy"); } }}'
    ),
]

import re
changes = 0
for old, new in replacements:
    if re.search(old, content):
        content = re.sub(old, new, content)
        changes += 1
        print(f"✓ Copy button {changes} fixed")

print(f"\n{changes}/{len(replacements)} copy buttons updated")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)

print("\n✅ Copy buttons fixed with error handling!")
