#Strings are immutable
content = "vampire offbeat"
slice_vampire = content[0:8]
last_value = content[-1]
len(content)

num_list = "8375879"
num_list[:]
num_list[3:]
num_list[:5]
num_list[0:7:2] #one number hopping

content.lower()
content.upper()
content.strip() #removes leading and trailing spaces
print(content.replace("vampire", "kook"))

new_cont = "vampire, offbeat, kjsf, kdf"
print(new_cont.split(", "))
print(content.find("vampire"))
content.count("vampire")

chai_type = "Masala"
quantity = 2
print("The chai type is {} and the quantity is {}".format(chai_type, quantity))

#list to Strings
varity = ["vampire", "offbeat", "kjsf", "kdf"]
print(" ".join(varity))

quote = "He said , \"I m Perfect\" "

path = r"Masala\nchai"

# for loop

varity = ["vampire", "offbeat", "kjsf", "kdf"]

for var in varity:
    print(var)

if "vampire" in varity:
    print("Yes")

# List 
varity.pop()
varity.remove("kjsf")
varity.insert(1, "new")

# Comprehensive List 
squared_num = [x**2 for x in range(10)]

#Dictionary
sample_dict = {"key1": "value1", "key2": "value2"}
for key , value in sample_dict.items():
    print(key, value)

if "key1" in sample_dict:
    print("Yes")

sample_dict["key3"] = "value3"
sample_dict["key4"] = "value4"
sample_dict.pop("key1")

#tuple

sample_tuple = (1, 2, 3, 4, 5)
sample_tuple[0]


# mutable 
# lists, dictionaries, and sets.

# immutable 
# tuples, strings, and numbers.
