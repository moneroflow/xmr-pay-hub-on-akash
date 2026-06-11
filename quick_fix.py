#!/usr/bin/env python3
import re
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f: content = f.read()
if 'navigator.clipboard.writeText(merchant.viewOnlyAddress);' in content:
    old = r'onClick={() => \{ navigator\.clipboard\.writeText\(merchant\.viewOnlyAddress\); toast\.success\(\\x27Address copied\\x27\); \}\}>'
    new = r'onClick={() => { try { navigator.clipboard.writeText(merchant.viewOnlyAddress).then(() => toast.success("Address copied")).catch(() => { const t = document.createElement("textarea"); t.value = merchant.viewOnlyAddress; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); document.execCommand("copy"); document.body.removeChild(t); toast.success("Address copied"); }); } catch { toast.error("Failed to copy"); } }}>'
    content = re.sub(old, new, content)
    if 'onClick={() => { try { navigator.clipboard.writeText(merchant.viewOnlyAddress)' in content:
        print("✓ XMR address copy fixed")
    else:
        print("✗ XMR address copy fix failed")
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f: f.write(content)
print("✅ Done")
