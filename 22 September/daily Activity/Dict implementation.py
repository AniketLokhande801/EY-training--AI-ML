dict1={"name":"aniket","age":22,"city":"bangalore"}
print(dict1)
print(dict1["name"])
print(dict1["age"])
print(dict1["city"])

# using get
print("using .get()",dict1.get("name"))
print("using .get()",dict1.get("age"))
print("using .get()",dict1.get("city"))
print("before",dict1)
dict1["grade"]="A+"
dict1["age"]="18"

print("after",dict1)

# dict1.pop("city")
# print(dict1)
# del dict1["grade"]
# print(dict1)

print(dict1.items())

emp={
    "id":1,
    "name":"aniket",
    "age":22,
    "skills":["python","Sql","C++","Java"],
    "grade":"A+"
}
print(emp["skills"][0])