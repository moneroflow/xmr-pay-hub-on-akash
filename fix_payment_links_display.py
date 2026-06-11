#!/usr/bin/env python3
"""
Fix PaymentLinksPage display - show chain type with icons and clear labeling
"""

with open('src/pages/dashboard/PaymentLinksPage.tsx', 'r') as f:
    content = f.read()

# Update payment link card display to show chain type
# Find the card rendering section and add chain badge

# Update imports to include icons
old_imports = '''import { Plus, Copy, Trash2, ExternalLink, Upload, Power, PowerOff, ShoppingBag } from ';'lucide-react';'''

new_imports = '''import { Plus, Copy, Trash2, ExternalLink, Upload, Power, PowerOff, ShoppingBag, Bitcoin, Activity, ChevronRight } from 'lucide-react';'''

if old_imports in content:
    content = content.replace(old_imports, new_imports)

# Update the payment link card to show chain type
# Find the card rendering section where link.label is displayed
old_card_display = r'''                        <div className="mt-3">
                          <code className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded font-mono">
                            \{buildPayUrl\(link\)\}
                          </code>
                        </div>'''

# We'll make this more complex - need to render based on chain type
# For now, let's add chain identification to the label display
old_label_section = r'''                    <div className="mt-2">
                      <p className="text-sm font-medium">\{link.label\}</p>
                    </div>'''

new_label_section = '''                    <div className="mt-2">
                      <div className="flex items-center gap-2">
                        {link.chainType === 'trx' ? (
                          <>
                            <Activity className="w-3.5 h-3.5 text-orange-500" />
                            <span className="text-sm font-medium">{link.label} - TRON (USDT)</span>
                          </>
                        ) : (
                          <>
                            <Bitcoin className="w-3.5 h-3.5 text-orange-500" />
                            <span className="text-sm font-medium">{link.label} - Monero (XMR)</span>
                          </>
                        )}
                      </div>
                    </div>'''

# Use sed for the large replacement - the regex may be too complex
# Let's use string replacement for the simpler label section

# Actually, let's find the label rendering more precisely
if "#2""link.label" in content:
    content = content.replace("#2""link.label#2"", ""#2""link.label + (link.chainType === \"trx\" ? \" - TRON\" : \"\")#2""")

# Let's add chain badges more carefully by looking for the card structure

with open('src/pages/dashboard/PaymentLinksPage.tsx', 'w') as f:
    f.write(content)

print("✅ PaymentLinksPage: Attempted chain display fixes")
print("Note: Label section needs manual review - adding chain badges systematically")

# Now let's create a comprehensive fix that targets the actual card rendering
