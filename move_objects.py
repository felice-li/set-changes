import csv
from collections import OrderedDict

# create 2 lists, left and right, that holds the pieces on stage left and right respectively
left = []
right = []
with open("leftright.csv", mode='r') as file:
    csvFile = csv.reader(file)
    for line in csvFile:
        left.append(line[0])
        right.append(line[1])
left = left[1:]
right = right[1:]


scene_items = {} # stores {'scene-name':item_names}, item_names is a list of strings
numbers_scene = {} # stores {'scene-number':scene-name}

# read the file, organize into a list of dictionaries
# each line of the list is a dictionary of scene info
with open("scenesets.csv", mode='r') as file:
    csvFile = csv.DictReader(file)
    for line in csvFile:
        item_names = line['items'].split()
        scene_items[line['scene-name']] = item_names
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

# returns a dictionary: {set_left: '', strike_left: '', set_right: '', strike_right: ''}
def compare_scene(scene1, scene2):
    todo = {'set_left': '', 'strike_left': '', 'set_right': '', 'strike_right': ''}
    # declare lists of items in each scene
    scene1things = scene_items[scene1]
    scene2things = scene_items[scene2]
    
    # pare down to bare essentials – aka remove _action
    # pared-down list is in scene1thingsp and scene2thingsp
    scene1thingsp = []
    for i in scene1things:
        if len(i.split("_")) == 1:
            scene1thingsp.append(i)
    scene2thingsp = []
    for i in scene2things:
        if len(i.split("_")) == 1:
            scene2thingsp.append(i)

    # establish what needs to be striked
    for i in range(len(scene1thingsp)):
        # if the same object exists in both scenes, don't strike
        # else, strike the object on left or right 
        if scene1thingsp[i] not in scene2thingsp:
            if scene1thingsp[i] in left:
                todo['strike_left'] += scene1thingsp[i] + ' '
            else:
                todo['strike_right'] += scene1thingsp[i] + ' '

    # establish what needs to be set
    for i in range(len(scene2things)):
        # if the same scene name, assume same scene and don't flip/move again
        if scene1 == scene2:
            continue

        # if scene 2 item needs to be moved, add to set
        # or if scene 2 item is not in scene 1, add to set
        if len(scene2things[i].split("_")) > 1 or scene2things[i] not in scene1things:
            if scene2things[i].split("_")[0] in left:
                todo['set_left'] += scene2things[i] + ' '
            else: 
                todo['set_right'] += scene2things[i] + ' '
    return todo


# will be written to csv
# output is a list of dictionaries, with each dictionary having the following info: (1) scene-num, (2) scene-name, (3) set, (4) strike
output = []
scene_name1 = numbers_scene[list(numbers_scene.keys())[0]]
# loop through all scene numbers, add what needs to be done between each scene with compare()
for scene_num in dict(list(numbers_scene.items())):
    scene_name = numbers_scene[scene_num]
    this_scene = {'scene-num': scene_num, 'scene-name': scene_name}
    # for the first scene, put everything in set
    if scene_num == list(numbers_scene.keys())[0]:
        this_scene.update({"set_left": ' '.join(scene_items[scene_name]), "strike_left": "", "set_right": "", "strike_right": ""})
    # if not first scene, actually compare
    else: 
        this_scene.update(compare_scene(scene_name1, scene_name).items())
    # add it to final output
    output.append(this_scene)
    # keep track of prev scene with scene_name1
    scene_name1 = scene_name

with open('moves.csv', 'w', newline='') as csvfile:
    fieldnames = ['scene-num', 'scene-name', 'set_left', 'strike_left', "set_right", "strike_right"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output)


## future
# same people moving same things
# automatically balance left v right? iffy
# !! could prob do this with hash maps?
