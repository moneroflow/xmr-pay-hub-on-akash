#!/usr/bin/env python3
"""
Add XMR/TRX toggle toggle to PosPage header
"""

with open('src/pages/dashboard/PosPage.tsx', 'r') as f:
    content = f.read()

# Find where to add the state and import
# Add useState import if not present
if 'useState, useCallback, useEffect, useMemo' in content and 'selectedChain' not in content:
    # Add selectedChain state after existing useState declarations
    code_marker = 'const [input, setInput] = useState(\'0\');'
    new_state = code_marker + '''
  const [selectedChain, setSelectedChain] = useState<\'xmr\' | \'trx\'>(\'xmr\');'''
    content = content.replace(code_marker, new_state)

# Import Toggle component from switch
if 'import { Switch' not in content:
    import_line = 'import { Button } from \'@/components/ui/button\';'
    new_import = '''import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';'''
    content = content.replace(import_line, new_import)

# Add Toggle component in the header (after user selector)
# Find the user selector section and add the chain toggle
if 'let {showAddButton' in content and 'Chain Toggle' not in content:
    toggle_html = '''        {/* ═══ Payment Chain Toggle ═══ */}
        <div className="flex items-center gap-2 bg-card border border-border rounded-lg px-3 py-2">
          <span className={`text-xs font-medium ${selectedChain === 'xmr' ? 'text-primary' : 'text-muted-foreground'}`}>XMR</span>
          <Switch
            checked={selectedChain === 'trx'}
            onCheckedChange={(checked) => setSelectedChain(checked ? 'trx' : 'xmr')}
            className="bg-muted data-[state=checked]:bg-primary"
          />
          <span className={`text-xs font-medium ${selectedChain === 'trx' ? 'text-orange-500' : 'text-muted-foreground'}`}>TRX/USDT</span>
        </div>
'''

    # Insert after user selector closing div
    if '{users.length > 0 && (' in content:
        insert_point = '{users.length > 0 && ('
        idx = content.find(insert_point)
        if idx > 0:
            # Find the closing div of this section
            closing_idx = content.find('</div>\n      )}\n      <div className="flex flex-col lg:flex-row', idx)
            if closing_idx > idx:
                content = content[:closing_idx] + toggle_html + '\n' + content[closing_idx:]

with open('src/pages/dashboard/PosPage.tsx', 'w') as f:
    f.write(content)

print("✅ XMR/TRX toggle added to PosPage header")
