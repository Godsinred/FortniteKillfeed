import requests
import time
import sqlite3
import PriorityQueue

class FortniteTracker:
    """
    Class which handles all interaction with the Fortnite sqlite3 database

    """
    def __init__(self, username, key, thread_lock):
        """
        initialize the class
        :param username: the username of the current user
        :param key: an API key attained from google-cloud services
        :param thread_lock: A singleton containing the lock for the current multithreaded process
        """
        self.header = {'TRN-Api-Key': key}
        # check_same_thread is set to false so the multi thread can write to the db, default is true which doesn't allow
        # other threads to write to the db to avoid data corruption. writing operations should be serialized
        self.conn = sqlite3.connect("fortnite_feed.sqlite", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.priority_queue = PriorityQueue.PriorityQueue()
        # all the unique lines that have been read
        self.history = []
        # all the people currently alive in the game
        self.alive = []
        # all the dead people
        self.dead = []
        # the person who is playing the game
        self.user = username

        # a lock to make sure the database cursors don't update and access from different threads
        self.thread_lock = thread_lock

        cmd = """
        PRAGMA encoding='UTF-8';
        DROP TABLE IF EXISTS CurrentStats;
        CREATE TABLE CurrentStats(
        user_id INTEGER PRIMARY KEY NOT NULL,
        username TEXT,
        platform TEXT,
        current_kills INTEGER,
        current_weapon TEXT,
        total_wins INTEGER,
        total_matches INTEGER,
        win_percent FLOAT,
        total_kills INTEGER,
        kd FLOAT,
        alive INTEGER
        );
        
        
        CREATE TABLE IF NOT EXISTS WeaponStats(
        player_id INTEGER PRIMARY KEY NOT NULL,
        username TEXT,
        rifle_kills INTEGER,
        shotgun_kills INTEGER,
        explosives_kills INTEGER,
        sniper_kills INTEGER,
        smg_kills INTEGER,
        pistol_kills INTEGER,
        pickaxe_kills INTEGER
        );
        """

        """
        CREATE TABLE IF NOT EXISTS Players(
        player_id INTEGER PRIMARY KEY NOT NULL,
        username TEXT);
        """
        try:
            self.thread_lock.acquire(True)
            self.cur.executescript(cmd)
        finally:
            self.thread_lock.release()

    def thread_safe_execute(self, cmd, args=()):
        """
        executes any database commands in a thread safe manner to prevent cursors in different threads from accessing the
        same data at the same time
        :param cmd: a str containing the sql command to be executed
        :param args: any arguments that need to be passed into the sql command
        :return:
        """
        try:
            self.thread_lock.acquire(True)
            if not args:
                self.cur.execute(cmd)
            else:
                self.cur.execute(cmd, args)
            self.conn.commit()
        finally:
            self.thread_lock.release()

    def add_player(self, name):
        """
        Adds a player info into the db
        :param name: a string, player's name
        :return: nothing
        """
        try:
            self.thread_lock.acquire(True)
            self.cur.execute("""SELECT * FROM Players WHERE username='{}'""".format(name))
            data = self.cur.fetchall()
            if len(data) == 0:
                cmd = """INSERT OR IGNORE INTO Players(username) VALUES(?)"""
                self.thread_safe_execute(cmd, (name,))
        finally:
            self.thread_lock.release()

    def add_weapon_stats(self, name):
        """
        Adds a player's weapon stats into the db
        :param name: a string, player's name
        :return: nothing
        """
        try:
            self.thread_lock.acquire(True)
            self.cur.execute("""SELECT * FROM WeaponStats WHERE username='{}'""".format(name))
            data = self.cur.fetchall()
            if len(data) == 0:
                cmd = """INSERT OR IGNORE INTO WeaponStats(username, shotgun_kills, pistol_kills, pickaxe_kills, 
                explosives_kills, sniper_kills, rifle_kills, smg_kills) VALUES(?,?,?,?,?,?,?,?)"""

                self.cur.execute(cmd, (name, 0, 0, 0, 0, 0, 0, 0))
        finally:
            self.thread_lock.release()

    def update_weapon_stats(self, username, current_wep):
        """
        Updates the weapon stats when someone got killed
        :param username: a string, the killer's name
        :param current_wep: a string, the weapon that the killer uses
        :return: nothing
        """
        weapons = ['explosives', 'sniper', 'rifle', 'smg', 'shotgun', 'pistol', 'pickaxe']
        try:
            self.thread_lock.acquire(True)
            if current_wep in weapons:
                cmd = """UPDATE WeaponStats SET {}_kills=({}_kills+1) 
                        WHERE username="{}"
                        """.format(current_wep, current_wep, username)
                self.cur.execute(cmd)
                self.conn.commit()
        except:
            print("Can't update weapon stats: for", username)

        finally:
            self.thread_lock.release()


    def update_db(self, line, way, current_wep=None):
        """
        Updates the db for the format killer / way / dead_guy / possible wep
        :param line: one of the many possible lines of text that is received from the google vision api
        :param way: the way the guy died
        :param current_wep: the current weapon of the person
        :return: nothing
        """
        print('here 5')
        if current_wep == None:
            index = line.find(way)
            dead_guy = line[0:index].strip()

            # extra validation to make sure that the same lines doesn't get processed again due to an inaccurate
            # return from the google vision api
            if dead_guy in self.dead:
                return

            if dead_guy in self.alive:
                self.alive.remove(dead_guy)
                cmd = r"UPDATE CurrentStats SET alive=0 WHERE username='{}'".format(dead_guy)
                self.thread_safe_execute(cmd)

            print("died: " + dead_guy)
            self.dead.insert(0, dead_guy)
            # self.add_player(dead_guy)
            self.add_weapon_stats(dead_guy)

        else:
            if way == "eliminated":
                index = line.find("eliminated")
                # for the rare case that finally appears in solos
                if "finally" in line[index - 8:index]:
                    line = line[:index - 8] + line[index:]
                    index = line.find("eliminated")
                    killer = line[0:index].strip()
                    dead_guy = line[(index + 10):].strip()
                else:
                    killer = line[0:index].strip()
                    index1 = line.find("with")
                    if index1 == -1:
                        dead_guy = line[(index + 10):].strip()
                        current_wep = "NA"
                    else:
                        dead_guy = line[(index + 10):index1].strip()
                        current_wep = line[(index1 + 7):].strip()
            else:
                index = line.find(way)
                killer = line[0:index-1].strip()
                dead_guy = line[(index + 10):].strip()

            print('here 6')
            # extra validation to make sure that the same lines doesn't get processed again due to an inaccurate
            # return from the google vision api because the same person can't die twice
            if dead_guy in self.dead:
                print('here 9')
                return

            if dead_guy in self.alive:
                self.alive.remove(dead_guy)
                print('here 10')
                cmd = r"UPDATE CurrentStats SET alive=0 WHERE username='{}'".format(dead_guy)
                self.thread_safe_execute(cmd)
                print('here 11')

            self.dead.insert(0, dead_guy)
            print('here 12')
            # self.add_player(dead_guy)
            print('here 13')
            self.add_weapon_stats(dead_guy)
            print('here 7')
            # checks to see if the player has been added to the db before
            if killer not in self.alive:
                self.alive.insert(0, killer)
                # self.add_player(killer)
                self.add_weapon_stats(killer)
                cmd = """INSERT INTO CurrentStats(username, platform, current_kills, current_weapon, total_wins, 
                total_matches, win_percent, total_kills, kd, alive) VALUES(?,?,?,?,?,?,?,?,?,?)"""

                self.thread_safe_execute(cmd, (killer, "N/A", 1, current_wep, 0, 0, 0, 0, 0, 1))
                self.priority_queue.push_high(killer)
                self.update_weapon_stats(killer, current_wep)
            # this means he already has a kill and we just need to update the db with his kill
            else:
                cmd = r"""UPDATE CurrentStats SET current_kills=(current_kills+1), current_weapon='{}' WHERE username='{}'""".format(
                    current_wep, killer)
                self.thread_safe_execute(cmd)
                self.update_weapon_stats(killer, current_wep)
            print('here 8')

    def get_api_stats(self, username, platform, priority_level, original_username=None):
        """
        Makes a connection to the fortnite tracker api (limit 1 request per 2 seconds) <<<<----- not currently checked in the program
        :param username: the usename of the person to get stats for
        :param platform: the platform the player is on. currently only checks for PC
        :param priority_level: what queue we are currently checking
        :return: a tuple of the data to be used to store in the db
                 format of (total_wins, total_matches, win_percent, total_kills, kd)
        """
        epic = ''
        found_epic = False
        print("looking up: " + username + " on " + platform)
        if "[epic]" in username[:6]:
            print("found an epic emplyee, looking up username - [epic]")
            epic = 7
            found_epic = True
        elif "[epic_cs]" in username[:9] or "[epic cs]" in username[:9] :
            print("found an epic emplyee, looking up username - [epic_cs]")
            epic = 10
            found_epic = True

        try:
            lookup_username = username
            if found_epic:
                lookup_username = username[epic:].strip()

            r = requests.get("https://api.fortnitetracker.com/v1/profile/" + platform + '/' + lookup_username,
                             headers=self.header)
            data = r.json()
            stats = data["lifeTimeStats"]
            # returns all the data needed to enter in the
            # total_wins, total_matches, win_percent, total_kills, kd
            temp_username = ''
            if priority_level != "last":
                temp_username = username
            else:
                temp_username = original_username

            self.thread_safe_execute(r"""UPDATE CurrentStats SET total_wins={}, total_matches={}, win_percent={}, total_kills={}, kd={},
                        platform='{}', username='{}'
                        WHERE username='{}'""".format(int(stats[8]["value"]), int(stats[7]["value"]),
                        float(stats[9]["value"][:-1]), int(stats[10]["value"]), float(stats[11]["value"]), platform, username, temp_username))
        except KeyError:
            # if this gets returned that means that the user wasn't found and requests threw and error

            if priority_level == "high":
                self.priority_queue.push_med(username)
            elif priority_level == "med":
                self.priority_queue.push_low(username)
            elif priority_level == "low":
                # just does one last check to see if spaces in the username can be switched with underscores since that
                # is one of the most common errors
                if ' ' in username:
                    new_username = username.replace(' ', '_')
                    self.get_api_stats(new_username, "pc", "last", username)
            elif priority_level == "last":
                # no more checking after and leaves username as is
                print(": Can't find/fix username: {}".format(original_username))
                cmd = r"UPDATE CurrentStats SET platform='Not Found' WHERE username='{}'".format(original_username)
                self.thread_safe_execute(cmd)
        except:
            print("Possible error from looking up nothing in the api.")