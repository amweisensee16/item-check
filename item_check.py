from unittest import result
import requests
import pandas
import json
import streamlit as st
from io import BytesIO

# Disable the warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# For debugging in vscode
debug = False
if debug:
    st.write('Debug mode on, waiting for connection from remote debugger')
    import ptvsd
    ptvsd.enable_attach(address=('localhost', 5678))
    ptvsd.wait_for_attach()

def get_locations():
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.get(f'https://{host}/api/v1/locations', 
                      verify=False,
                      auth=(username, password),
                      headers=headers
                    )
    locations = [location['id'] for location in r.json()['locations']]
    return locations

def find_item(item_name, progress_window=False, percent_complete=False):
    
    if progress_window and percent_complete:
        update_progress_window(percent=percent_complete, window=progress_window)
    
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        'columns':[
            {'name':'tiName','filter':{'eq':item_name}}
        ],
        'selectedColumns':[
            {'name':'tiName'},
            {'name':'cmbLocation'}
        ]
    }
    r = requests.post(f'https://{host}/api/v2/quicksearch/items?pageSize=0', 
                      data=json.dumps(body), 
                      verify=False,
                      auth=(username, password),
                      headers=headers
                    )
    if r.status_code == 400:
        return False
#    result_len = r.json()['count']
    results = r.json()['searchResults']['items']
#    page=0
    exact_match = [item['cmbLocation'] for item in results if item['tiName'] == item_name]
    if len(exact_match) > 0:
        return exact_match[0]
    else:
        return False

def st_main_input_window():
    st.write("""
    # Item checker
    This is the Item Checker tool, please make your selections and we'll try to find your items in dcTrack!
    """)
    options = {}
    options['host'] = st.text_input('dctrack host/ip', 
                                    key='host',
                                    )
    options['username'] = st.text_input('username', 
                                        key='username',
                                        value='admin',
                                        )
    options['password'] = st.text_input('password', 
                                        key='password', 
                                        type='password', 
                                        value=password,
                                        )
    options['uploaded_file'] = st.file_uploader(label='incoming file',
                                                type=['xlsx','csv'],
                                                key='upload_file',
                                                )
    return options

def st_get_name_col():
    selection = st.selectbox('Select the field which contains names to look up',
                 items.columns,
                 )
    if st.button(f'Use {selection}'):
        return selection

if __name__ == '__main__':
    username = 'admin'
    password = 'sunbird'

    user_input = st_main_input_window()
    if '' not in user_input.values() and None not in user_input.values():
        file = user_input['uploaded_file']
        if file.name.endswith('.xlsx'):
            items = pandas.read_excel(file)
        elif file.name.endswith('.csv'):
            items = pandas.read_csv(file)
        else:
            st.error('File type must be xlsx or csv')

        host = user_input['host']
        username = user_input['username']
        password = user_input['password']
        name_column = st_get_name_col()
        
        if name_column:
            locations = get_locations()
            lookup_items = items[name_column]
            results = []
            found = 0
            not_found = 0
            loading = st.progress(0)
            loading_message = st.text(f'Found: {found} Not Found: {not_found}')
            for count, item in enumerate(lookup_items):
                percent_complete = (count + 1) / len(lookup_items)
                loading_message.text(f'Found: {found} Not Found: {not_found}')
                loading.progress(percent_complete)
                search_result = find_item(item)
                if search_result:
                    found+=1
                else:
                    not_found+=1
                results.append({'Name': item, 'Result': search_result})

            output = pandas.DataFrame(results)

            old_file = file.name.split('\\')[-1].split('.')[0]
            new_file_name = f'{old_file}-results.xlsx'
            new_file = BytesIO()
            output.to_excel(new_file, index=False)
            st.success(f'Done! The file was saved as {new_file_name}')
            st.download_button(
                label="Download results",
                data=new_file.getvalue(),
                file_name=new_file_name,
                mime="application/vnd.ms-excel"
            )