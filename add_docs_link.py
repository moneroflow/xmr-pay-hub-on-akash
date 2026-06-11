#!/usr/bin/env python3
"""
Add Help/Docs link to sidebar and Overview page
"""

import re

# Read the file
with open('src/components/DashboardLayout.tsx', 'r') as f:
    content = f.read()

# 1. Add Book import to lucide-react
old_imports = '''import {
  Sidebar, SidebarContent, SidebarGroup, SidebarGroupContent, SidebarGroupLabel,
  SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarProvider, SidebarTrigger, useSidebar
} from '@/components/ui/sidebar';
import { LayoutDashboard, FileText, Clock, Settings, LogOut, RefreshCw, MonitorSmartphone, BarChart3, Link2, Plug, Globe, Paintbrush, Landmark, Gift, Server, Shield, HardDrive, Users, Sun, Moon, Zap } from 'lucide-react';'''

new_imports = '''import {
  Sidebar, SidebarContent, SidebarGroup, SidebarGroupContent, SidebarGroupLabel,
  SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarProvider, SidebarTrigger, useSidebar
} from '@/components/ui/sidebar';
import { LayoutDashboard, FileText, Clock, Settings, LogOut, RefreshCw, MonitorSmartphone, BarChart3, Link2, Plug, Globe, Paintbrush, Landmark, Gift, Server, Shield, HardDrive, Users, Sun, Moon, Zap, Book, ExternalLink } from 'lucide-react';'''

# 2. Add Help/Docs to configNav - below Settings, before LogOut
old_config_nav = '''const configNav = [
  { title: 'Users', url: '/dashboard/users', icon: Users },
  { title: 'Localization', url: '/dashboard/localization', icon: Globe },
  { title: 'White-Label', url: '/dashboard/white-label', icon: Paintbrush },
  { title: 'Backups', url: '/dashboard/backups', icon: HardDrive },
  { title: 'Settings', url: '/dashboard/settings', icon: Settings },
];'''

new_config_nav = '''const configNav = [
  { title: 'Users', url: '/dashboard/users', icon: Users },
  { title: 'Localization', url: '/dashboard/localization', icon: Globe },
  { title: 'White-Label', url: '/dashboard/white-label', icon: Paintbrush },
  { title: 'Backups', url: '/dashboard/backups', icon: HardDrive },
  { title: 'Settings', url: '/dashboard/settings', icon: Settings },
  { title: 'Help/Docs', url: 'https://docs.moneroflow.com/wiki.html', icon: Book, external: true },
];'''

# 3. Update renderNav to handle external links with ExternalLink icon
old_render_nav = '''  const renderNav = (items: typeof mainNav) => (
    <SidebarMenu>
      {items.map(item => (
        <SidebarMenuItem key={item.title}>
          <SidebarMenuButton asChild>
            <NavLink
              to={item.url}
              end={item.url === '/dashboard'}
              onClick={closeMobile}
              className="flex items-center gap-3 px-3 py-2 rounded-lg text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors"
              activeClassName="bg-sidebar-accent text-primary font-medium"
            >
              <item.icon className="w-4 h-4 shrink-0" />
              {!collapsed && <span>{item.title}</span>}
            </NavLink>
          </SidebarMenuButton>
        </SidebarMenuItem>
      ))}
    </SidebarMenu>
  );'''

new_render_nav = '''  const renderNav = (items: typeof any[]) => (
    <SidebarMenu>
      {items.map(item => (
        <SidebarMenuItem key={item.title}>
          {item.external ? (
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={closeMobile}
              className="flex items-center gap-3 px-3 py-2 rounded-lg text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:underline transition-colors w-full"
            >
              <item.icon className="w-4 h-4 shrink-0" />
              {!collapsed && <span>{item.title}</span>}
              {!collapsed && <ExternalLink className="w-3 h-3 opacity-60" />}
            </a>
          ) : (
            <SidebarMenuButton asChild>
              <NavLink
                to={item.url}
                end={item.url === '/dashboard'}
                onClick={closeMobile}
                className="flex items-center gap-3 px-3 py-2 rounded-lg text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors"
                activeClassName="bg-sidebar-accent text-primary font-medium"
              >
                <item.icon className="w-4 h-4 shrink-0" />
                {!collapsed && <span>{item.title}</span>}
              </NavLink>
            </SidebarMenuButton>
          )}
        </SidebarMenuItem>
      ))}
    </SidebarMenu>
  );'''

# Apply replacements
if all(old in content for old in [old_imports, old_config_nav, old_render_nav]):
    content = content.replace(old_imports, new_imports)
    content = content.replace(old_config_nav, new_config_nav)
    content = content.replace(old_render_nav, new_render_nav)
    print("✅ Sidebar Help/Docs link added!")
else:
    print("❌ Some patterns not found")
    for i, old in enumerate([old_imports, old_config_nav, old_render_nav]):
        print(f"{'✓' if old in content else '✗'} Pattern {i+1} found")

# Write the file
with open('src/components/DashboardLayout.tsx', 'w') as f:
    f.write(content)

print("\n🎯 Now updating OverviewPage...")
print("Previewing changes needed for OverviewPage Help icon")
