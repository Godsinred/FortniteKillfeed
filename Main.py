import io
import os
import time
import subprocess
import threading
import brians_printer
import FortniteTracker
import audit_way
import pyautogui
import graphing
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

API_KEY = "e7462887-33cc-44d2-bb7d-ea3796b3231f"
LOCK = threading.Lock()

"""
NOTE: User must obtain a google cloud api key and .json package from the google cloud API. 
Once you have created your api key and generated a .json credential package, place the json in this folder and 
link the folder in the environmental variables. this can be done in the main function in the below code. 
Lastly they must use their associated API key and change the global variable above
"""

def take_screenshot(x, y, num=''):
    """
    Takes a screenshot of the bottom left hand corner where the kill feed is located
    :param x: the x diminsions of the screen (some reason it seems to be 1/2 of the actual size)
    :param y: the y diminsions of the screen (some reason it seems to be 1/2 of the actual size)
    :param num: the number of the screenshot if specified
    :return: nothing
    """
    # screenshot takes starting x,y coordinates and then for how far the shot should stretch
    pic = pyautogui.screenshot(region=(0, y * 1.3, x * 0.75, y * 0.6))
    pic.save("Screenshot" + str(num) + ".png")

def take_linux_screenshot(x, y):
    # if on linux use: 0, y * 1.3, x * 0.75, y * 0.6)
    # -crop WxH+X+Y
    x *= .5
    y *= .5
    height = y * 0.6
    width = x * 0.75
    subprocess.run(['import', '-window', 'root', '-crop', f'{width}x{height}+{0}+{int(y * 1.3)}', '-quality', '100',
                    'Screenshot.png'])

def take_windows_screenshot(x, y):
    """
    Takes a screenshot of the bottom left hand corner where the kill feed is located
    :param x: the x diminsions of the screen (some reason it seems to be 1/2 of the actual size)
    :param y: the y diminsions of the screen (some reason it seems to be 1/2 of the actual size)
    :return: nothing
    """
    # screenshot takes starting x,y coordinates and then for how far the shot should stretch
    pic = pyautogui.screenshot(region=(0, y * 0.6, x * 0.33, y * 0.3))
    pic.save("Screenshot.png")


def process_text(line, fortnite_database, checked = False):
    """
    Process the text that is received from the google vision api
    :param line: one of the many possible lines of text that is received from the google vision api
    :param fortnite_database: the db object
    :param checked: true if the line has been run before to reduce infinite loops
    :return: nothing
    """

    # should also make sure that this "key" word doesn't appear in someone's username <<<<<<<----------------------
    # i.e. "brian_was_eliminated" eliminated "jonny_shotgunned" with a rifle
    # add in string_var.count(key) to make sure it only appears once
    if "eliminated" in line:
         way = "eliminated"
         current_wep = ""
         fortnite_database.update_db(line, way, current_wep)

    elif "shotgunned" in line:
        way = "shotgunned"
        current_wep = "shotgun"
        fortnite_database.update_db(line, way, current_wep)

    elif "sniped" in line:
        way = "sniped"
        current_wep = "sniper"
        fortnite_database.update_db(line, way, current_wep)

    elif "bludgeoned" in line:
        way = "bludgeoned"
        current_wep = "pickaxe"
        fortnite_database.update_db(line, way, current_wep)

    elif "\'sploded" in line or "sploded" in line:
        way = "sploded"
        current_wep = "explosives"
        fortnite_database.update_db(line, way, current_wep)

    elif "checked out early" in line:
        way = "check"
        fortnite_database.update_db(line, way)

    elif "played themselves" in line:
        way = "play"
        fortnite_database.update_db(line, way)

    elif "was lost in the storm" in line:
        way = "was lost"
        fortnite_database.update_db(line, way)

    elif "didn\'t stick the landing" in line:
        way = "didn\'t stick"
        fortnite_database.update_db(line, way)

    elif "is literally on fire" in line:
        way = "is literally"
        fortnite_database.update_db(line, way)

    elif "took the L" in line:
        way = "took the L"
        fortnite_database.update_db(line, way)

    elif "is now spectating you" in line:
        return
    else:
        # doesn't go into infinite loop if the program can't determine a change
        if not checked:
            print("ERROR:Can't determine phrase: {}".format(line))
            print("Analyzing the line and determining if any fixes can be made.")
            new_line = update_sentence(line)
            process_text(line, fortnite_database, True)
# try:
    brians_printer.print_table("SELECT * FROM CurrentStats ORDER BY alive desc", 'Game results', fortnite_database.cur)
    # brians_printer.print_table("SELECT * FROM Players ORDER BY player_id", 'Players', fortnite_database.cur)
    # brians_printer.print_table("SELECT * FROM WeaponStats ORDER BY player_id", 'Weapon stats', fortnite_database.cur)
    # pretty_print(conn,cur)
# except:
#     print("Printing Error.")

def pretty_print(conn, cur): # an out dated function. if use update with fortnite_database object
    """
    Shows all the current data in the db. Currently using because dash has not been setup yet
    :param conn: the connection to the db
    :param cur: the cursor to the db
    :return: nothing
    """

    cur.execute("""SELECT * FROM CurrentStats 
    ORDER BY alive desc
    """)
    data = cur.fetchall()
    # returns x in the x[0] // header row in the data.descriptions
    # iterates through all the items in the data description
    print("\n{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}".format(
        "user_id", "username", "current_kills", "current_weapon", "total_wins", "total_matches", "win_percent",
        "total_kills", "kd", "alive"))

    for d in data:
        print(
            "{:<20d}{:20s}{:<20d}{:20s}{:<20d}{:<20d}{:<20.2f}{:<20d}{:<20.2f}{:<20d}".format(d[0], d[1], d[2], d[3], d[4],
                                                                                          d[5], d[6], d[7], d[8], d[9]))

def update_sentence(line):
    """
    Updates the sentence using the audit_way class to see if changes can be made to the line
    :param line: the line to be updated because the text can't be processed as is
    :return: the new line that can possibly be the same
    """
    checker = audit_way.Similarity()
    return checker.check(line)

def thread_fortnite_api(fortnite_database):
    """
    The thread that will be running the fortnite api and updating the db with usernames
    :param fortnite_database: the db object that has the db and all other important stuff
    :return: nothing runs until program is over
    """

    while True:
        time.sleep(2)

        # runs if something is in the high priority queue, ect...
        if fortnite_database.priority_queue.high_queue:
            fortnite_database.get_api_stats(fortnite_database.priority_queue.high_queue.pop(0), "pc", "high")
        elif fortnite_database.priority_queue.med_queue:
            fortnite_database.get_api_stats(fortnite_database.priority_queue.med_queue.pop(0), "xbox", "med")
        elif fortnite_database.priority_queue.low_queue:
            fortnite_database.get_api_stats(fortnite_database.priority_queue.low_queue.pop(0), "ps4", "low")


def main():
    username = input("What is your username: ").lower()
    start = ""
    while start != "s":
        start = input("Please enter \"s\" to start or \"q\" to quit: ").lower()
        if(start == 'q'):
            exit()

    print("Program starting in:")
    for i in range(5, 0 , -1):
        print(i)
        time.sleep(1)
    print("GO!\n")

    # creates the database
    fortnite_database = FortniteTracker.FortniteTracker(username, API_KEY, LOCK)

    # starts the multi threading in the background to update the database
    # class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
    # can use a barrier thread to synchronize all the threads
    # if deamon thread is false the thread will keep running until it is time to stop
    # if true the thread will stop when the program stops
    t = threading.Thread(target=thread_fortnite_api, args=(fortnite_database,), daemon=True)
    # starts the thread
    t.start()
    t1 = threading.Thread(target=graphing.run_dash, args=(LOCK,), daemon=True)
    t1.start()

    # gets the display size of the computer
    x, y = pyautogui.size()

    # here to num the photos in case we want a reference to them later
    num = 1

    # credentials for vision.ImageAnnotatorClient() object
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/Users/godsinred/Desktop/account_key.json'

    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    time.sleep(5)
    # runs the program the the person dies
    # while num < 5 is still in there it only runs 5 iterations
    while username not in fortnite_database.dead and username.replace('_', ' ') not in fortnite_database.dead:
        #take_screenshot(x, y) # run this one for a real game. don't want a bunch of numbered photos
        #take_linux_screenshot(x, y)  # if on linux use this
        take_windows_screenshot(x, y) # if on windows use this

        # The name of the image file to annotate
        file_name = os.path.join(os.path.dirname(__file__), "Screenshot.png")

        #take_screenshot(x, y, num)
        #file_name = os.path.join(os.path.dirname(__file__), "Screenshot" + str(num) + ".png")

        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.text_detection(image=image)

        labels = ''
        try:
            labels = response.text_annotations[0].description.strip().split('\n')
        except:
            time.sleep(4)
            continue

        print(labels)
        for label in labels:
            label = label.lower()
            if label not in fortnite_database.history:
                # insert it in the front to reduce checking time
                fortnite_database.history.insert(0, label)
                process_text(label, fortnite_database)

        #subprocess.call(["afplay", "/System/Library/Sounds/Funk.aiff"])
        # this time.sleep() kinda monitors how often the screen shot should be taken
        # almost like update rate of the program
        time.sleep(3)
        num += 1

    fortnite_database.conn.close()
    if username in fortnite_database.dead or username.replace('_', ' ') in fortnite_database.dead:
        print("You died.")
    print("Finished!")

if __name__ == "__main__":
    main()