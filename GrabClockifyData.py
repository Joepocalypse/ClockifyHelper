import requests
import json
from datetime import date, datetime, tzinfo, timezone, timedelta
import pytz
from Keywords import keywords

api_key = "ZWEyZGFkY2UtZjYwZC00ZGNjLWEzZjQtNWZmZDU0Mzk4NTky"
today =date.today().strftime("%Y-%m-%dT00:00:00-04:00")
def call_clockify_api(url):
    headers = {'x-api-key' : api_key}
    r =requests.get(url, headers=headers)
    return json.loads(r.content)

def call_clockify_time_entries_api(workspace_id, user_id):
    url = 'https://api.clockify.me/api/v1/workspaces/{}/user/{}/time-entries'.format(workspace_id, user_id)
    headers = {'x-api-key': api_key}
    parameters  = {
        "start" : today,
        "page-size" : "100"
    }
    r = requests.get(url, headers=headers, params=parameters)
    return json.loads(r.content)

def print_api_call_results(results):
    print(json.dumps(results, indent=4))
def get_time_entry(workspace_id, entry_id):
    this_time_entry_url = 'https://api.clockify.me/api/v1/workspaces/{}/time-entries/{}'.format(workspace_id, entry_id)
    this_time_entry = call_clockify_api(this_time_entry_url)
    return  this_time_entry


# ***** USER *****
user_url = 'https://api.clockify.me/api/v1/user'
user_info = call_clockify_api(user_url)
workspace_id = user_info['activeWorkspace']
user_id = user_info['id']

print('Active User: {} ({})'.format(user_info['name'], user_info['email']))

# ***** CLIENTS *****
clients_url = 'https://api.clockify.me/api/v1/workspaces/{}/clients'.format(workspace_id)
clients_info = call_clockify_api(clients_url)

client_id = ''

print('Loading clients...')
for client in clients_info:
    # print('\t {}'.format(client['name']))
    if client['name'] == 'HiveFS':
        client_id = client['id']

# ***** PROJECTS & TASKS *****
projects_url = 'https://api.clockify.me/api/v1/workspaces/{}/projects'.format(workspace_id)
projects_info = call_clockify_api(projects_url)

project_id = ''
projects_dictionary = {}
tasks_dictionary = {}

print('Loading projects and associated tasks...')
for project in projects_info:
    
    # if project['archived'] == False and project['clientId'] == client_id:
    if project['clientId'] == client_id:
        project_id = project['id']
        projects_dictionary[project['id']] = project['name']
        tasks_url = 'https://api.clockify.me/api/v1/workspaces/{}/projects/{}/tasks'.format(workspace_id, project_id)
        tasks_info = call_clockify_api(tasks_url)

        for task in tasks_info:
            tasks_dictionary[task['id']] = task['name']            
            print("{},{},{},{},{},{},".format(project['name'], project['id'], project['archived'], task['name'], task['id'], task['status']))

# ***** TAGS *****
tags_url = 'https://api.clockify.me/api/v1/workspaces/{}/tags'.format(workspace_id)
tags_info = call_clockify_api(tags_url)

print('Loading tags...')
tags_dictionary = {}
for tag in tags_info:
    tags_dictionary[tag['id']] = tag['name']
