import json

with open(r"C:\Users\black\Downloads\handwrittencorrection-ba23c2547e50.json") as f:
    key_data = json.load(f)

key_string = json.dumps(key_data)
print(key_string)  # Copy this