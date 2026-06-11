#!/bin/bash
set -e
cd /home/moneroflow/testing/xmr-pay-hub-on-akash
echo "Building production bundle..."
npx vite build
echo "Build complete! Copying to container..."
rm -rf dist/*.log
docker cp dist/ test-app:/usr/share/nginx/html/
echo "Deployed to http://192.168.60.123:8090"
