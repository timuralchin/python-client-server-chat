import json

with open('client-sever/server/db/users.json', 'r') as json_file: 
            data = json.load(json_file)   
users = data['users']
usernames = []
for user in users: 
    usernames.append(user['username'])
print(usernames)
if 'sdf' in usernames:
    print('loh')