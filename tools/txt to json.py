import json
import os
dict= {
    "names": []
}
with open('lnames.txt', 'r') as f:
    t = f.read()
    names = t.split('\n')
    dict['names'] = names

print(dict['names'])
with open('lnames.json', 'w') as f:
    json.dump(dict, f, indent=4)