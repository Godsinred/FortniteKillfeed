username = "[epic] Godsinred"
if "[epic]" in username[:6]:
    username = username.replace("[epic]", '').strip()

print(username)
current_wep = 'rifle (53 m)'
print(current_wep[:-6])
exit()
import sqlite3
current_wep = 'smg'
username = 'wonkals'
cmd = r"""UPDATE WeaponStats SET {}_kills=({}_kills+1) 
WHERE username='{}'""".format(current_wep, current_wep, username)
conn = sqlite3.connect("fortnite_feed.sqlite")
cur = conn.cursor()
cur.execute(cmd)
conn.commit()
cur.execute("SELECT * FROM WeaponStats")
print(cur.fetchall())
import pyautogui
x, y = pyautogui.size()
pic = pyautogui.screenshot(region=(0, y * 0.6, x * 0.33, y * 0.3))
pic.save("Screenshot.png")
exit()
import psutil
for pid in psutil.pids():
    p = psutil.Process(pid)
    # print(p.name())
    if p.name() == "FortniteClient-Win64-Shipping_BE.exe":
        print("Called By Python:"+ str(p.cmdline()))

from screeninfo import get_monitors
for m in get_monitors():
    print(str(m))

exit()
import requests
try:
    platform = "pc"
    username = "Godsinred1"
    API_KEY = {"TRN-Api-Key": "e7462887-33cc-44d2-bb7d-ea3796b3231f"}
    r = requests.get("https://api.fortnitetracker.com/v1/profile/" + platform + '/' + username, headers=API_KEY)
    data = r.json()
    stats = data["lifeTimeStats"]
    # returns all the data needed to enter in the
    # total_wins, total_matches, win_percent, total_kills, kd
    print(stats[8]["value"], stats[7]["value"], stats[9]["value"], stats[10]["value"], stats[11]["value"])

except KeyError:
    print("can't find username")


import time
time.sleep(2)
import pyautogui
x, y = pyautogui.size()
pic = pyautogui.screenshot(region=(0, y * 0.7, x * 0.3 , y * 0.3))
pic.save("Screenshot.png")

# from difflib import SequenceMatcher
# print(SequenceMatcher(None, a, b).ratio())
print("Ĺαšt-ÐεNz ツ")
print("미움.")

time = time.time()
print(time)
import sqlite3
import requests
platform = "pc"
username = "ωμega"
API_KEY = {"TRN-Api-Key": "e7462887-33cc-44d2-bb7d-ea3796b3231f"}
r = requests.get("https://api.fortnitetracker.com/v1/profile/" + platform + '/' + username, headers=API_KEY)
data = r.json()
stats = data["lifeTimeStats"]
# returns all the data needed to enter in the
# total_wins, total_matches, win_percent, total_kills, kd
print(stats[8]["value"], stats[7]["value"], stats[9]["value"], stats[10]["value"], stats[11]["value"])

conn = sqlite3.connect("fortnite_feed.sqlite")
cur = conn.cursor()

# sqlite3 db_name
# .tables
# .schema table_name
# this database is responsible for holding all the players in the game
cur.execute("""DROP TABLE IF EXISTS Game""")
cur.execute("""CREATE TABLE Game(
    user_id INTEGER PRIMARY KEY NOT NULL,
    username TEXT,
    current_kills INTEGER,
    current_weapon TEXT,
    total_wins INTEGER,
    total_matches INTEGER,
    win_percent FLOAT,
    total_kills INTEGER,
    kd FLOAT,
    alive INTEGER
    );""")

killer = "미움."
cur.execute("""INSERT INTO Game(username, current_kills, current_weapon, total_wins, total_matches, win_percent,
            total_kills, kd, alive) VALUES(?,?,?,?,?,?,?,?,?)""", (killer, 3, 'bag', 4, 5, 0.8, 7, 1.5, 1))
conn.commit()
cmd = r"""UPDATE Game SET current_kills=(current_kills+1), current_weapon='{}' WHERE username='{}'""".format("michaels dick", killer)
print(cmd)
cur.execute(cmd)
conn.commit()
cmd = r"UPDATE Game SET alive=0 WHERE username='{}'".format(killer)
cur.execute(cmd)
conn.commit()

data = cur.execute("SELECT * FROM Game")
names = list(map(lambda x: x[0], data.description))
print("{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}{:20s}".format(
    "user_id", "username", "current_kills", "current_weapon", "total_wins", "total_matches", "win_percent",
    "total_kills", "kd", "alive"))
data = cur.fetchall()
for d in data:
    print("{:<20d}{:20s}{:<20d}{:20s}{:<20d}{:<20d}{:<20f}{:<20d}{:<20f}{:<20d}".format(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9]))

