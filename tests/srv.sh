#!/bin/bash
curl -s -o /dev/null localhost:8765/index.html || (cd /home/claude/pinnacle/public && nohup python3 -m http.server 8765 >/dev/null 2>&1 &) ; sleep 1
