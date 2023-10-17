"""Module to house the class below"""

from datetime import datetime
import pytz

class ClockifyTimeEntry():
    """Class representing a Clockify time entry"""

    def __init__(self,incoming_time_entry,time_zone):
        self.id = incoming_time_entry['id']
        self.description = incoming_time_entry['description'].strip()
        self.tag_ids = incoming_time_entry['tagIds']
        self.user_id = incoming_time_entry['userId']
        self.billable = incoming_time_entry['billable']
        self.task_id = incoming_time_entry['taskId']
        self.project_id = incoming_time_entry['projectId']
        self.workspace_id = incoming_time_entry['workspaceId']
        self.duration = incoming_time_entry['timeInterval']['duration']

        self.pytz_timezone = pytz.timezone(time_zone)

        self.start = incoming_time_entry['timeInterval']['start']
        self.formatted_start = datetime.strptime(self.start,'%Y-%m-%dT%H:%M:%S%z')
        self.start_with_timezone = self.formatted_start.astimezone(self.pytz_timezone)
        self.readable_start = self.formatted_start.strftime('%m/%d/%Y %H:%M')

        self.end = incoming_time_entry['timeInterval']['end']
        self.formatted_end = datetime.strptime(self.end,'%Y-%m-%dT%H:%M:%S%z')
        self.end_with_timezone = self.formatted_end.astimezone(self.pytz_timezone)
        self.readable_end = self.formatted_end.strftime('%m/%d/%Y %H:%M')

        self.timezone_name = self.end_with_timezone.tzname()


# {'id': '652801e2746a844165294be4',
# 'description': 'Asana review/update',
# 'tagIds': ['63969cc69b39be4a8aef9b1b'],
# 'userId': '640742a0f2e6b64344c871fa',
# 'billable': False,
# 'taskId': '63efa255cf0b257026d87a2d',
# 'projectId': '63988e3819e7630fd51fac2a',
# 'workspaceId': '6396899a9b39be4a8aef565f',
# 'timeInterval': {'start': '2023-10-12T14:00:00Z',
# 'end': '2023-10-12T14:30:00Z','duration': 'PT30M'},
# 'customFieldValues': [],
# 'type': 'REGULAR',
# 'kioskId': None,
# 'hourlyRate': None,
# 'costRate': None,
# 'isLocked': False}
