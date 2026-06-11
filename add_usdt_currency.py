#!/usr/bin/env python3
"""
Add USDT support to currency service
"""

with open('src/lib/currency-service.ts', 'r') as f:
    content = f.read()

# Add USDT API endpoint
usdt_fetch = '''
// ── Fetch USDT price from exchanges ──
async function fetchUsdtPrice(): Promise<number> {
  const sources = [
    async () => {
      const r = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=usd', { signal: AbortSignal.timeout(5000) });
      const d = await r.json();
      return d.tether?.usd || 1.0;
    },
    async () => {
      const r = await fetch('https://min-api.cryptocompare.com/data/price?fsym=USDT&tsyms=USD', { signal: AbortSignal.timeout(5000) });
      const d = await r.json();
      return d.USD || 1.0;
    },
  ];

  for (const src of sources) {
    try {
      const price = await src();
      if (price && price > 0) return price;
    } catch { /* try next */ }
  }
  return 1.0; // USDT is pegged to USD
}
'''

# Add USDT exports
usdt_exports = '''
export function usdToUsdt(usdAmount: number): number {
  return usdAmount; // 1 USD = 1 USDT (pegged)
}

export function usdtToFiat(usdtAmount: number): number {
  return usdtAmount; // 1 USDT = 1 USD (pegged)
}

export function getUsdtPrice(fiatCurrency: string, rates: CachedRates): number {
  const fiatRate = rates.fiatRates[fiatCurrency] || 1;
  return fiatRate; // USDT mirrors USD rate for other currencies
}
'''

# Insert USDT fetch before fetchXmrUsd
if 'fetchXmrUsd() {' in content and 'fetchUsdtPrice()' not in content:
    content = content.replace('async function fetchXmrUsd(): Promise<number> {', usdt_fetch + 'async function fetchXmrUsd(): Promise<number> {', count=1)

# Add USDT exports at the end
if 'export function getXmrPrice' in content and 'export function getUsdtPrice' not in content:
    content += usdt_exports

with open('src/lib/currency-service.ts', 'w') as f:
    f.write(content)

print("✅ USDT support added to currency service")
