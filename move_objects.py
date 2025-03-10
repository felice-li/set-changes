import csv
from collections import OrderedDict

scene_items = {} # stores {'scene-name':items}
numbers_scene = {} # stores {'scene-number':scene-name}

# read the file, organize into a list of dictionaries
# each line of the list is a dictionary of scene info
with open("sing2025-scenesets.csv", mode='r') as file:
    csvFile = csv.DictReader(file)
    for line in csvFile:
        scene_items[line['scene-name']] = line['items']
        numbers = line['scene-numbers'].split()
        for number in numbers:
            numbers_scene[float(number)] = line['scene-name']

# orders scene numbers with its corresponding scene name
# scene numbers should be in float form
def order_numbers(d1):
    orderedkeys = list((d1.keys()))
    orderedkeys.sort()
    newD = dict.fromkeys(orderedkeys)
    for num in newD:
        newD[num] = d1[num]
    return newD

numbers_scene = order_numbers(numbers_scene)


# goal: list form of data, use csv.write()


#### NEED TO SORT BETWEEN STAGE LEFT AND STAGE RIGHT 
left = []
right = []
with open("sing2025-leftright.csv", mode='r') as file:
    csvFile = csv.reader(file)
    for line in csvFile:
        left.append(line[0])
        right.append(line[1])
left = left[1:]
right = right[1:]

# returns a dictionary: {set_left: '', strike_left: '', set_right: '', strike_right: ''}
def compare_scene(scene1, scene2):
    todo = {'set_left': '', 'strike_left': '', 'set_right': '', 'strike_right': ''}
    # declare lists of items in each scene
    scene1things = scene_items[scene1].split()
    scene2things = scene_items[scene2].split()
    # establish what needs to be striked
    for i in range(len(scene1things)):
        if scene1things[i] not in scene2things:
            if scene1things[i] in left:
                todo['strike_left'] += scene1things[i] + ' '
            else:
                todo['strike_right'] += scene1things[i] + ' '
    # establish what needs to be set
    for i in range(len(scene2things)):
        if scene2things[i] not in scene1things:
            if scene2things[i] in left:
                todo['set_left'] += scene2things[i] + ' '
            else: 
                todo['set_right'] += scene2things[i] + ' '
    return todo
# print(compare_scene("speakeasy","brewery"))

# will be written to csv
# output_ is a list of dictionaries, with each dictionary having the following info: (1) scene-num, (2) scene-name, (3) set, (4) strike
output = []
scene_name1 = numbers_scene[list(numbers_scene.keys())[0]]
# loop through all scene numbers, add what needs to be done between each scene with compare()
for scene_num in dict(list(numbers_scene.items())):
    scene_name = numbers_scene[scene_num]
    this_scene = {'scene-num': scene_num, 'scene-name': scene_name}
    # for the first scene, put everything in set
    if scene_num == list(numbers_scene.keys())[0]:
        this_scene.update({"set_left": scene_items[scene_name], "strike_left": "", "set_right": "", "strike_right": ""})
    # if not first scene, actually compare
    else: 
        this_scene.update(compare_scene(scene_name1, scene_name).items())
    # add it to final output
    # print(this_scene)
    output.append(this_scene)
    # keep track of prev scene with scene_name1
    scene_name1 = scene_name

print(output)

with open('sing2025-moves.csv', 'w', newline='') as csvfile:
    fieldnames = ['scene-num', 'scene-name', 'set_left', 'strike_left', "set_right", "strike_right"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output)


## future
# verb dont count
# verb makign things appear twice (strike)
# same people moving same things
# automatically balance left v right? iffy
