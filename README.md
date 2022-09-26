# item-check
This tool can be used to check for items in dcTrack. 
If the item name is not found, the tool returns FALSE. If the item is found, the tool returns location(s) where the item name was found.

# How To
1. Download the python code
2. Make it run at boot (add to crontab `@reboot streamlit run item_check.py --server.port 8080`)
3. Go to the site: http<ip>:8080
4. Follow the on-screen instructions
