import json

with open('../out.json') as f:
    data = json.load(f)
    is_like_zero_lst = []
    for structure in data:
        is_like_zero_lst.append(structure['is_like_zero'])
    print(is_like_zero_lst)
