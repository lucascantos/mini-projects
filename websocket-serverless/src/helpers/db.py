from src.helpers import s3
def clients_connected (client_id, action):
    
    try:
        client_data = s3.s3_download()
    except:
        client_data = {
            'connected': []
        }

    client_list = client_data['connected']
    
    action = action.upper()
    if action == "ADD":
        client_list.append(client_id)
    elif action == 'REMOVE':
        client_list.remove(client_id)
    else:
        print("action must be 'add' or 'remove' ")

    s3.s3_upload(client_data)
