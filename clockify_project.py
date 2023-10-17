"""Module to house the class below"""

class ClockifyProject():
    """Class representing a Clockify project"""

    def __init__(self,incoming_project):
        self.id = incoming_project['id']
        self.name = incoming_project['name']
        self.workspace_id = incoming_project['workspaceId']
        self.archived = incoming_project['archived']
        self.client_id = incoming_project['clientId']


# {'id': '63969d3619e7630fd50ef689',
# 'name': 'Cap Markets',
# 'hourlyRate': None,
# 'clientId': '63969d330e063d4b898a1446',
# 'workspaceId': '6396899a9b39be4a8aef565f',
# 'billable': True,
# 'memberships':
# [# {'userId': '6396899a9b39be4a8aef565e','hourlyRate': None,'costRate': None,
# 'targetId': '63969d3619e7630fd50ef689','membershipType': 'PROJECT','membershipStatus': 'ACTIVE'}],
# 'color': '#4CAF50',
# 'estimate': {'estimate': 'PT0S','type': 'AUTO'},
# 'archived': True,
# 'duration': 'PT0S',
# 'clientName': 'Non-Profits',
# 'note': '',
# 'costRate': None,
# 'timeEstimate': {'estimate': 'PT0S','type': 'AUTO','resetOption': None,'active': False,
# 'includeNonBillable': True},
# 'budgetEstimate': None,'template': False,'public': True},
