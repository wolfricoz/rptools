import json
import os
dict= {
    "names": []
}
with open('new 4.txt', 'r') as f:
    t = f.read()
    names = t.split('\n')
    dict['names'] = names

print(dict['names'])
with open('fnames.json', 'w') as f:
    json.dump(dict, f, indent=4)