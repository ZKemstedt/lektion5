import typing as t

# GUIDELINES
# avoid loops
# avoid if

# REQUIREMENTS
# 1. not-case sensitive
# 2. accept and track user input for 3 people's name, age and shoesize
# 3. print name and shoesize of the oldest registered person, print name
#    and age of the person with the median shoesize
# 4. after this the user should be able to search for someone by inputing
# 	 one of the three datatypes as well as it's value. If the program finds
# 	 someone matching any value it should print all of it's associated data.


# toggles manual data entry, search (#4) is always manual
DEV_MODE = True


# Global helper functions

def input_person(retries: int = 3) -> t.Tuple[str, str, str]:
    """Helper function to create user data."""
    try:
        name, age, size = input(
            'name, age, shoesize\n>> '
            ).lower().split(',')
        return name.strip(), age.strip(), size.strip()
    except ValueError:
        if retries:
            return input_person(retries - 1)
        raise


def input_search(retries: int = 3) -> t.Tuple[str, str]:
    """Helper function to create search requests."""
    try:
        category, value = input(
            '[name|age|shoesize],[search_value]\n>> '
            ).lower().split(',')
        return category.strip(), value.strip()
    except ValueError:
        if retries:
            return input_search(retries - 1)
        raise


###############################################################################
#   uppgift B
#   Solution 1
#   Using one primary list of all data, and list-slicing for most operations
###############################################################################

people = []
offset = {
    'name': 0,
    'age': 1,
    'shoesize': 2
}
step = len(offset)  # step = size of each set of data

if not DEV_MODE:
    people += input_person()
    people += input_person()
    people += input_person()
else:
    people += ['pelle', '15', '55']
    people += ['martin', '13', '25']
    people += ['rasmus', '17', '35']


# uppgift B ~ 3.1
#
# Objective: Find the oldest person and print their name and shoesize.
#
# Methodology:
# 1. Create a list-slice `targets` from `people`, containing every `step`
#    value, starting from the value `offset[seek]`.
#    In this case, it's all the ages registered.
# 2. In `targets`, get the index of the max value and multiply it by `step`.
#    In max(), lambda is used for converting the values to int.
#    the index is assigned to `cur` and it points to the first value of the
#    'set of data' which represents the oldest person.
# 3  print the findings. `people[cur]` (always) gives you a name,
#    so `people[cur+1]` gives age and `people[cur+2]` gives shoesize.

seek = 'age'
targets = people[offset[seek]::step]

cur = targets.index(max(targets, key=lambda x: int(x))) * step
print(f'The oldest person is {people[cur]}, they have shoesize '
      f'{people[cur+2]}')


# uppgift B ~ 3.2 Option 1
#
# Objective: Find the person with the median shoesize,
#            then print their name and age.
#
# Methodology:
# 1. Create `targets` once again, this time it's all the shoesizes registered.
# 2. Once again find the max value in `targets`, but replace that value with 0.
# 3. Find the new max value in `targets` and assign it's index,
#    multiplied by step, to `cur`.
# 4. Print the findings.

seek = 'shoesize'
targets = people[offset[seek]::step]

# This method is only valid when there's exactly 3 people registered.
assert len(targets) == 3

targets[targets.index(max(targets, key=lambda x: int(x)))] = '0'
cur = targets.index(max(targets, key=lambda x: int(x))) * step

print(f'The person with the median shoesize is {people[cur]}, they are '
      f'{people[cur+1]} years old.')


# uppgift B ~ 3.2 Option 2
#
# Objective: Find the person with the median shoesize,
#            then print their name and age.
#
# Methodology:
# 1. `targets` with shoesizes
# 2. `targets_in_order`, same as `targets` but sorted ascendingly.
# 3. Get the `middle` index of `targets_in_order`. Technically...
#    If there's an even amount of people registered, the selected value
#    would be the lower one of the two median-most values.
# 4. Get the value in 'targets_in_order` at the 'middle', this is the `median`.
# 5. Get the index of the `median` value in `targets`, multiply by
#    step and assign it to `cur`.
# 6. Print the findings.

seek = 'shoesize'
targets = people[offset[seek]::step]

targets_in_order = sorted(targets, key=lambda x: int(x))
middle, remainder = divmod(len(targets_in_order), 2)
median = targets_in_order[middle]

# This method is only valid when there's an odd amount of people registered.
assert remainder != 0

cur = targets.index(median) * step
print(f'The person with the median shoesize is {people[cur]}, they are '
      f'{people[cur+1]} years old.')


# uppgift B ~ 4
#
# Objective: Ask the user to do a search among the registered people
#            in the following format: [ name | age | shoesize ], [ value ].
#            then look for this value among the registered people and print
#            all the information about them if they are found.
#
# Methodology:
# 1. Get user input using the helper function.
# 2. Try...
#   2.1.  Create `targets`
#   2.2.  Get the index of the `value` in `targets`,
#         multiply by step and assign to `cur`.
# 3. Except...
# 4. Print the findings.

seek, value = input_search()
try:
    targets = people[offset[seek]::step]
    # seek might not exist in offset. -> KeyError
    cur = targets.index(value) * step
    # Value might not exist in targets -> ValueError
    findings = (f'Person found!\n\t\tName: {people[cur]}\n\t\tAge: '
                f'{people[cur+1]}\n\t\tShoesize: {people[cur+2]}\n')
except KeyError:
    findings = f'{seek} is not a valid data field'
except ValueError:
    findings = f'Nobody with the {seek} {value} was found.'

print(findings)


###############################################################################
#   uppgift B
#   Solution 2
#   Pure dictonary solution
###############################################################################
print('\n-- Solution 2 --\n')

#
# Methodology / data structure:
# 2 primary dicts are used, both of them have sub dicts
#   lookup {
#       category key (seek) -> category {
#           value -> key
#       }
#   }
#   data {
#       key -> owner (person) {
#           category key -> value
#   }
#
# If we know one seek:value pair eg. age: 15, we can easily get
# the owner of that data by `person = data[lookup['age'][15]]`.
# If you have trouble seeing how it works out...
# Let's do it step by step:
#   category = lookup['age']
#   key of owner = category[value]
#   person = data[key of owner]
#
# Since accessing the data is so straightforward, focus is
# at getting that category:value pair that we want to look for.

lookup = {
    'name': {},
    'age': {},
    'shoesize': {},
}
data = {}


def populate(name: str, age: str, size: str) -> None:
    """Helper function to populate the dictonaries with data"""
    lookup['name'][name] = id(name)
    lookup['age'][age] = id(name)
    lookup['shoesize'][size] = id(name)
    data[id(name)] = {
        'name': name,
        'age': age,
        'shoesize': size
    }


if not DEV_MODE:
    populate(input_person())
    populate(input_person())
    populate(input_person())
else:
    populate('pelle', '15', '55')
    populate('martin', '13', '25')
    populate('rasmus', '17', '35')


# uppgift B ~ 3.1
#
# Objective: Find the oldest person and print their name and shoesize.

old = max(lookup['age'], key=lambda x: int(x))

person = data[lookup['age'][old]]
print(f'The oldest person is {person["name"]}, they have shoesize '
      f'{person["shoesize"]}')


# uppgift B ~ 3.2
#
# Objective: Find the person with the median shoesize,
#            then print their name and age.

half, remainder = divmod(len(data), 2)
assert remainder != 0  # Median values don't exist for sequences of even lenth

shoe = sorted(lookup['shoesize'], key=lambda x: int(x))[half]

person = data[lookup['shoesize'][shoe]]
print(f'The person with the median shoesize is {person["name"]}, they are '
      f'{person["age"]} years old.')


# uppgift B ~ 4
#
# Objective: Ask the user to do a search among the registered people
#            in the following format: [ name | age | shoesize ], [ value ].
#            then look for this value among the registered people and print
#            all the information about them if they are found.

seek, value = input_search()

try:
    person = data[lookup[seek][value]]
    print(f'Person found!\n\t\tName: {person["name"]}\n\t\tAge: '
          f'{person["age"]}\n\t\tShoesize: {person["shoesize"]}\n')
except Exception:
    print(f'Sorry could not find anyone with the {seek} {value}')


###############################################################################
#   uppgift B
#   Solution 3
#   Using a Class and a list of objects of said class.
###############################################################################

class Person(object):
    """Simple datacontainer reprsenenting a person"""

    def __init__(self, name: str, age: str, shoesize: str):
        """Create person with name:str, age: str, shoesize: str"""
        self.name = name
        self.age = age
        self.shoesize = shoesize

    def __str__(self) -> str:
        """Format class data for presentation"""
        return (f'Person found!\n\t\tName: {self.name}\n\t\tAge: '
                f'{self.age}\n\t\tShoesize: {self.shoesize}\n')


people = []

if not DEV_MODE:
    people += [Person(input_person())]
    people += [Person(input_person())]
    people += [Person(input_person())]
else:
    people += [Person('pelle', '15', '55')]
    people += [Person('martin', '13', '25')]
    people += [Person('rasmus', '17', '35')]

# uppgift B ~ 3.1
#
# Objective: Find the oldest person and print their name and shoesize.

print(max(people, key=lambda x: int(x.age)))


# uppgift B ~ 3.2
#
# Objective: Find the person with the median shoesize,
#            then print their name and age.

half, remainder = divmod(len(people), 2)
assert remainder != 0  # Median values don't exist for sequences of even lenth

print(sorted(people, key=lambda x: int(x.shoesize))[half])

# uppgift B ~ 4
#
# Objective: Ask the user to do a search among the registered people
#            in the following format: [ name | age | shoesize ], [ value ].
#            then look for this value among the registered people and print
#            all the information about them if they are found.

seek, value = input_search()

found = False
for person in people:
    try:
        if getattr(person, seek) == value:
            print(person)
            found = True
    except AttributeError:
        print(f"{seek} is not a valid search key!\nExiting...")
        break

if not found:
    print(f'Sorry could not find anyone with the {seek} {value}')
