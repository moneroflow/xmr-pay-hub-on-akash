# USDT/TRON Integration - QUICK TEST GUIDE

##Tonight's Fix Summary
✅ Fixed POS theme reverting when navigating back from Invoice page
✅ USDT now shows as "11.00 USDT" not "A$11" 
✅ InvoicePage has full TRX/USDT chain support (orange theme, TRON QR codes)

## Quick Test Steps (Morning)

1. **Build & Deploy:**
   ```bash
   cd /home/moneroflow/testing/xmr-pay-hub-on-akash
   npx vite build
   docker exec test-app rm -rf /usr/share/nginx/html/*
   docker cp dist/ test-app:/usr/share/nginx/html/
   ```

2. **Test Navigation (The Critical Bug):**
   - Open http://192.168.60.123:8090/dashboard/pos
   - Click "TRX" (chain selector)
   - Verify: Orange theme activates
   - Click "Create Invoice"
   - Click invoice link → Opens InvoicePage
   - Verify: Still orange theme
   - **Click back to POS**
   - **Verify: ORANGE THEME PERSISTS** (this was the bug!)

3. **Test USDT Display:**
   - On InvoicePage: shows "11.00 USDT" (not "A$11")
   - QR code is TRX scan link (not monero:)
   - Explorer links go to tronscan.org

## If Still Purple/XMR Theme When Back:
Check browser console:
```javascript
localStorage.getItem('pos-chain')           // Should be 'trx'
localStorage.getItem('mf-previous-theme')   // Should be 'dark'
```

Clear to reset:
```javascript
localStorage.clear()
location.reload()
```

## Next Session Goals
1. Test current build
2. If fixed: Add Send dialog multi-chain support
3. Add Overview page dual-chain balance display
