# item-check
This tool can be used to check for items in dcTrack. 
If the item name is not found, the tool returns FALSE. If the item is found, the tool returns location(s) where the item name was found.

# How To
1. Download the latest release from the releases page.
2. Launch `item-checker.exe` application.
3. Provide the IP address (or hostname) of the dcTrack you will be performing lookup on.
4. The pre-filled credentials are dcTrack's default (`admin`:`sunbird`). Change these if necessary.
5. Select the sheet which contains device names. 
    - the sheet must be XLSX or CSV format
    - if XLSX, only the first sheet (far left tab) in the workbook will be read.
    - all item names must be in the same column 
    - the first row must be column names.
6. Press `OK`.
7. On the next popup, select the column name which contains item names.
8. When the tool is done looking up items, a result file is created.
    - The result file is created in the same folder the application is run from.
    - titled `[input file]-result.xlsx`
    - XLSX format

