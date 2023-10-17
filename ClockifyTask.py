class ClockifyTask():
    def __init__(self, incoming_task):
        self.id = incoming_task['id']
        self.name = incoming_task['name']
        self.project_id = incoming_task['projectId']
        self.billable = incoming_task['billable']
        self.status = incoming_task['status']
        

# {'id': '63f0f8091a3ab13ae6f9f367',
# 'name': 'Huddle',
# 'projectId': '63969db319e7630fd50ef85c',
# 'assigneeIds': [],
# 'assigneeId': None,
# 'userGroupIds': [],
# 'estimate': 'PT0S',
# 'status': 'ACTIVE',
# 'budgetEstimate': None,
# 'duration': 'PT2157H25M41S',
# 'billable': True,
# 'hourlyRate': None,
# 'costRate': None}
