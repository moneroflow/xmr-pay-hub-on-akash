#!/usr/bin/env python3
"""
Update PayPage to show USDT branding and display USDT amounts
"""

with open('src/pages/PayPage.tsx', 'r') as f:
    content = f.read()

# Pay with TRX/USDT branding
old_branding = "Pay with {chainName}"
new_branding = "Pay with TRON (USDT {isTrxPayment ? '/ TRX' : ''})"
content = content.replace(old_branding, new_branding)

# Show USDT amount instead of TRX amount
old_amount = "isTrxPayment ? `${trxAmount.toFixed(2)} TRX` : formatXMR(xmrAmount)"
new_amount = "isTrxPayment ? `${fiatAmount.toFixed(2)} USDT` : formatXMR(xmrAmount)"
content = content.replace(old_amount, new_amount)

# Update on-chain text
old_onchain = "rateLabel} = {displaySymbol}{referenceRate.toFixed(2)} {displayCurrency}"
new_onchain = "rateLabel} = {isTrxPayment ? '1 USDT' : `${displaySymbol}${referenceRate.toFixed(2)} ${displayCurrency}`}"
content = content.replace(old_onchain, new_onchain)

with open('src/pages/PayPage.tsx', 'w') as f:
    f.write(content)

print("✅ PayPage updated with USDT branding and amounts")
