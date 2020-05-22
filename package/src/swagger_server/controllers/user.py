from os import environ as env

import requests

AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')

def _request_management_token():
  url = 'https://' + AUTH0_DOMAIN + '/oauth/token'
  payload = {
    'client_id': AUTH0_CLIENT_ID, 
    'client_secret': AUTH0_CLIENT_SECRET, 
    'audience': 'https://' + AUTH0_DOMAIN + '/api/v2/',
    'grant_type': 'client_credentials'
    }
  res = requests.post(url, json=payload)
  res.raise_for_status()
  data = res.json()
  return data.get('access_token')
  
def _update_user(user_id, body, token):
  data = {}
  for item in body:
    if item.get('field') == 'email':
      data['email_verified'] = False,
      data['verify_email'] = True
    data[item.get('field')] = item.get('value')

  url = 'https://' + AUTH0_DOMAIN + '/api/v2/users/' + user_id
  headers = {'Authorization': 'Bearer ' + token}
  res = requests.patch(url, json=data, headers=headers)
  res.raise_for_status()
  return res.json()
