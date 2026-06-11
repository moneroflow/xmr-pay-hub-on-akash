# Agent Notes

## Core Rules
- Gary has gone now, he's been laid off, you're the new Lead Dev! Take the lead on everything don't wait for Gary
- Always generate **both** Monero (XMR) and TRON (USDT) payment links when creating a new payment.
- Label the first link as "Monero" with blue badge (`bg-blue-600`).
- Label the second link as "TRON (USDT)" with orange badge (`bg-orange-600`).
- Never show two links both labeled "Monero".
- When editing PaymentLinksPage.tsx, make changes in as few tool calls as possible to avoid rate limits.
- Prefer outputting full corrected code sections or clean diffs instead of many small patches.

## Tech Stack
- React + TypeScript
- Tailwind CSS for styling
- Quick deploy workflow documented
- Container info recorded (xmr-pay-hub)
- ...

## Workflow Preferences
- Plan first, then edit.
- If rate limited, pause and suggest manual changes.

## Deployment & Testing

**Active Testing Container:**
- Runs on port **8090**
- This is where all manual testing occurs
- Any code changes require rebuild to see effects

**Build Requirements:**
- Minimum flag: `--no-cache` (e.g., `npm run build --no-cache` or `npx vite build --no-cache`)
- Docker Compose rebuild: `docker-compose up -d --build`
- Never use cached builds when testing bug fixes or UI changes

**Quick Deploy Workflow:**
```bash
# 1. Build frontend
cd /home/moneroflow/testing/xmr-pay-hub-on-akash
npm run build --no-cache

# 2. Rebuild and restart container
docker-compose up -d --build

# 3. Verify on testing port
curl http://localhost:8090
# Or browser: http://localhost:8090
```

**Container Info:**
- Container name: `xmr-pay-hub`
- Service in docker-compose: `app`
- Maps to port 8090 (nginx listens on 80, docker maps to 8090)

**Project Paths:**
- **Active project:** `/home/moneroflow/testing/xmr-pay-hub-on-akash`
- **DEPRECATED - DO NOT USE:** 
  - `/home/node/moneroflow/workspace/moneroflow`
  - `/home/node/moneroflow/workspace/moneroflow/backend`
  - Container: `moneroflow-backend-1` (old, removed)
