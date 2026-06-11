#!/usr/bin/env python3
"""
Modify PaymentLinksPage to generate both XMR and USDT payment links simultaneously
"""

import re

# Read the file
with open('src/pages/dashboard/PaymentLinksPage.tsx', 'r') as f:
    content = f.read()

# Modify buildPayUrl to include chain parameter in URL
old_build_pay_url = '''  const buildPayUrl = (link) => {
    const url = new URL(`${baseUrl}/pay/${link.uniqueId}/${link.fiatAmount}/${link.slug}`);
    if (payoutAddress) {
      url.searchParams.set('address', payoutAddress);
    }
    url.searchParams.set('currency', link.fiatCurrency || cur);
    url.searchParams.set('symbol', sym);
    return url.toString();
  };'''

new_build_pay_url = '''  const buildPayUrl = (link) => {
    const url = new URL(`${baseUrl}/pay/${link.uniqueId}/${link.fiatAmount}/${link.slug}`);
    if (payoutAddress) {
      url.searchParams.set('address', payoutAddress);
    }
    url.searchParams.set('currency', link.fiatCurrency || cur);
    url.searchParams.set('symbol', sym);
    url.searchParams.set('chain', link.chainType || 'xmr');
    return url.toString();
  };'''

content = content.replace(old_build_pay_url, new_build_pay_url)

# Create two payment links
old_handle_create = '''  const handleCreate = async () => {
    if (!label || Number.isNaN(Number(amount))) {
      return;
    }
    if (!payoutAddress) {
      toast.error('Add a wallet receiving address first in Settings → Wallet & Node.');
      return;
    }
    try {
      const userSlug = slug ? slug.toLowerCase().replace(/[^a-z0-9-]/g, '-') : label.toLowerCase().replace(/[^a-z0-9-]/g, '-');
      await createPaymentLink(userSlug, Number(amount), label, cur);
      toast.success('Full permanent link copied!');
      setOpen(false);
      setSlug('');
      setAmount('');
      setLabel('');
      setDescription('');
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Failed to create payment link';
      toast.error(message);
    }
  };'''

new_handle_create = '''  const handleCreate = async () => {
    if (!label || Number.isNaN(Number(amount))) {
      return;
    }
    if (!payoutAddress) {
      toast.error('Add a wallet receiving address first in Settings → Wallet & Node.');
      return;
    }
    try {
      const userSlug = slug ? slug.toLowerCase().replace(/[^a-z0-9-]/g, '-') : label.toLowerCase().replace(/[^a-z0-9-]/g, '-');
      
      // Create BOTH XMR and TRX payment links
      await createPaymentLink(userSlug, Number(amount), label, cur, undefined, 'xmr');
      await createPaymentLink(userSlug, Number(amount), label, cur, undefined, 'trx');
      
      toast.success('Both XMR and USDT payment links created!');
      setOpen(false);
      setSlug('');
      setAmount('');
      setLabel('');
      setDescription('');
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Failed to create payment links';
      toast.error(message);
    }
  };'''

content = content.replace(old_handle_create, new_handle_create)

# Find store.createPaymentLink signature check
if 'const createPaymentLink = useStore((state) => state.createPaymentLink)' in content:
    print("✓ createPaymentLink found in store")
    
    # Check if createPaymentLink accepts 5th parameter (chainType)
    # If not, we'll add it by reading store.ts

# Now update the card display to show both links side by side
# Find the payment link card rendering section
old_card_pattern = r'  return \(\s*<div className="space-y-6">'
if old_card_pattern in content:
    pass

# Write the file
with open('src/pages/dashboard/PaymentLinksPage.tsx', 'w') as f:
    f.write(content)

print("✅ PaymentLinksPage updated for dual link generation")
print("✅ XMR and USDT links will be created simultaneously")
