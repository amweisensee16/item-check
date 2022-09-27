# item-check
This tool can be used to check for items in dcTrack. 
If the item name is not found, the tool returns FALSE. If the item is found, the tool returns location(s) where the item name was found.

# How To
1. Download the python code
2. Make it run at boot (add to crontab `@reboot         <user>    <path>/item-check/item_check.sh`)
3. The content of `item_check.sh` should be something like:
```bash
#!/bin/bash
PATH=/usr/local/bin
/usr/bin/tmux new-session -d -s ENTER
/usr/bin/tmux detach -s ENTER
sleep 3
/usr/bin/tmux send-keys -t 0 "streamlit run <path>/item-check/item_check.py --server.address <ip> --server.port <port> --server.headless true" ENTER
echo "$(date) ${1} RESTARTED NODE"
```
4. Go to the site: `http://<ip>:<port>`, be sure to use the IP and port that was set in the script.
5. Follow the on-screen instructions
