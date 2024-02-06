import json

my_dict = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# json_string = json.dumps(my_dict)

# print(json_string)

with open("json_file.json", "w") as json_file:
    json.dump(my_dict, json_file)

load = {
        "new_loads": [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"}
        ],
        "assign_loads": [
            {"product": "Laptop", "price": 1000},
            {"product": "Phone", "price": 500}
        ]
    }
