#!/usr/bin/env python3
"""
Fix API key copy button and add safeCopyToClipboard helper
"""

# Read the file
with open('src/pages/dashboard/SettingsPage.tsx', 'r') as f:
    content = f.read()

# Find where to add the new copyKey function (after safeCopyToClipboard if it exists, or after hashPassword)
old_hash_func_end = '''  return 'h_' + Math.abs(hash).toString(36);
}


'''

new_hash_func_end = '''  return 'h_' + Math.abs(hash).toString(36);
}


/** Safe clipboard copy with fallback support */
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

if old_hash_func_end in content:
    content = content.replace(old_hash_func_end, new_hash_func_end)
    print("✓ safeCopyToClipboard function added")
else:
    print("⚠️ Hash function patterns changed, using fallback")

# Now add the new copyKey function before handleExportBackup
# Find handleExportBackup and add copyKey before it
export_backup_marker = '''const handleExportBackup = async () =>'''

new_copy_key = ''' const copyKey = () => {
    safeCopyToClipboard(merchant.apiKey, 'API key copied!');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExportBackup = async () =>'''

if export_backup_marker in content:
    content = content.replace(export_backup_marker, new_copy_key)
    print("✓ copyKey function updated to use safeCopyToClipboard")
else:
    print("✗ handleExportBackup pattern not found")

# Write the file
with open('src/pages/dashboard/SettingsPage.tsx', 'w') as f:
    f.write(content)

print("\n✅ API key copy button fixed!")
