import json
student={
    "name":"aniket",
    "age":22,
    "course":["AI","ML"],
    "marks":{"AI":88,"ML":90},


}
with open("st.json",'w') as f:
    json.dump(student,f,indent=4)

with open("st.json",'r') as f:
    json_student = json.load(f)

print(json_student["name"])
