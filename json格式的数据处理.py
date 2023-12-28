import json

with open('response.txt', 'r', encoding='utf-8') as f:
    result = json.load(f)
print(type(result))
print(result['data'])
with open("result.txt", 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False,indent=4)