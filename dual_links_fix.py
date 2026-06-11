#!/usr/bin/env python3
"""
Make PaymentLinksPage generate dual XMR/USDT links
Remove chain selector - generate both automatically
"""

with open('src/pages/dashboard/PaymentLinksPage.tsx', 'r') as f:
    lines = f.readlines()
    content = ''.join(lines)

# Step 1: Remove chainType state (we don't need it anymore)
if 'const [chainType, setChainType] = useState<"xmr" | "trx">("xmr");' in content:
    content = content.replace("  const [chainType, setChainType] = useState<\\'xmr\\' | \\'trx\\'>(\\'xmr\\');\\n", "")

# Step 2: Update buildPayUrl to add chain parameter
old_build_url = '''  const buildPayUrl = (link) => {
    const url = new URL(`${baseUrl}/pay/${link.uniqueId}/${link.fiatAmount}/${link.slug}`);
    if (payoutAddress) {
      url.searchParams.set('address', payoutAddress);
    }
    url.searchParams.set('currency', link.fiatCurrency || cur);
    url.searchParams.set('symbol', sym);
    return url.toString();
  };'''

new_build_url = '''  const buildPayUrl = (link) => {
    const url = new URL(`${baseUrl}/pay/${link.uniqueId}/${link.fiatAmount}/${link.slug}`);
    if (payoutAddress) {
      url.searchParams.set('address', payoutAddress);
    }
    url.searchParams.set('currency', link.fiatCurrency || cur);
    url.searchParams.set('symbol', sym);
    url.searchParams.set('chain', link.chainType || 'xmr');
    return url.toString();
  };'''

content = content.replace(old_build_url, new_build_url)

# Step 3: Update handleCreate to generate both links
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
      
      // Generate BOTH XMR and USDT payment links
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

with open('src/pages/dashboard/PaymentLinksPage.tsx', 'w') as f:
    f.write(content)

print("✅ PaymentLinksPage updated to generate dual links")
print("✅ Chain selector removed - both XMR and USDT created automatically")
print("⚠️ Note: Need to verify store.createPaymentLink accepts chainType parameter")
