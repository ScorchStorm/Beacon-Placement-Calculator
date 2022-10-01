import csv
from numpy import sqrt, array, floor, empty_like, ones_like
from tkinter import Tk, Frame, Canvas, BOTH

path_names = []
'''Prints a list with the format [[origin_name to destination_name],[origin_name to destination_name]]'''
beacon_paths = []
'''A list that follows the format: [[origin_name, origin_coordinates, destination_name, destination_coordinates]]'''
preferences = []
'''A list that follows the format: [[color, spacing, f_n_beacons, f_spacing, f_away, block, height]]'''
coordinates = []
'''A list that follows the format: [[array([x_coor, y_coor]), array([x_coor, y_coor])][array([x_coor, y_coor]), array([x_coor, y_coor])]]'''
resources = []
'''A list that follows the format: [["beacons", n_beacons, block_name, n_blocks],["beacons", n_beacons, block_name, n_blocks]]'''
resources_dict = {}
'''A dictionary of resources that follows the format: {resource: number, resource: number}'''

def main():
    welcome()
    while True:
        print('')
        print("Please Enter the index of the option you'd like to do")
        print("1. Add new beacon paths to list") # appends a list of names and coordinates for path origins and destinations. # ex: beacon_vectors = [[origin_name, origin_coordinates, destination_name, destination_coordinates],[origin_name, origin_coordinates, destination_name, destination_coordinates]]
        print("2. Create a new set of preferences for beacon paths") # appends a list of preferences for beacon spacing, destination beacon numbers, destination beacon spacing, glass color, pyramid block and pyramid height.
        print("3. Create a list of Coordinates and Resources for each beacon path")
        print("4. Print a list of the coordinates for beacons to be built at") # creates and displays a list of coordinates for beacons to be placed on one, multiple, or all beacon paths
        print("5. Print a list of the resources required to create beacon paths") # creates and displays a list of resources required to build one, multiple, or all beacon paths
        print("6. Save current paths/preferences/coordinates/resources lists for later") # user must already have a list of beacon paths/preferences or it will ask them to create one, it will automatically create coordinate/resource lists
        print("7. View a previously saved set of paths/preferences/coordinates/resources lists") # this is so the computer doesn't have to redo the calculations each time you want to view a previoulsy saved list
        print("8. Clear current paths/preferences/coordinates/resources lists") # clears the lists for paths, preferences, coordinates and resources
        print("9. Print all currently active lists") # A trouble shooting function
        index = integer("Index: ")
        if index == 1:
            get_beacon_paths()
        elif index == 2:
            backtrack(index)
            get_preferences()
        elif index == 3:
            get_coordinates()
            create_resources_lists()
            global resources_dict
            resources_dict = create_resources_dict(range(len(beacon_paths)))
        elif index == 4:
            backtrack(index)
            print_coordinates()
        elif index == 5:
            backtrack(index)
            print_resources()
        elif index == 6:
            backtrack(index)
            save_beacon_data()
        elif index == 7:
            import_saved_beacon_data()
        elif index == 8:
            clear_beacon_data()
        elif index == 9:
            print_all_lists()
        elif index == 10:
            calculate_work_hours()
        else:
            print('the number you entered is not a valid index')
            print('Please enter an integer from 1 to 8')

def welcome():
    print("Welcome to the Beacon Location Finder")

def backtrack(index):
    if index > 1 and len(beacon_paths) == 0:
        print("Sorry but you must have beacon paths before performing this action")
        get_beacon_paths()
    elif index > 2 and len(beacon_paths) > len(preferences):
        print("Sorry but some of your paths are missing preferences, all your paths need to have preferences before performing this action")
        get_preferences()
    elif index > 3 and len(coordinates) == 0:
        global resources_dict
        get_coordinates()
        create_resources_lists()
        resources_dict = create_resources_dict(range(len(beacon_paths)))

def create_or_load_data(sorry, data, function):
    print(sorry)
    while True:
        index = integer(f'would you like to 1. load previously saved {data}\nor\n2. create new {data}')
        if index == 1:
            import_saved_beacon_data()
        elif index == 2:
            function()
        else:
            print("Please enter an integer between 1 and 2")


def yes_or_no(question):
    '''Parameters: a yes or no quesion
    Return: a true or false answer'''
    while True:
        answer = input(question)
        if answer.lower() == 'n' or answer.lower() == 'no':
            return False
        elif answer.lower() == 'y' or answer.lower() == 'yes':
            return True
        else:
            print("That's not a valid answer. Please enter yes or no")

def floating(question):
    '''Parameters: a question
    Return: a float'''
    while True:
        try:
            answer = input(question)
            return float(answer)

        except TypeError as type_err:
                print(f"The number you entered {type_err} you entered is not a valid number")
                print("Please enter a valid number")

        except ValueError as val_err:
            print(f"The number you entered {val_err}, has non-number characters")
            print("Please enter a valid number")

def integer(question):
    '''Parameters: a question
    Return: an integer'''
    while True:
        try:
            answer = input(question)
            return int(answer)

        except TypeError as type_err:
                print(f"The number you entered {type_err} you entered is not a valid integer")
                print("Please enter an integer")

        except ValueError as val_err:
            print(f"The number you entered {val_err}, has non-number characters")
            print("Please enter a valid integer")

def get_array(question):
    '''Parameters: a question
        Returns: an array'''
    while True:
        try:
            answer = input(question)
            return array(answer.split(','), int)

        except TypeError as type_err:
            print(f'Type Error: {type_err}')
            print(f"The coordinates you entered {answer} is not a valid set of coordinates")
            print("Please enter a valid set of coordinates")

        except ValueError as val_err:
            print(f'Value Error: {val_err}')
            print(f"The coordinates you entered {answer}, has non-number characters")
            print("Please enter a valid set of coordinates")

def choose_path_index():
    '''Parameters: none
        Returns: a valid index for beacon_paths'''
    while True:
        print("Please enter the index of one of the following beacon paths:")
        for n in range(len(beacon_paths)):
            print(f'{n + 1}. {beacon_paths[n][0]} + " to " + {beacon_paths[n][2]}')
        index = integer("Index: ") - 1
        if index > len(beacon_paths):
            print(f"Sorry, that's not a valid index. Please enter an integer from 1 to {len(beacon_paths)}")
            choose_path_index()
        else:
            return index - 1

def choose_path_indexes():
    '''Parameters: none
        Returns: valid indexes for beacon_paths'''
    while True:
        print("Please enter the index of one or more of the following beacon paths:")
        for n in range(len(beacon_paths)):
            print(f'{n + 1}. {beacon_paths[n][0]} to {beacon_paths[n][2]}')
        pre_indexes = get_array("Indexes: ")
        sub = ones_like(pre_indexes)
        indexes = pre_indexes - sub
        for index in indexes:
            if index > len(beacon_paths):
                print(f"Sorry, those are not valid indexes. Please enter integers from 1 to {len(beacon_paths)}")
        return indexes

def get_beacon_paths():
    print('')
    n_paths = integer("How many new paths do you want to enter? ")
    if n_paths >= 1:
        if n_paths ==1:
            origin = get_array("What are the X and Z coordinates of the origin? ")
            destination = get_array("What are the X and Z coordinates of the destination? ")
            origin_name = input("What is the name of the origin? ")
            destination_name = input("What is the name of the destination? ")
            beacon_paths.append([origin_name, origin, destination_name, destination])
            path_name = f"Path from {origin_name} to {destination_name}"
            path_names.append(path_name)
        else:
            same_origin = yes_or_no("Do all the paths have the same origin? ")
            if same_origin:
                origin = get_array("What are the X and Z coordinates of the origin? ")
                origin_name = input("What is the name of the origin? ")
                for n in range(n_paths):
                    destination = get_array(f"What are the X and Z coordinates of destination {n}? ")
                    destination_name = input(f"What is the name of destination {n}? ")
                    beacon_paths.append([origin_name, origin, destination_name, destination])
                    path_name = f"Path from {origin_name} to {destination_name}"
                    path_names.append(path_name)
            else:
                for _ in range(n_paths):
                    origin = get_array(f"What are the X and Z coordinates of origin {n}? ")
                    destination = get_array(f"What are the X and Z coordinates of destination {n}? ")
                    origin_name = input(f"What is the name of origin {n}? ")
                    destination_name = input(f"What is the name of destination {n}? ")
                    beacon_paths.append([origin_name, origin, destination_name, destination])
                    path_name = f"Path from {origin_name} to {destination_name}"
                    path_names.append(path_name)
    else:
        print("That's not a valid number of paths. Please enter an integer greater than 0")

def get_preferences():
    """appends a list of preferences for beacon spacing, destination beacon numbers, destination beacon spacing, distance from destination to closest beacon, glass color, pyramid block and pyramid height."""
    for _ in range(len(beacon_paths) - len(preferences)):
        preferences.append([])
    print('')
    display_colors()
    repetitive_question("color")
    root.destroy()
    repetitive_question("spacing between path beacons", "float")
    repetitive_question("number of destination beacons", "int")
    repetitive_question("spacing between destination beacons", "float")
    repetitive_question("distance from the closest beacon to the destination", "float")
    repetitive_question("pyramid block")
    repetitive_question("pyramid height", "int")

def repetitive_question(question, type = ''):
    if len(beacon_paths) > 1:
        full_question = "Do you want each of your beacon paths to have the same " + question + "? "
        same = yes_or_no(full_question)
        if same:
            answer = fit_type((f"What do you want the {question} to be for each beacon path? "), type)
            for n in range(len(beacon_paths)):
                preferences[n].append(answer)
        else:
            for n in range(len(beacon_paths)):
                answer = fit_type((f"What do you want the {question} to be for the {path_names[n]}? "), type)
                preferences[n].append(answer)
    else:
        answer = fit_type((f"What do you want the {question} to be for your only beacon path? "), type)
        preferences[0].append(answer)

def fit_type(question, type):
    if type == 'float':
        return floating(question)
    elif type == 'int':
        return integer(question)
    else:
        return input(question)

def display_colors():
    colors = [['white',249,255,255],['gray',156,157,151],['dark gray',71,79,82],['black',29,28,33],['yellow',255,216,61],['orange',249,128,29],['red',176,46,38],['brown',130,84,50],['lime',128,199,31],['green',93,124,21],['light blue',58,179,218],['cyan',22,156,157],['blue',60,68,169],['pink',243,140,170],['magenta',198,79,189],['purple',137,50,183]]
    '''[[color_name, [r,g,b]],[color_name, [r,g,b]]]'''
    scene_width  = 145
    color_height = 30
    border = 10
    scene_height = border * (len(colors) + 1) + len(colors) * color_height
    canvas = start_drawing("Beacon Colors", scene_width, scene_height)
    color_right = scene_width - border
    color_left = color_right - color_height
    text_center_x = color_left/2
    for n in range(len(colors)):
        bottom_y = scene_height - (n + 1) * border - (n + 1) * color_height
        top_y = bottom_y + color_height
        text_center_y = bottom_y + color_height/2
        draw_text(canvas, text_center_x, text_center_y, colors[n][0].title())
        draw_rectangle(canvas, color_left, bottom_y, color_right, top_y, width=1, outline="black", fill=_make_color(colors[n][1],colors[n][2],colors[n][3]))

def start_drawing(title, width, height): # I copied this from draw2d.py
    global root # I finally was able to simplify this program by just copying the next 3 functions from draw2d.py and learning that I only needed to add root.attributes("-topmost", True) for the widget to automatically display on top of VS code. Now that was a huge pain!!!
    root = Tk()
    root.attributes("-topmost", True) # This line of code took hours and hours to find and impliment. I ended up having to copy the next 3 functions from draw2d.py for this solution to even work!
    root.geometry(f"{width}x{height}")
    frame = Frame()
    frame.master.title(title)
    frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(frame)
    canvas.pack(fill=BOTH, expand=1)
    canvas.update()
    return canvas

def draw_rectangle(canvas, x0, y0, x1, y1,* ,width=1, outline="black", fill=""): # I copied this from draw2d.py
    height = canvas.winfo_height()
    canvas.create_rectangle(x0, height-y0, x1, height-y1, width=width, outline=outline, fill=fill)

def draw_text(canvas, center_x, center_y, text, *, fill="black"): # I copied this from draw2d.py
    height = canvas.winfo_height()
    canvas.create_text(center_x, height-center_y, text=text, fill=fill)

def _make_color(r, g, b): # I copied this from draw2d.py
    return "#" + _hex_str(r) + _hex_str(g) + _hex_str(b)

def _hex_str(n): # I copied this from draw2d.py
    n = int(round(n, 0))
    assert 0 <= n <= 255
    s = hex(n)[2:]
    if len(s) == 1:
        s = "0" + s
    return s

def get_coordinates():
    coordinates.clear()
    for n in range(len(beacon_paths)):
        path_coordinates = []
        origin = beacon_paths[n][1]
        destination = beacon_paths[n][3]
        spacing = preferences[n][1]
        pre_vector = destination - origin
        pre_distance = find_distance(pre_vector)
        unit_vector = pre_vector / pre_distance
        vector = destination - origin - unit_vector * preferences[n][4]
        distance = find_distance(vector)
        n_beacons = int(floor(distance/spacing))
        beacon_vector = spacing * unit_vector
        for num in range(n_beacons):
            coordinate = (origin + (num + 1) * beacon_vector).round()
            path_coordinates.append(coordinate)
        f_n_beacons = preferences[n][2]
        f_spacing =  preferences[n][3]
        f_away = preferences[n][4]
        f_unit_vector = perpendicular(unit_vector)
        f_distance = f_spacing * (f_n_beacons - 1)
        f_vector = f_unit_vector * f_distance
        f_center = destination - f_away * unit_vector
        f_origin = f_center - f_vector / 2
        f_beacon_vector = f_vector / (f_n_beacons - 1)
        for n in range(f_n_beacons):
            coordinate = (f_origin + n * f_beacon_vector).round()
            path_coordinates.append(coordinate)
        coordinates.append(path_coordinates)
    return coordinates

def perpendicular(vector): # from https://stackoverflow.com/questions/16890711/normalise-and-perpendicular-function-in-python
    perpendicular = empty_like(vector)
    perpendicular[0] = -vector[1]
    perpendicular[1] = vector[0]
    return perpendicular

def find_distance(vector):
    distance = sqrt((vector**2).sum())
    return distance

def print_coordinates():
    print('')
    if yes_or_no('Would you like to see the beacon coordinates for all paths? '):
        indexes = range(len(path_names))
    else:
        print("Which path or paths would you like to see the beacon coordinates for? ")
        indexes = choose_path_indexes()
    n = 1
    for index in indexes:
        print(f'{n}. {path_names[index]}:')
        n += 1
        for num in range(len(coordinates[index])):
            print(coordinates[index][num])

def create_resources_lists():
    resources.clear()
    for index in range(len(beacon_paths)):
        block_name = preferences[index][5]
        pyramid_height = preferences[index][6]
        color = preferences[index][0]
        glass = f'{color} tinted glass'
        n_blocks_pyramid = 0
        for n in range(pyramid_height + 1):
            if n != 0:
                width = 2 * n + 1
                n_blocks_pyramid += width ** 2
        n_beacons = len(coordinates[index])
        n_blocks = n_blocks_pyramid * n_beacons
        resources.append(["beacons", n_beacons, block_name, n_blocks, glass, n_beacons])

def create_resources_dict(indexes):
    resources_dict = {}
    for index in indexes:
        for r in range(0, len(resources[index]), 2):
            name = resources[index][r]
            number = resources[index][r + 1]
            if name in resources_dict:
                resources_dict[name] += number
            else:
                resources_dict[name] = number
    return resources_dict

def print_resources():
    print('')
    all = yes_or_no("Would you like to see the required resources for all paths? ")
    if all:
        print("Resources required for all paths:")
        print_dict(resources_dict)
    else:
        print("Which path or paths would you like to see the required resources for? ")
        indexes = choose_path_indexes()
        print_resources_lists(indexes)
        if len(indexes) > 1:
            print("Total:")
            print_dict(create_resources_dict(indexes))

def print_dict(dict):
    for name, number in dict.items():
        print(f"{name} x {number}")

def print_list(list):
    for item in list:
        print(item)

def print_resources_lists(indexes):
    for index in indexes: 
        print(f'Resources for {path_names[index]}:')
        for r in range(0, len(resources[index]), 2):
            name = resources[index][r]
            number = resources[index][r + 1]
            print(f'{name} x {number}')
        return indexes

def save_beacon_data():
    print('')
    with open('beacons.csv', "at") as csv_file:
        writer = csv.writer(csv_file)
        save_name = input("What would you like this save to be named? ")
        compound_list = [save_name, path_names, [resources_dict], resources, beacon_paths, preferences, coordinates]
        writer.writerow(compound_list)

def import_saved_beacon_data():
    clear_beacon_data()
    print('')
    index = choose_save_index()
    with open('beacons.csv', "rt") as csv_file:
        reader = csv.reader(csv_file)
        for _ in range(index):
            next(reader)
        items = next(reader)
        new_path_names = extract_path_names(items[1])
        new_resources_dict = extract_resources_dict(items[2])
        new_resources = extract_resources(items[3])
        new_beacon_paths = extract_beacon_paths(items[4])
        new_preferences = extract_preferences(items[5])
        new_coordinates = extract_coordinates(items[6])
        make_global(new_path_names, new_resources_dict, new_resources, new_beacon_paths, new_preferences, new_coordinates)

def remove_characters(string, characters = ['[', ']',"' "," '", '"', "'", '(', ')', 'array', '{', '}']):
    for character in characters:
        string = string.replace(character, '')
    return string.split(',')

def extract_array(x_coor, y_coor):
    return array([round(float(x_coor.replace(' ', ''))), round(float(y_coor.replace(' ', '')))])

def extract_path_names(input):
    new_path_names = remove_characters(input)
    return new_path_names

def extract_resources_dict(input):
    new_resources_dict = {}
    new_resources_dict = extract_dict(new_resources_dict, remove_characters(input))
    return new_resources_dict

def extract_dict(dict, lists):
    for items in lists:
        items = items.split(':')
        name = items[0].strip()
        number = items[1]
        if name in dict:
            dict[name] += int(number)
        else:
            dict[name] = number
    return dict

def extract_resources(input):
    list = remove_characters(input)
    new_resources = []
    for n in range (0, len(list), 6):
        new_resources.append([list[n].strip(), int(list[n+1]), list[n+2].strip(), int(list[n+3]), list[n+4].strip(), int(list[n+5])])
    return new_resources

def extract_beacon_paths(input):
    new_beacon_paths =[]
    list = remove_characters(input, ['[', ']', '"', "'", '(', ')', 'array'])
    for n in range (0, len(list), 6):
        new_beacon_paths.append([list[n].strip(), extract_array(list[n+1], list[n+2]), list[n+3].strip(), extract_array(list[n+4], list[n+5])])
    return new_beacon_paths

def extract_preferences(input):
    new_preferences = []
    list = remove_characters(input)
    for n in range (0, len(list), 7):
        new_preferences.append([list[n].strip(), float(list[n+1]), int(list[n+2]), float(list[n+3]), float(list[n+4]), list[n+5].strip(), int(list[n+6])])
    return new_preferences

def extract_coordinates(input):
    new_coordinates = []
    for sub_list in input.split("], ["):
        list = remove_characters(sub_list)
        app_list = []
        for n in range(0, len(list), 2):
            coordinate = extract_array(list[n], list[n+1])
            app_list.append(coordinate)
        new_coordinates.append(app_list)
    return new_coordinates

def make_global(new_path_names, new_resources_dict, new_resources, new_beacon_paths, new_preferences, new_coordinates):
    global path_names
    path_names = new_path_names
    global resources_dict
    resources_dict = new_resources_dict
    global resources
    resources = new_resources
    global beacon_paths
    beacon_paths = new_beacon_paths
    global preferences
    preferences = new_preferences
    global coordinates
    coordinates = new_coordinates

def clear_beacon_data():
    path_names.clear()
    beacon_paths.clear()
    preferences.clear()
    coordinates.clear()
    resources.clear()
    resources_dict.clear()

def choose_save_index():
    with open('beacons.csv', "rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        print("Enter the index of the saved data you would like to use")
        n = 1
        for items in reader:
            if len(items) != 0:
                save_name = items[0]
                path_names = items[1]
                resources_dict = items[2]
                print(f'{n}. {save_name}  Paths: {path_names}  Resources: {resources_dict}')
                n += 1
        index = integer("Index: ")
        return index

def print_all_lists():
    '''Prints all currently active lists'''
    print(f'path_names = {path_names}')
    print(f'beacon_paths = {beacon_paths}')
    print(f'preferences = {preferences}')
    print(f'coordinates = {coordinates}')
    print(f'resources = {resources}')
    print(f'resources_dict = {resources_dict}')

def goodbye():
    print('')
    print("Thank you for using the Beacon Coordinate Finder")

def calculate_work_hours():
    work_days = [] # work_days = [[hours, minutes][hours, minutes]]
    hours = 0
    minutes = 0
    work_days.append([4, 5]) # I worked on this program on 7/1/2022 from 5:30pm to 8:45pm and then from 8:57pm to 10:02pm -  4 hr 5 min
    work_days.append([9, 4]) # I worked on this program on 7/2/2022 from 10:00am to > 12:00pm and then from 12:30pm to > 9:34pm (seriously) - 9 hr 4 min
    work_days.append([11, 6]) # I worked on this program on 7/3/2022 from 2:17pm to 10:23pm and then from 12:48am to 3:58am (also very seriously)  - 11 hr 6 min(This is when all of the programs functions were finally working! =D)
    work_days.append([0, 42]) # I worked on this program on 7/5/2022 from 8:56pm to 9:38pm - 0 hr 42 minutes
    work_days.append([2, 45]) # I worked on this program on 7/10/2022 from 9:10pm to 11:55pm - 2 hours 45 minutes
    work_days.append([1, 25]) # I worked on this program on 7/14/2022 from 3:30pm to 4:30 pm and then from 9:45pm to 10:10pm - 1 hour 25 minutes
    # I made the calculate_work_hours() function and elimnated some unnecessary lists
    work_days.append([4, 35])# I worked on this program on 7/16/2022 from 8:15pm to 12:50 pm - 4 hours, 35 minutes
    # I found all the colors of minecraft glass online and implemented code that would display each color next to it's name when players are choosing colors for their beacon paths
    for day in work_days:
        hours += day[0]
        minutes += day[1]
    while minutes >= 60:
        hours += 1
        minutes -= 60
    print(f'total_time = {hours} hours & {minutes} minutes') # Final Total = 33 hours and 42 minutes

if __name__ == "__main__":
    main()