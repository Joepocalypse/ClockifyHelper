from datetime import datetime
import pytz

class ClockifyTimeEntry():
    def __init__(self, incoming_time_entry, time_zone):
        self.id = incoming_time_entry['id']
        self.description = incoming_time_entry['description'].strip()
        self.tagIds = incoming_time_entry['tagIds']        
        self.userId = incoming_time_entry['userId']
        self.billable = incoming_time_entry['billable']
        self.taskId = incoming_time_entry['taskId']
        self.projectId = incoming_time_entry['projectId']
        self.workspaceId = incoming_time_entry['workspaceId']
        self.duration = incoming_time_entry['timeInterval']['duration']
        
        self.pytzTimezone = pytz.timezone(time_zone)
        
        self.start = incoming_time_entry['timeInterval']['start']
        self.formattedStart = datetime.strptime(self.start,'%Y-%m-%dT%H:%M:%S%z')
        self.startWithTimeZone = self.formattedStart.astimezone(self.pytzTimezone)
        self.readableStart = self.formattedStart.strftime('%m/%d/%Y %H:%M')

        self.end = incoming_time_entry['timeInterval']['end']
        self.formattedEnd = datetime.strptime(self.end,'%Y-%m-%dT%H:%M:%S%z')
        self.endWithTimeZone = self.formattedEnd.astimezone(self.pytzTimezone)       
        self.readableEnd = self.formattedEnd.strftime('%m/%d/%Y %H:%M')      

        self.timeZoneName = self.endWithTimeZone.tzname()


# {'id': '652801e2746a844165294be4', 
# 'description': 'Asana review/update', 
# 'tagIds': ['63969cc69b39be4a8aef9b1b'], 
# 'userId': '640742a0f2e6b64344c871fa', 
# 'billable': False, 
# 'taskId': '63efa255cf0b257026d87a2d', 
# 'projectId': '63988e3819e7630fd51fac2a', 
# 'workspaceId': '6396899a9b39be4a8aef565f', 
# 'timeInterval': {'start': '2023-10-12T14:00:00Z', 'end': '2023-10-12T14:30:00Z', 'duration': 'PT30M'}, 
# 'customFieldValues': [], 
# 'type': 'REGULAR', 
# 'kioskId': None, 
# 'hourlyRate': None, 
# 'costRate': None, 
# 'isLocked': False}