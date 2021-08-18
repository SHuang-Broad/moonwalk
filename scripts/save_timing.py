#!/usr/bin/env python3

import urllib.request    

serverl_url = ''
execution_uuid = ''
api=f'{server_url}/api/workflows/v1/{execution_uuid}/timing'

save_to_file = ''

urllib.request.urlretrieve(api, save_to_file)
