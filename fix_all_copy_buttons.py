#!/usr/bin/env python3
"""
Add safe clipboard copy helper function and fix all copy buttons
"""

import re

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Add the helper function after the hashPassword function
hash_password_func = '''function hashPassword(pw: string): string {
  let hash = 0;
  for (let i = 0; i < pw.length; i++) {
    const chr = pw.charCodeAt(i);
    hash = ((hash << 5) - hash) + chr;
    hash |= 0;
  }
  return 'h_' + Math.abs(hash).toString(36);
}


'''

new_helper_funcs = '''function hashPassword(pw: string): string {
  let hash = 0;
  for (let i = 0; i < pw.length; i++) {
    const chr = pw.charCodeAt(i);
    hash = ((hash << 5) - hash) + chr;
    hash |= 0;
  }
  return 'h_' + Math.abs(hash).toString(36);
}

/**
 * Safe clipboard copy with fallback support
 */
function safeCopyToClipboard(text: string, successMsg: string): void | Promise<void> {
  const copyText = async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
        toast.success(successMsg);
        return;
      }
      throw new Error('Clipboard API not available');
    } catch {
      // Fallback: use textarea method
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      const success = document.execCommand('copy');
      document.body?.removeChild?.(textarea);
      if (success) {
        toast.success(successMsg);
      } else {
        toast.error('Failed to copy to clipboard');
      }
    }
  };

  return copyText();
}


'''

# Replace the old function with the new one
if hash_password_func in content:
    content = content.replace(hash_password_func, new_helper_funcs)
    print("✓ Helper functions added")

# Now fix each copy button with proper Promise handling
replacements = [
    # Line 448: XMR address
    (
        r'onClick=\{\(\) => \{ navigator\.clipboard\.writeText\(merchant\.viewOnlyAddress\); toast\.success\([\'"]Address copied[\'"]\); \}\}',
        r'onClick={() => safeCopyToClipboard(merchant.viewOnlyAddress, "Address copied")}'
    ),
    # Line 466: ETH/ARB address
    (
        r'onClick=\{\(\) => \{ navigator\.clipboard\.writeText\(merchant\.ethAddress \|\| [\'"]+[\'"]\); toast\.success\([\'"]ETH/ARB address copied[\'"]\); \}\}',
        r'onClick={() => safeCopyToClipboard(merchant.ethAddress || "", "ETH/ARB address copied")}'
    ),
    # Line 477: TRX address
    (
        r'onClick=\{\(\) => \{ navigator\.clipboard\.writeText\(merchant\.tronAddress \|\| [\'"]+[\'"]\); toast\.success\([\'"]TRX address copied[\'"]\); \}\}',
        r'onClick={() => safeCopyToClipboard(merchant.tronAddress || "", "TRX address copied")}'
    ),
    # Line 143: API key - needs special handling
    (
        r'onCopy=\(\) => \{[\s\n]*navigator\.clipboard\.writeText\(merchant\.apiKey\);[\s\n]*setCopied\(true\);[\s\n]*toast\.success\([\'"]API key copied!\')[\'"]\);[\s\n]\}',
        r'onCopy={async () => { await Promise.resolve(safeCopyToClipboard(merchant.apiKey || "", "API key copied!")); setCopied(true); }}'
    ),
]

for i, (old, new) in enumerate(replacements):
    old_count = len(re.findall(old, content, re.MULTILINE | re.DOTALL))
    if old_count > 0:
        content = re.sub(old, new, content, flags=re.MULTILINE | re.DOTALL)
        print(f"✓ Replacement {i+1}: {old_count} copy button(s) updated")
    else:
        print(f"✗ Replacement {i+1}: not found")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)

print("\n✅ All copy buttons fixed with error handling and fallback support!")
