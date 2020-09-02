import typing as t

# GUIDELINES
# avoid loops
# avoid if

# REQUIREMENTS
# 1. not-case sensitive
# 2. accept and track user input for 3 people's name, age and shoesize
# 3. print namn and shoesize of the oldest, print name and age of the one that
#      has the median shoesize
# 4. after this the user should be able to search for the people by inputing
# 		one of the three datatypes as well as it's value. If the program finds
# 		someone matching any value it should print all of it's associated data.

# toggles manual data entry
DEV_MODE = True

# Shared code


def input_person(retries: int = 3) -> t.Tuple[str, str, str]:
    """Helper function to create user data."""
    try:
        name, age, size = input('name, age, shoesize\n>> ').lower().split(',')
        return name.strip(), age.strip(), size.strip()
    except ValueError:
        if retries:
            return input_person(retries - 1)
        raise


def input_search(retries: int = 3) -> t.Tuple[str, str]:
    """Helper function to create search requests."""
    try:
        category, value = input(
            '[name|age|shoesize],[search_value]\n>> ').lower().split(',')
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
    # people += [*input_person()]
    people += input_person()
    people += input_person()
    people += input_person()
else:
    people += ['pelle', '15', '55']
    people += ['martin', '13', '25']
    people += ['rasmus', '17', '35']


#
# uppgift B ~ 3.1
#
# Objective: Find the oldest person and print their name and shoesize.
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

#
# uppgift B ~ 3.2
#
# Objective: Find the person with the largest shoesize,
#            then print their name and age.
# Methodology: (2 alternatives)


# V1 (Only works if there's exactly 3 people registered)
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


# V2 (Works as long as the amount of people registerd is odd (%2!=0))
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
# four = offset[seek]
targets = people[offset[seek]::step]

targets_in_order = sorted(targets, key=lambda x: int(x))
middle, reminder = divmod(len(targets_in_order), 2)
median = targets_in_order[middle]

# This method is only valid when there's an odd amount of people registered.
assert reminder != 0

cur = targets.index(median) * step
print(f'The person with the median shoesize is {people[cur]}, they are '
      f'{people[cur+1]} years old.')


#
# uppgift B ~ 4
#
# Objective: Ask the user to do a search among the registered people
#            in the following format: [ name | age | shoesize ], [ value ].
#            then look for this value among the registered people and print
#            all the information about them if they are found.
#
# Methodology:
#   1. Get user input using the helper function.
#   2. Try...
#     2.1.  Create `targets`
#     2.2.  Get the index of the `value` in `targets`,
#           multiply by step and assign to `cur`.
#   3. Except...
#   4. Print the findings.

seek, value = input_search()
try:
    targets = people[offset[seek]::step]
    # seek might not exist in offset. -> KeyError
    cur = targets.index(value)
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
#   Dictonary solution, re-write in progress
###############################################################################


# Extensive dict-only solution

# data_table = {
#     'martin': {
#         'name': 'martin',
#         'age': '13',
#         'shoesize': '25',
#     },
#     'pelle': {
#         'name': 'pelle',
#         'age': '15',
#         'shoesize': '55'
#     },
#     'rasmus': {
#         'name': 'rasmus',
#         'age': '17',
#         'shoesize': '35'
#     }
# }

# age_lookup_table = {
#     '15': data_table['pelle'],
#     '13': data_table['martin'],
#     '17': data_table['rasmus']
# }

# shoesize_lookup_table = {
#     '55': data_table['pelle'],
#     '25': data_table['martin'],
#     '35': data_table['rasmus']
# }

# name_lookup_table = {
#     'pelle': data_table['pelle'],
#     'martin': data_table['martin'],
#     'rasmus': data_table['rasmus']
# }

# section_table = {
#     'name': name_lookup_table,
#     'age': age_lookup_table,
#     'shoesize': shoesize_lookup_table,
# }


# invalid_section = {
#     'type': 'invalid section',
#     'text': "The section is invalid!"
# }

# invalid_data = {
#     'type': 'data not found',
#     'text': 'The data was not found.'
# }

# validate_args = {
#     True: ['fail', 'safe']  # equivalent to invalid data scenario
# }

# validate_section = {
#     True: invalid_section
# }

# validate_data = {
#     True: invalid_data
# }

# text_table = {
#     True: "Person found!\n\t\tName: {data[name]}\n\t\tAge: {data[age]}\n\t\tShoesize: {data[shoesize]}\n",
#     False: "ERROR: {data[text]}"
# }

# if "-m2" in argv:
#     while True:
#         args = input("Please enter search data. `[ name | age | shoesize ] [ value ]`\n>> ").lower().split(" ")
#         args = validate_args.get(len(args) != 2, args)

#         section_test = section_table.get(args[0], invalid_section)
#         valid_section = validate_section.get(section_test is False, section_test)

#         test_data = valid_section.get(args[1], invalid_data)
#         valid_data = validate_data.get('name' not in test_data, test_data)

#         text = text_table['name' in valid_data]
#         print(text.format(data=valid_data))


# # 'Short' dict-only solution

# data_table = {
#     'martin': {
#         'name': 'martin',
#         'age': '13',
#         'shoesize': '25',
#     },
#     'pelle': {
#         'name': 'pelle',
#         'age': '15',
#         'shoesize': '55'
#     },
#     'rasmus': {
#         'name': 'rasmus',
#         'age': '17',
#         'shoesize': '35'
#     }
# }

# age_lookup_table = {
#     data_table.values()[0]['age']: data_table[data_table.keys()[0]],
#     data_table.values()[1]['age']: data_table[data_table.keys()[1]],
#     data_table.values()[2]['age']: data_table[data_table.keys()[2]]
# }

# shoesize_lookup_table = {
#     '55': data_table['pelle'],
#     '25': data_table['martin'],
#     '35': data_table['rasmus']
# }

# name_lookup_table = {
#     'pelle': data_table['pelle'],
#     'martin': data_table['martin'],
#     'rasmus': data_table['rasmus']
# }

# section_table = {
#     'name': name_lookup_table,
#     'age': age_lookup_table,
#     'shoesize': shoesize_lookup_table,
# }

# while True:
#     try:
#         args = input('Please enter search data. `[ name | age | shoesize ] [ value ]`\n>> ').lower().split(' ')
#         section_search = args[0]
#         value_search = args[1]
#         data = section_table[section_search][value_search]
#         print(f"Person found!\n\t\tName: {data['name']}\n\t\tAge: {data['age']}\n\t\tShoesize:' {data['shoesize']}\n")
#     except KeyboardInterrupt:
#         quit()
#     except Exception as e:
#         print(f'{type(e)}! ~ {e}')
