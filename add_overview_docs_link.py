#!/usr/bin/env python3
"""
Add docs link to Help Info icon on OverviewPage
"""

import re

# Read the file
with open('src/pages/dashboard/OverviewPage.tsx', 'r') as f:
    content = f.read()

# Update the Help section - make the Info icon clickable to docs
old_help_section = '''          <div className="flex items-center gap-3 bg-card/50 px-3 py-1.5 rounded-lg border border-border/50">
            <Info className="w-3.5 h-3.5 text-primary" />
            <span className="text-xs text-muted-foreground font-medium">Help</span>
            <Switch checked={helpEnabled} onCheckedChange={setHelpEnabled} size="sm" />
          </div>'''

new_help_section = '''          <div className="flex items-center gap-3 bg-card/50 px-3 py-1.5 rounded-lg border border-border/50">
            <button
              onClick={() => window.open('https://docs.moneroflow.com/wiki.html', '_blank')}
              className="flex items-center justify-center hover:opacity-70 transition-opacity"
              title="Open documentation"
            >
              <Info className="w-3.5 h-3.5 text-primary" />
            </button>
            <span className="text-xs text-muted-foreground font-medium">Help</span>
            <Switch checked={helpEnabled} onCheckedChange={setHelpEnabled} size="sm" />
          </div>'''

if old_help_section in content:
    content = content.replace(old_help_section, new_help_section)
    print("✅ OverviewPage.Help Info icon now links to docs!")
else:
    print("❌ Help section pattern not found")
    # Find similar patterns
    matches = re.findall(r'<Info.*?Help.*?Switch.*?\/>', content, re.DOTALL)
    if matches:
        print(f"Found {len(matches)} Help section patterns")

# Write the file
with open('src/pages/dashboard/OverviewPage.tsx', 'w') as f:
    f.write(content)

print("\n✅ Both updates complete!")
print("- Sidebar: Help/Docs link with external icon")
print("- Overview: Info icon links to docs")
