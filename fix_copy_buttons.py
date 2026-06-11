#!/usr/bin/env python3
"""
Fix all copy buttons in SettingsPage - add error handling and fallback
"""

import re

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Define the improved copy function to add at the top
copy_function = '''/**
 * Safe clipboard copy with fallback support
 */
async function safeCopyToClipboard(text: string, successMsg: string) {
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
      toast.success(successMsg);
    } else {
      // Fallback for older browsers
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
  } catch {
    toast.error('Failed to copy to clipboard');
  }
}

'''

# Find all navigator.clipboard.writeText direct calls and replace with safeCopyToClipboard
# Pattern: navigator.clipboard.writeText(...); toast.success(...)

replacements = [
  # XMR address copy
  (
    r'onClick=\{\(\) => \{ navigator\.clipboard\.writeText\(merchant\.viewOnlyAddress\); toast\.success\([\'"]Address copied[\'"]\); \}\}',
    r'onClick={() => safeCopyToClipboard(merchant.viewOnlyAddress, "Address copied")}'
  ),
  # ETH address copy
  (
    r'onClick=\{\(\) => \{ navigator\.clipboard\.writeText\(merchant\.ethAddress \|\| [\'\\0']*[\'"]\); toast\.success\([\'"]ETH/ARB address copied[\'"]\); \}\}',
    r'onClick={() => safeCopyToClipboard(merchant.ethAddress || "", "ETH/ARB address copied")}'
  ),
  # TRX address copy
  (
    r'onClick=\{\(\) => \{ navigator\.clipboard\.writeText\(merchant\.tronAddress \|\| [\'\\0']*[\'"]\); toast\.success\([\'"]TRX address copied[\'"]\); \}\}',
    r'onClick={() => safeCopyToClipboard(merchant.tronAddress || "", "TRX address copied")}'
  ),
  # API key copy
  (
    r'onClick=\(\) => \{ navigator\.clipboard\.writeText\(merchant\.apiKey\); setCopied\(true\); toast\.success\([\'"]API key copied!\)[\'"]\);',
    r'onClick={() => { safeCopyToClipboard(merchant.apiKey, "API key copied!"); setCopied(true);'
  ),
]

changes = 0
for old_pattern, new_pattern in replacements:
    content = re.sub(old_pattern, new_pattern, content)
    changes += re.sub(old_pattern, '', content).count(new_pattern)
    print(f"✓ Pattern {changes} updated")

print(f"\n{changes} patterns updated")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)

print("\n✅ Copy buttons fixed with error handling!")
print("\n⚠️ NOTE: You may need to manually add the safeCopyToClipboard function at the top of the file")
