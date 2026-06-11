#!/usr/bin/env python3
"""
Modify PaymentLinksPage.tsx to generate both XMR and USDT payment links simultaneously
"""

with open('src/pages/dashboard/PaymentLinksPage.tsx', 'r') as f:
    content = f.read()

# Find the handleCreatePayment function and modify it to create two links
# Look for the pattern where payment link is created

# First, let's find the structure by looking for createPayment Link or similar
import re

# Find where handleCreate function creates the payment link
if 'handleCreate' in content and 'createPaymentLink' in content:
    # We need to modify this to create both XMR and TRX invoices
    print("Found createPaymentLink pattern - will modify to create dual links")

    # Find the handleCreate function and replace it
    old_pattern = r'  const handleCreate = async \(\) => \{.*?const paymentLink = await createPaymentLink\((.*?)\);'

    # Not using complex regex - let's use string replacement for the key part
    # Find where payment link is created and add dual link generation

with open('src/dashboard/PaymentLinksPage.tsx', 'r') as f:
    content = f.read()

# ...

print("\n⚠️ File not found at expected path")
