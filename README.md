##### final-project-cookiemonster created by GitHub Classroom

# Fortnite Tracker

  The program creates a real time tracker in Fortnite Battle Royal. The program will collect the data from the killfeed and give the user the live time stats of the players currently playing the same game as them. The data would be what weapon the players are using and which player killed who.
  
## Short Video Of The Program

Click below to download and watch!
[![Watch the video](https://amp.businessinsider.com/images/5c366de02a5b7442d75cda92-750-563.jpg)](assets/Fortnite_killfeed_beta_demo.mp4)

## Getting Started

  The program was coded using PyCharm CE on mac.

### Prerequisites

You will have to install following modules to be able to run the code.
For pyautogui refer to http://pyautogui.readthedocs.io/en/latest/install.html to install into your mac/window.

```
Pip3 install
requests
threading
subprocess
nltk
difflib
pyautogui
sqlite3
requests
google-cloud
google-cloud-vision
graphing
dash
dash_core_components
dash_html_components
dash.dependencies
plotly
plotly.graph_objs
```

### APIs

  This program needs two APIs, GoogleAPI and Fortnite API.

#### Fortnite API

  Fortnite API you would have to go to https://fortnitetracker.com/site-api and get an API key.

  On the Main.py, line 14, replace the API_KEY to given key.

```
Main.py - line 14
  API_KEY = "THIS WOULD BE YOUR API_KEY"
```

  On the unittesting.py, line 11, replace the TRN-Api-Key to given key.

```
unittesting.py - line 11
          self.header = {'TRN-Api-Key': "THIS WOULD BE YOUR API_KEY"}
```

#### Google Cloud Vision API

  Google Cloud Vision API can be obtained from the following website https://cloud.google.com/vision/docs/libraries#client-libraries-install-python.
 
  Save the api.json (eg, account_key.json) to the folder and get the path of the folder.
  Your path would end with json file. For example /Users/mypath/Desktop/GoogleAPI/account_key.json
  
  On Main.py , line 215, replace the path.
```
Main.py - line 215
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r' YOUR PATH HERE '
```

## Running the tests

There is a automated unit test class in unittesting.py. 
This class goes over each functions and checks if there is any error.
Unit tests are fast, reliable and point us in the exact direction of the bug.

### Break down the unit test class

Each functions in unittesting tests one functions.
```
def test_add_player(self):
        self.fortnite_database.add_player("Dark")
        cmd = """SELECT * FROM Players WHERE username='Dark'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(1, "Dark")])
```
test_add_player tests the adding the new player("Dark") into the sql database and checks if the data in sql is correct. 


```
    def test_add_weapon_stats(self):
        self.fortnite_database.add_player("Dark")
        self.fortnite_database.add_weapon_stats("Dark")
        cmd = """SELECT * FROM WeaponStats WHERE username='Dark'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(1, "Dark", 0, 0, 0, 0, 0, 0)])
```
test_add_weapon_stats tests if weapon is correctly adding it when a new player is being added into the database. It checks if the added weapon for existing player is correctly added.


```
    def test_update_weapon_stats(self):
        self.fortnite_database.add_player("Dark")
        self.fortnite_database.add_weapon_stats("Dark")
        self.fortnite_database.update_weapon_stats("Dark", "shotgun")
        cmd = """SELECT * FROM WeaponStats WHERE username='Dark'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(1, "Dark", 1, 0, 0, 0, 0, 0)])
```
test_update_weapon_stats checks if the weapon of the eixisting player updates correctly. We tries to add player name "Dark" by using add_player fucntion, and updates his weapon stats with update_weapon_stats function with "shotgun". Lastly, we compare it with (1, "Dark", 1, 0, 0, 0, 0, 0). 


```
    def test_update_db(self):
        self.fortnite_database.update_db("Manduin Wyrnn bludgeoned Cupidie", "bludgeoned", "pickaxe")
        cmd = """SELECT * FROM CurrentStats WHERE username='Manduin Wyrnn'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(2, "Manduin Wyrnn", "N/A", 1, "pickaxe", 0, 0, 0, 0, 0, 1)])
```
test_update_db checks if the weapon of the eixisting player updates correctly. We use the function update_db in fortnite_database class, and passes "Manduin Wyrnn bludgeoned Cupidie", "bludgeoned", "pickaxe". Which should update the killer, they way he died, who is dead and the possible weapon.


```
    def test_update_sentence(self):
        result = m.update_sentence("Manduin Wyrnn bludgeomed Cupidie")
        self.assertMultiLineEqual(result, "Manduin Wyrnn bludgeoned Cupidie")

        result = m.update_sentence("sphaerophoria shotaunned Stein72")
        self.assertMultiLineEqual(result, "sphaerophoria shotgunned Stein72")
```
test_update_sentence checks if the program can get the right information from killfed. This checks if the sentence fixed correctly.


## Additional note

We also used multi threading in the background to update the database for efficiency.

## Built With

* [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) - The module used to take a screenshot
* [Natural Language Toolkit](https://www.nltk.org/) - To check the similarity of strings.
* [google-cloud](https://googlecloudplatform.github.io/google-cloud-python/) - The cloud use to store screenshots
* [plotly](https://plot.ly/) - Used for data visualization via the Web


## Authors

* **Brian Caulfield**  ------ [brotaku13](https://github.com/brotaku13)
* **Johnny Ishii**     ------ [Godsinred](https://github.com/Godsinred)
* **Sheng Lo**         ------ [shenglo1](https://github.com/shenglo1)
* **Alice Hyejin Kim** ------ [alice2short](https://github.com/alice2short)

