import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from plotly.graph_objs import Bar, Layout
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import sqlite3 as sql
import threading


def connect():
    """
    Creates a connection to a sql database named fortnite_feed.sqlite
    :return: a cursor pointing to the database file
    """
    con = sql.connect('fortnite_feed.sqlite')
    cur = con.cursor()
    return cur

def generate_table(cur, thread_lock):
    """
    Generates an html table to display all alive players
    :param cur: a cursor to the database
    :param thread_lock: a thread lock global which prevents two threads from accessing the db at the same time
    :return: an html.Table object from the dash library... essentially a pythonic representation of an html table
    """
    headers = ['Username', 'Current kills', 'Platform', 'Current Weapon', 'Favorite Weapon', 'Total Wins', 'Total Matches', 'K/D']
    data = get_player_info(cur, thread_lock)

    return html.Table(
        #header
        [html.Tr([html.Th(col) for col in headers])] + 
        # Body
        [html.Tr([html.Td(stat) for stat in player]) for player in data]
    )

def generate_bar_graph(cur, thread_lock):
    """
    generates a plotly bar graph based on top ten players currently in the game.
    :param cur: a cursor to the database
    :param thread_lock: a thread lock global which prevents two threads from accessing the db at the same time
    :return: a plotly bar graph object
    """
    x, y = get_top_ten(cur, thread_lock)
    return {
        'data':[
            go.Bar(
                x=x,
                y=y,
                marker={
                    'color': '#397BFF',  # change this to change graph color
                    'line': {
                        'color': 'white',
                        'width':1.5
                    }
                }
            )
        ],
        'layout':{
            'plot_bgcolor':'transparent',
            'paper_bgcolor': 'transparent',
            'font': {
                'color': 'white',
                'font-size': '12px'
            },
            'yaxis': {'tickformat': ',d'}
        }
    }

def setup_layout(cur, app, thread_lock):
    """
    sets up the page layout for the dash dashboard including table positioning and bar graph positioning
    :param cur: a cursor to the database
    :param app: a reference to the current dash app
    :param thread_lock: a thread lock global which prevents two threads from accessing the db at the same time
    :return: void
    """
    app.layout = html.Div([  # total outside box

        html.Link(href='/assets/table.css', rel='stylesheet'),

        html.H1(
        children='Fortnite Kill Feed',
        style={
            'textAlign': 'center',
            'color': '#FFFDB9',
            'padding': '0px 0px 0px 0px'
            }
        ),

        html.Div([   # bar graph 
            dcc.Graph(id='players_bar',
                figure=generate_bar_graph(cur, thread_lock)
            )
        ], style={'display': 'inline', 'height': '25vh', 'width': '10vw', 'fontSize': 14}),

        html.Div(id='table_id', 
        style={'width': '100vw'}),

        dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
        )
    ])

def get_top_ten(cur, thread_lock):
    """
    retrieves the top ten players currently in the game
    :param cur: a cursor to the database
    :param thread_lock: a thread lock global which prevents two threads from accessing the db at the same time
    :return: a tuple containing two lists ([usernames], [kills])
    """
    cmd = """
    select username, current_kills from CurrentStats
    where alive=1
    order by current_kills desc
    limit 10
    """
    try:
        thread_lock.acquire(True)
        cur.execute(cmd)
    finally:
        thread_lock.release()

    data = cur.fetchall()

    usernames = []
    kills = []
    for stat in data:
        usernames.append(stat[0])
        kills.append(stat[1])
    
    return usernames, kills

def get_player_info(cur, thread_lock):
    """
    gets all player information from the database
    :param cur: a cursor to the database
    :param thread_lock: a thread lock global which prevents two threads from accessing the db at the same time
    :return: returns a list of lists. this format is used in constructing the html.Table object
    """
    cmd = """
    select username, current_kills, platform, current_weapon, total_wins, total_matches, kd from CurrentStats
    order by alive desc, current_kills desc
    """
    try:
        thread_lock.acquire(True)
        cur.execute(cmd)
    finally:
        thread_lock.release()

    data = cur.fetchall()
    if len(data) < 1:
        return []

    table_info = []
    for player_stat in data:
        player_info = list(player_stat)
        player_info.insert(4, get_favorite_weapon(player_info[0], cur, thread_lock))
        table_info.append(player_info)

    return table_info

def get_favorite_weapon(username, cur, thread_lock):
    """
    gets the favorite weapon of a given username. The favorite weapon is based on historical data about the player
    :param username: the username of a given player
    :param cur: a cursor to the database
    :param thread_lock: a thread lock global which prevents two threads from accessing the db at the same time
    :return: a string containing the favorite weapon as well as the number of kills that username has with that weapon
    """
    cmd = """
    select shotgun_kills, pistol_kills, pickaxe_kills, explosives_kills, sniper_kills, rifle_kills
    from WeaponStats
    where username="{}"
    """.format(username)
    try:
        thread_lock.acquire(True)
        cur.execute(cmd)
    finally:
        thread_lock.release()

    data = cur.fetchall()
    if len(data) == 0:
        return 'No Game Data'

    weapon_index = ['Shotgun', 'Pistol', 'Pickaxe', 'Explosions', 'Sniper Rifles', 'Rifles']
    try:
        max_stat = data[0][0]
        fav_weapon = '{} - {} kills'.format(weapon_index[0], max_stat)
        for index, stat in enumerate(data[0]):
            if stat > max_stat:
                max_stat = stat
                fav_weapon = '{} - {} kills'.format(weapon_index[index], stat)
        if max_stat == 0:
            return 'No Game Data'
    except:
        return 'No Game Data'

    return fav_weapon
        
def run_dash(thread_lock):
    """
    Runs the dash dashboard
    :param thread_lock: a thread lock global which prevents two threads from accessing the db at the same time
    :return:
    """
    cur = connect()
    app = dash.Dash(__name__, static_folder='assets')
    app.scripts.config.serve_locally=True
    app.css.config.serve_locally=True

    setup_layout(cur, app, thread_lock)

    """Updates the bar graph in 1 second intervals"""
    @app.callback(Output(component_id='players_bar', component_property='figure'),
                [Input(component_id='interval-component', component_property='n_intervals')])
    def update_graph_live(n):
        return generate_bar_graph(cur, thread_lock)

    """updates the table simultaneously with the bar graph"""
    @app.callback(Output('table_id', 'children'),
                [Input(component_id='interval-component', component_property='n_intervals')])
    def update_table_live(n):
        return generate_table(cur, thread_lock)

    """sets the flask server to serve static files from the assets folder"""
    @app.server.route('/assets/<path:path>')
    def static_file(path):
        static_folder = os.path.join(os.getcwd(), 'assets')
        return flask.send_from_directory(static_folder, path)


    app.run_server(port=8011)

if __name__ == '__main__':
    """
    used for debugging
    """
    lock = threading.Lock()
    run_dash(lock)