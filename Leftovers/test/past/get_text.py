# -*- coding: utf-8 -*-
'''
Create Date: 2023/07/26
Author: @1chooo(Hugo ChunHo Lin)
Version: v0.0.2
'''

import json

with open('./ai-event.log', 'r') as f:
    content = f.read().split()
    f.close()

# print(len(content))

print(content[0])

data = json.loads(content[0])

json_formatted_str = json.dumps(data, indent=2)

print(json_formatted_str)

print(data.get('events')[0].get('message'))