import requests
import json
from datetime import date
from keywords import keywords
from clockify_project import ClockifyProject
from clockify_task import ClockifyTask
from clockify_time_entry import ClockifyTimeEntry
from clockify_tag import ClockifyTag

API_KEY = "<YOUR CLOCKIFY API KEY HERE>"
UPDATE_MARK = ' *'
today = date.today().strftime("%Y-%m-%dT00:00:00-04:00")

def call_clockify_api(url):
    """Used to call the Clockify API"""

    headers = {'x-api-key' : API_KEY}
    r =requests.get(url, headers=headers)
    return json.loads(r.content)

def call_clockify_time_entries_api(workspace_id, user_id):
    """Used to call the Clockify time entry api specifically"""

    url = 'https://api.clockify.me/api/v1/workspaces/{}/user/{}/time-entries'.format(workspace_id, user_id)
    headers = {'x-api-key': API_KEY}
    parameters  = {
        "start" : today,
        "page-size" : "100"
    }
    r = requests.get(url, headers=headers, params=parameters)
    return json.loads(r.content)

def print_api_call_results(results):
    """Prints the results of a Clockify API call in a readable way"""

    print(json.dumps(results, indent=4))

def get_time_entry(workspace_id, entry_id):
    """Retrieves a specific Clockify time entry"""

    this_time_entry_url = 'https://api.clockify.me/api/v1/workspaces/{}/time-entries/{}'.format(
        workspace_id, entry_id)
    this_time_entry = call_clockify_api(this_time_entry_url)
    return  this_time_entry

def update_time_entry (workspace_id, time_entry, project_obj, task_obj, tag_obj):
    """Updates a specific Clockify time entry"""

    if(task_obj is None or task_obj.id == ""):
        task_id = ""
    else:
        task_id = task_obj.id

    if(tag_obj is None or tag_obj.id == ""):
        tag_ids = []
    else:
        tag_ids = [tag_obj.id]

    if (time_entry.project_id == project_obj.id and time_entry.task_id == task_id and 
        time_entry.tag_ids == tag_ids) or time_entry.description.endswith(UPDATE_MARK):
        return None

    url = 'https://api.clockify.me/api/v1/workspaces/{}/time-entries/{}'.format(workspace_id,
                                                                                time_entry.id)
    headers = {'x-api-key': API_KEY, 'Content-Type': 'application/json'}
    data  = {
        "description" : time_entry.description + UPDATE_MARK,
        "start" : time_entry.start,
        "end": time_entry.end,
        "projectId": project_obj.id,
        "taskId": task_id,
        "tagIds": tag_ids
    }
    r = requests.put(url, headers=headers, data=json.dumps(data))
    return json.loads(r.content)

def evaluate_keywords(keywords, project_list, task_list, tag_list):
    """Evaluates the keywords file to find erroneous entries"""

    keywords_valid = True

    for keyword in keywords:
        # print ("Validating Keyword [{}]".format(keyword))
        current_project = keywords[keyword]['project']
        current_task = keywords[keyword]['task']
        current_tag = keywords[keyword]['tag']

        # Search project list for provided project name
        project_results = [project for project in project_list if project.name == current_project]

        if len(project_results) == 0:
            print("Invalid project [{}] for keyword [{}].".format(current_project, keyword))
            keywords_valid = False
        else:
            # Search task list for provided task name, taking parent project into account
            task_results = [task for task in task_list if (task.name == current_task or 
                                                           task.id is None) and
                                                           task.project_id == project_results[0].id]

            if len(task_results) == 0 and current_task != '':
                print("Task [{}] does not exist under project [{}] for keyword [{}].".format(
                    current_task, current_project, keyword))
                keywords_valid = False

            # Search tag list for provided tag name
            tag_results = [tag for tag in tag_list if tag.name == current_tag]
            if len(tag_results) == 0 and current_tag != '':
                print("Invalid tag [{}] for keyword [{}].".format(current_tag, keyword))
                keywords_valid = False

    return keywords_valid

def validate_search_results(results):
    """Checks search results and returns None if no results are present"""

    valid_result = None
    if len(results) > 0:
        valid_result = results[0]
    return valid_result

# ***** CURRENT USER *****
user_url = 'https://api.clockify.me/api/v1/user'
user_info = call_clockify_api(user_url)
workspace_id = user_info['activeWorkspace']
user_id = user_info['id']
user_timezone = user_info['settings']['timeZone']

print('Current User: {}, {} ({})'.format(user_info['name'], user_info['email'], user_timezone))

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
project_list = []
task_list = []

print('Loading projects and associated tasks...')
for project in projects_info:
    if project['archived'] == False and project['clientId'] == client_id:
        this_project = ClockifyProject(project)
        project_list.append(this_project)

        tasks_url = 'https://api.clockify.me/api/v1/workspaces/{}/projects/{}/tasks'.format(
            workspace_id, this_project.id)
        tasks_info = call_clockify_api(tasks_url)

        for task in tasks_info:
            task_list.append(ClockifyTask(task))

# ***** TAGS *****
tags_url = 'https://api.clockify.me/api/v1/workspaces/{}/tags'.format(workspace_id)
tags_info = call_clockify_api(tags_url)

print('Loading tags...')
tags_dictionary = {}
tag_list = []
for tag in tags_info:
    tags_dictionary[tag['id']] = tag['name']
    tag_list.append(ClockifyTag(tag))

# ***** TIME ENTRIES *****
time_entries_url = 'https://api.clockify.me/api/v1/workspaces/{}/user/{}/time-entries'.format(
    workspace_id, user_id)
time_entries_info = call_clockify_time_entries_api(workspace_id, user_id)

print('Loading time entries starting on {}...'.format(date.today().strftime("%m/%d/%Y")))

time_entry_dictionary = {}
time_entry_object_list = []
for time_entry in time_entries_info:
    time_entry_dictionary[time_entry['timeInterval']['start']] = time_entry
    time_entry_object_list.append(ClockifyTimeEntry(time_entry, user_timezone))

# Sort time entries by start datetime
time_entry_object_list.sort(key=lambda time_entry: time_entry.start)

keywords_valid = evaluate_keywords(keywords, project_list, task_list, tag_list)

if keywords_valid is True:
    # Process/evaluate/update time entries
    for time_entry in time_entry_object_list:
        MSG = ''
        new_project = ""
        new_task = {}
        new_tag = ""
        update_needed = False
        updates = 0

        time_entry_output = '\t{} to {} {}: {} '.format(time_entry.readable_start,
                                                        time_entry.readable_end,
                                                        time_entry.timezone_name,
                                                        time_entry.description)

        for keyword in keywords:
            if keyword.lower() in time_entry.description.lower() and updates == 0:
                entry_updated = False
                new_project = keywords[keyword]['project']
                new_task = keywords[keyword]['task']
                new_tag = keywords[keyword]['tag']

                new_project_obj = validate_search_results([project for project in project_list
                                                           if project.name == new_project])
                new_task_obj = validate_search_results([task for task in task_list if task.name ==
                                                        new_task and task.project_id ==
                                                        new_project_obj.id])
                new_tag_obj = validate_search_results([tag for tag in tag_list if tag.name ==
                                                       new_tag])

                update_results = update_time_entry(workspace_id, time_entry, new_project_obj,
                                                   new_task_obj, new_tag_obj)

                if update_results is None:
                    entry_updated = False
                elif update_results['id']:
                    MSG = '| *** Time Entry Updated for Keyword [{}] ***'.format(keyword)
                    updates += 1
                else:
                    print_api_call_results(update_results)

                final_time_entry = ClockifyTimeEntry(get_time_entry(workspace_id, time_entry.id),
                                                     user_timezone)
                final_project = validate_search_results([project for project
                                                         in project_list if project.id ==
                                                         final_time_entry.project_id])
                final_task = validate_search_results([task for task in task_list if task.id ==
                                                       final_time_entry.task_id])

                if final_task is None:
                    final_task_name = "No Task"
                else:
                    final_task_name = final_task.name

                if updates > 0:
                    break

        time_entry_output += '({} / {}) {}'.format(final_project.name, final_task_name, MSG)

        print(time_entry_output)
