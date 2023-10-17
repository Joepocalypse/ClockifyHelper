class ClockifyTag():
    def __init__(self, incoming_tag):
        self.id = incoming_tag['id']
        self.name = incoming_tag['name']
        self.workspace_id = incoming_tag['workspaceId']
        self.archived = incoming_tag['archived']  

#{'id': '63968a2319e7630fd50eb214', 
# 'name': 'mobile', 
# 'workspaceId': '6396899a9b39be4a8aef565f', 
# 'archived': True}
