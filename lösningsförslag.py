NAME = 0
AGE = 1
SIZE = 2

def input_person(retries = 3):
    try:
        name, age, size = input(f'name, age, shoesize: ').split(",")
        return name.strip().lower(), age.strip(), size.strip()
    except ValueError:
        if (retries):
            return input_person(retries - 1)
        raise

def search_person(retries = 3):
    try:
        search_type, search_text = input(f'Enter [type text]: ').split(" ")
        return search_type.strip().lower(), search_text.strip().lower()
    except ValueError:
        if (retries):
            return search_person(retries - 1)
        raise

lookup_dict = {"name": {}, "age": {}, "size": {}}
persons = {}

name_0, age_0, size_0 = input_person() #("olle", "14", "44")
persons.update({0: (name_0, age_0, size_0)})

name_1, age_1, size_1 = input_person() #("pelle", "20", "48")
persons.update({1: (name_1, age_1, size_1)})

name_2, age_2, size_2 = input_person() #("lisa", "33", "38")
persons.update({2: (name_2, age_2, size_2)})

# Contruct lookup dict
lookup_dict["name"] = {name_0: 0, name_1: 1, name_2: 2}
lookup_dict["age"] = {age_0: 0, age_1:1, age_2:2}
lookup_dict["size"] = {size_0: 0, size_1:1, size_2:2}

# Programmet ska sedan skriva ut namn och skostorlek på den person som är 
# äldst samt namn och ålder på den som har medianskostorlek.

# Find oldest person
max_age = max(lookup_dict["age"], key=lambda x: int(x))
idx_oldest_person = lookup_dict["age"][max_age]
oldest_person = persons[idx_oldest_person]

format_oldest_person = (
    f'Oldest person: {oldest_person[NAME].capitalize()}'
    f' and with size: {oldest_person[SIZE]}'
)
print(format_oldest_person)

# Resolve median person
idx_median, reminder = divmod(len(lookup_dict["size"]), 2)
assert(reminder == 1)

# find median shoesize person
median_size = sorted(lookup_dict["size"], key=lambda x: int(x))[idx_median]
idx_median_shoesize = lookup_dict["size"][median_size]
median_shoesize_person = persons[idx_median_shoesize]

format_median_print = (
    f'Median size person: {median_shoesize_person[NAME].capitalize()}'
    f' and age: {median_shoesize_person[AGE]}'
)
print(format_median_print)

# Efter det ska användaren kunna söka efter personer genom att mata in en av
# de tre datatyperna. Om programmet hittar någon som matchar ska dennes
# kompletta uppgifter skrivas ut.

search_type, search_text = search_person()
person_idx = lookup_dict.get(search_type, {}).get(search_text)
search_result = persons.get(person_idx, ("No match","No match","No match"))

format_search_result = (
    f'name: {search_result[NAME].capitalize()}\n'
    f'age: {search_result[AGE]}\n'
    f'size: {search_result[SIZE]}'
)
print(format_search_result)