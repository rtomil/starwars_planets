import psycopg2
from psycopg2 import extras
import requests
import math
from flask import request, redirect, session
import os
import urllib


urllib.parse.uses_netloc.append('postgres')
url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
connection = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


def logger():
    if 'option' in request.form:
        if request.form['option'] == 'logout':
            username = None
            user_id = None
            user_info = {'username': None, 'user_id': None}
    else:
        username = request.form['username']
        for i in username:
            if i.isspace():
                username = False
                break
        if 'password' in request.form:
            password = request.form['password']
            for i in password:
                if i.isspace():
                    password = False
                    break
        else:
            password = False
        if (username and password) is not False:
            if request.form['type'] == 'register':
                user_id = registration(username, password)
                print(user_id)
                if user_id is not False:
                    user_info = {'username': username, 'user_id': user_id}
                else:
                    user_info = None
            else:
                user_info= inlogger(username, password)
        else:
            user_info = None
    return user_info

def get_planets(url=None):
    planet_dict = {}
    planet_list = []
    if url is None:
        planet_json = requests.get('https://swapi.co/api/planets/').json()
    else:
        planet_json = requests.get(url).json()
    for i in planet_json['results']:
        planet_dict.update({i['name']: {'name': i['name'],
                            "diameter": int(i['diameter'])/1000 if i['diameter'] != 'unknown' else 'unknown',
                            "climate": i['climate'],
                            'terrain': i['terrain'],
                            'surface_water': i['surface_water']+' %' if i['surface_water'] != 'unknown' else 'unknown',
                            'population': millify(i['population']) if i['population'] != 'unknown' else 'unknown',
                            'residents': i['residents'],
                            'id': i['url'].replace('http://swapi.co/api/planets/', '').replace('/', '')}})
    planet_list.append(planet_dict)
    planet_list.append(planet_json['next'])
    planet_list.append(planet_json['previous'])
    return planet_list


def millify(n):
    millnames = ['',' Thousand',' Million',' Billion',' Trillion']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


def cookiemaker(user_id):
    print(user_id)
    print(type(user_id))
    if type(user_id) is list:
        print('WWWWWAAAAAAAAAAAAAAAAAAAAAAA')
        user_id = user_id[0]['id']
        print(user_id)
    print(user_id)
    sql = """SELECT planet_name, times_voted FROM planet_votes WHERE user_id = %s;"""
    data = (user_id,)
    user_votes = executor(sql, data)
    print(request.cookies)

    for key, value in request.cookies.items():
        cookie_user_id = int(key.split('+')[0])
        if cookie_user_id == user_id:
            planet_name = key.split('+')[1]
            times_voted = value.split('+')[0]
            planet_id = value.split('+')[1]
            inlist = False
            if user_votes != []:
                for i in user_votes:
                    if planet_name in i['planet_name']:
                        if (int(times_voted) == i['times_voted']) or (int(times_voted) < i['times_voted']):
                            pass
                        else:
                            sql = """UPDATE planet_votes SET times_voted = %s WHERE planet_id = %s AND user_id = %s RETURNING id;"""
                            data = (times_voted, planet_id, user_id)
                            executor(sql, data)
                        inlist = True
            if inlist is False:
                sql = """INSERT INTO planet_votes (planet_id, planet_name, user_id, times_voted) VALUES (%s, '%s', %s, %s) RETURNING id;"""
                data = (planet_id, planet_name, user_id, times_voted)
                executor(sql, data)


def vote_inserter(planet_id, key, user_id, times_voted):
    sql = """INSERT INTO planet_votes (planet_id, planet_name, user_id, times_voted) VALUES (%s, '%s', %s, %s) RETURNING id;"""
    data = (planet_id, key, user_id, times_voted)
    executor(sql, data)
    return True


def vote_upVader():
    sql = """SELECT planet_id, SUM(times_voted) FROM planet_votes GROUP BY planet_id;"""
    result = executor(sql)
    return result


def registration(username, password):
    try:
        sql = """INSERT INTO users (username, password) VALUES ('%s', '%s') RETURNING id;"""
        data = (username, password)
        result = executor(sql, data)
    except psycopg2.IntegrityError:
        result = False
    result = result[0]['id']
    return result


def executor(sql, data=None):
    conn = connect_to_DB()
    conn.autocommit = True
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if data is not None:
        cur.execute(sql % data)
    else:
        cur.execute(sql)
    return cur.fetchall()


def connect_to_DB():
    """Conects to my database. Yes my friend, i have a database."""
    # setup connection string
    connect_str = "dbname='starwars' user='richter' host='localhost' password='richter123ads'"
    try:
        return psycopg2.connect(connect_str)
    except:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print("or STFU I KNOW!")


def inlogger(username, password):
    conn = connect_to_DB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""SELECT id, username, password FROM users WHERE username = '%s';""" % (username,))
        result = cur.fetchall()
        user_info = {'username': result[0]['username'], 'user_id': result[0]['id']}
        if password != result[0]['password']:
            user_info = False
    except:
        user_info = False
    return user_info


def vote_statistics(user_id):
    sql = """SELECT planet_name times_voted WHERE user_id = %s;"""
    data = (user_id,)
    result = executor(sql, data)
    return result