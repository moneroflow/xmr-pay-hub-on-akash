#!/usr/bin/env python3
"""
Fix PayPage copy address button with error handling
"""

with open('src/pages/PayPage.tsx', 'r') as f:
    content = f.read()

# Fix the copyAddr function
old_copy = '''  const copyAddr = () => {
    const addr = isTrxPayment ? trxAddress : subaddress;
    navigator.clipboard.writeText(addr);
    setCopied(true);
    toast.success(isTrxPayment ? 'TRX address copied!' : 'XMR address copied!');
    setTimeout(() => setCopied(false), 2000);
  };'''

new_copy = '''  const copyAddr = () => {
    const addr = isTrxPayment ? trxAddress : subaddress;
    try {
      navigator.clipboard.writeText(addr).then(() => {
        setCopied(true);
        toast.success(isTrxPayment ? 'TRX address copied!' : 'XMR address copied!');
        setTimeout(() => setCopied(false), 2000);
      }).catch(() => {
        const t = document.createElement('textarea');
        t.value = addr;
        t.style.position = 'fixed';
        t.style.opacity = '0';
        document.body.appendChild(t);
        t.select();
        document.execCommand('copy');
        document.body.removeChild(t);
        setCopied(true);
        toast.success(isTrxPayment ? 'TRX address copied!' : 'XMR address copied!');
        setTimeout(() => setCopied(false), 2000);
      });
    } catch {
      toast.error('Failed to copy address');
    }
  };'''

content = content.replace(old_copy, new_copy)

with open('src/pages/PayPage.tsx', 'w') as f:
    f.write(content)

print("✅ PayPage copy address button fixed")
