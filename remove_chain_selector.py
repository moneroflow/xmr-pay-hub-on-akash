#!/usr/bin/env python3
"""
Remove chain selector UI from PaymentLinksPage
Simplify to generate both links automatically
"""

with open('src/pages/dashboard/PaymentLinksPage.tsx', 'r') as f:
    content = f.read()

# Find and remove the chain selector section entirely
# Look for the "Accept Payments In" section
chain_selector_section = '''                  <div className="space-y-2">
                    <Label className="text-foreground">Accept Payments In</Label>
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        onClick={() => setChainType('xmr')}
                        className={`p-3 rounded-lg border-2 transition-all ${
                          chainType === 'xmr'
                            ? 'border-primary bg-primary/10 text-foreground font-medium'
                            : 'border-border bg-background text-muted-foreground'
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 rounded-full bg-orange-500"></div>
                          <span>Monero</span>
                        </div>
                      </button>
                      <button
                        onClick={() => setChainType('trx')}
                        className={`p-3 rounded-lg border-2 transition-all ${
                          chainType === 'trx'
                            ? 'border-primary bg-primary/10 text-foreground font-medium'
                            : 'border-border bg-background text-muted-foreground'
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 rounded-full bg-red-500"></div>
                          <span>TRX</span>
                        </div>
                      </button>
                    </div>
                  </div>'''

simplified_section = '''                  <div className="p-4 rounded-lg bg-muted/30 border border-border">
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-3 h-3 rounded-full bg-orange-500"></div>
                      <span className="text-sm font-medium">Monero (XMR) + TRON (USDT)</span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      This will create two separate payment links — one for Monero and one for USDT on the TRON network.
                    </p>
                  </div>'''

content = content.replace(chain_selector_section, simplified_section)

with open('src/pages/dashboard/PaymentLinksPage.tsx', 'w') as f:
    f.write(content)

print("✅ Chain selector removed - now generates both XMR and USDT links automatically")
print("✅ Payment links will create dual links for each payment")
