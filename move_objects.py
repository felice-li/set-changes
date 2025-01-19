import csv
from collections import OrderedDict

scene_items = {} # stores {'scene-name':items}
numbers_scene = {} # stores {'scene-number':scene-name}

# read the file, organize into a list of dictionaries
# each line of the list is a dictionary of scene info
with open("sets.csv", mode='r') as file:
    csvFile = csv.DictReader(file)
    for line in csvFile:
        scene_items[line['scene-name']] = line['items']
        numbers = line['scene-numbers'].split()
        for number in numbers:
            numbers_scene[number] = line['scene-name']

# orders scene numbers with its corresponding scene name
def order_numbers(d1):
    orderedkeys = list((d1.keys()))
    orderedkeys.sort()
    newD = dict.fromkeys(orderedkeys)
    for num in newD:
        newD[num] = d1[num]
    return newD

numbers_scene = order_numbers(numbers_scene)

# goal: list form of data, use csv.write()

# returns a dictionary: {set: '', strike: ''}
def compare_scene(scene1, scene2):
    todo = {'set': '', 'strike': ''}
    # declare lists of items in each scene
    scene1things = scene_items[scene1].split()
    scene2things = scene_items[scene2].split()
    # establish what needs to be striked
    for i in range(len(scene1things)):
        if scene1things[i] not in scene2things:
            todo['strike'] += scene1things[i] + ' '
    todo['strike'] = todo['strike'][:-1]
    # establish what needs to be set
    for i in range(len(scene2things)):
        if scene2things[i] not in scene1things:
            todo['set'] += scene2things[i] + ' '
    todo['set'] = todo['set'][:-1]
    return todo

# will be written to csv
output = []
scene_name1 = numbers_scene[list(numbers_scene.keys())[0]]
print(scene_name1)
for scene_num in dict(list(numbers_scene.items())[1:]):
    scene_name = numbers_scene[scene_num]
    this_scene = {'scene-num': scene_num, 'scene-name': scene_name}
    this_scene.update(compare_scene(scene_name1, scene_name).items())
    output.append(this_scene)
    scene_name1 = scene_name

with open('moves.csv', 'w', newline='') as csvfile:
    fieldnames = ['scene-num', 'scene-name', 'set', 'strike']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output)