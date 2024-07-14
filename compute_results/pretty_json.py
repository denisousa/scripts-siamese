import json

def read_json_and_format(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    
    json_formatted = json.dumps(json_data, indent=4, ensure_ascii=False)
    open(file_path,'w').write(json_formatted)

file_path = 'pretty_data.json'

read_json_and_format(file_path)
