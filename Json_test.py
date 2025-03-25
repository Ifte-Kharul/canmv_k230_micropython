import ujson  # MicroPython's JSON module

# Sample JSON data as a string
json_str = '''
{
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "skills": ["Python", "C++", "MicroPython"],
    "active": true
}
'''

# Parse JSON string
data = ujson.loads(json_str)

# Access values
print("Name:", data["name"])
print("Age:", data["age"])
print("City:", data["city"])
print("Skills:", ", ".join(data["skills"]))
print("Active:", "Yes" if data["active"] else "No")

# Modify data
data["age"] += 1  # Increment age
data["skills"].append("Embedded C")  # Add new skill

# Convert back to JSON string
updated_json_str = ujson.dumps(data)
print("\nUpdated JSON:", updated_json_str)
