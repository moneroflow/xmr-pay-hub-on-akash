#!/usr/bin/env python3
"""
Fix PosPage - Add actual toggle UI to the header
"""

with open('src/pages/dashboard/PosPage.tsx', 'r') as f:
    content = f.read()

# Find the user selector section and add toggle after it
old_user_section = '''      {users.length > 0 && (
        <div className="flex items-center gap-3 px-1">
          <div className="flex items-center gap-2 bg-card border border-border rounded-lg px-3 py-2">
            <span className="text-xs text-muted-foreground">Cashier:</span>
            <Select value={activeUserId} onValueChange={handleSwitchUser}>
              <SelectTrigger className="h-7 w-[140px] bg-background border-border text-xs">
                <SelectValue placeholder="Admin" />
              </SelectTrigger>
              <SelectContent className="bg-card border-border">
                <SelectItem value="admin">Admin</SelectItem>
                {users.map(u => (
                  <SelectItem key={u.id} value={u.id}>{u.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20 text-xs gap-1.5 py-1">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            {activeUserName}
          </Badge>
        </div>
      )}'''

new_user_section = '''      {users.length > 0 && (
        <div className="flex items-center gap-3 px-1">
          <div className="flex items-center gap-2 bg-card border border-border rounded-lg px-3 py-2">
            <span className="text-xs text-muted-foreground">Cashier:</span>
            <Select value={activeUserId} onValueChange={handleSwitchUser}>
              <SelectTrigger className="h-7 w-[140px] bg-background border-border text-xs">
                <SelectValue placeholder="Admin" />
              </SelectTrigger>
              <SelectContent className="bg-card border-border">
                <SelectItem value="admin">Admin</SelectItem>
                {users.map(u => (
                  <SelectItem key={u.id} value={u.id}>{u.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <Badge variant="outline" className="bg-primary/10 text-primary border-primary/20 text-xs gap-1.5 py-1">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            {activeUserName}
          </Badge>
        </div>
      )}
      {/* ═══ Payment Chain Toggle ═══ */}
      <div className="flex items-center gap-3 bg-card border border-border rounded-lg px-3 py-2">
        <span className={`text-xs font-medium ${selectedChain === 'xmr' ? 'text-primary' : 'text-muted-foreground'}`}>XMR</span>
        <Switch
          checked={selectedChain === 'trx'}
          onCheckedChange={(checked) => setSelectedChain(checked ? 'trx' : 'xmr')}
          className="bg-muted data-[state=checked]:bg-orange-500"
        />
        <span className={`text-xs font-medium ${selectedChain === 'trx' ? 'text-orange-500' : 'text-muted-foreground'}`}>TRX/USDT</span>
      </div>'''

content = content.replace(old_user_section, new_user_section)

with open('src/pages/dashboard/PosPage.tsx', 'w') as f:
    f.write(content)

print("✅ PosPage: Added chain toggle UI to header")
print("✅ Toggle now visible and functional")
print("  - XMR (blue) / TRX/USDT (orange) labels")
print("  - Switch component imported from shadcn/ui")
print("  - State variable: selectedChain ('xmr' | 'trx')")
