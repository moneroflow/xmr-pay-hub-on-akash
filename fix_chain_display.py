#!/usr/bin/env python3
"""
Fix chain display - labels, icons, and PayPage titles
"""

# 1. Fix PaymentLinksPage imports and chain display
with open('src/pages/dashboard/PaymentLinksPage.tsx', 'r') as f:
    content = f.read()

# Add icons to imports
old_imports = "import { Plus, Copy, Trash2, ExternalLink, Upload, Power, PowerOff, ShoppingBag } from 'lucide-react';"
new_imports = "import { Plus, Copy, Trash2, ExternalLink, Upload, Power, PowerOff, ShoppingBag, Bitcoin, Activity } from 'lucide-react';"
content = content.replace(old_imports, new_imports)

# Add chain badge after power toggle
old_power_section = "                            {link.active ? <Power className=\"w-4 h-4 text-success\" /> : <PowerOff className=\"w-4 h-4 text-muted-foreground\" />}"
new_power_section = """                            {link.active ? <Power className="w-4 h-4 text-success" /> : <PowerOff className="w-4 h-4 text-muted-foreground" />}
                            {link.chainType === 'trx' ? (
                              <Badge variant="outline" className="bg-orange-500/10 text-orange-500 border-orange-500/20 text-xs gap-1.5 py-1 ml-2">
                                <Activity className="w-3 h-3" />
                                <span>TRON</span>
                              </Badge>
                            ) : (
                              <Badge variant="outline" className="bg-orange-500/10 text-orange-500 border-orange-500/20 text-xs gap-1.5 py-1 ml-2">
                                <Bitcoin className="w-3 h-3" />
                                <span>Monero</span>
                              </Badge>
                            )}"""
content = content.replace(old_power_section, new_power_section)

# Update label display to be clearer
if '<p className="text-sm font-medium">{link.label}</p>' in content:
    content = content.replace('</p> - </p>', '</p>')

with open('src/pages/dashboard/PaymentLinksPage.tsx', 'w') as f:
    f.write(content)

print("✅ PaymentLinksPage: Added chain icons and badges")
print("  - Activity icon for TRON")
print("  - Bitcoin icon for Monero")
print("  - Color-coded badges")

# 2. Fix PayPage to show correct title based on chain
with open('src/pages/PayPage.tsx', 'r') as f:
    content = f.read()

# Fix the header title
old_title = "            <h1 className=\"text-xl font-bold text-foreground\">\n              {label ? decodeURIComponent(label).replace(/-/g, ' ') : 'Payment'}\n            </h1>\n            <p className=\"text-muted-foreground text-sm mt-1\">Pay with {chainName}</p>"
new_title = "            <h1 className=\"text-xl font-bold text-foreground\">\n              {label ? decodeURIComponent(label).replace(/-/g, ' ') : 'Payment'}\n            </h1>\n            <p className=\"text-muted-foreground text-sm mt-1\">{isTrxPayment ? 'Pay with TRON (USDT)' : 'Pay with Monero (XMR)'}</p>"
content = content.replace(old_title, new_title)

# Fix TRX badge description
old_badge = "{\"Multi-Chain\" }"
new_badge = "{isTrxPayment ? 'TRON (USDT)' : 'Multi-Chain'}"
content = content.replace(old_badge, new_badge)

# Fix multi-chain header
old_multi_header = "Multi-Chain Wallet"
new_multi_header = "{isTrxPayment ? 'TRON (USDT)' : 'Multi-Chain'}"
content = content.replace(old_multi_header, new_multi_header)

with open('src/pages/PayPage.tsx', 'w') as f:
    f.write(content)

print("✅ PayPage: Fixed titles to show chain correctly")
print("  - Monero payments show 'Pay with Monero (XMR)'")
print("  - TRX payments show 'Pay with TRON (USDT)'")
print("  - Multi-chain badge updated")

print("\n✅ All display fixes applied")
