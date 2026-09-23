#!/bin/sh
# Serve the complete HTML school site on 8080 for live preview + download.
if curl -sf http://127.0.0.1:8080/ >/dev/null 2>&1; then
  exit 0
fi
cd /workspace/public
python3 -m http.server 8080 --bind 0.0.0.0 >/tmp/madrase-http.log 2>&1 &
sleep 0.4
exit 0
