# chatgpt hard carried lol

import time
import json
import base64
import random
import sqlite3


class jewcord_db:
    def __init__(self):
        self.connect = sqlite3.connect("jewcord.db", check_same_thread=False)
        self.cursor = self.connect.cursor()

        try:
            table_structure = '''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    discriminator INTEGER,
                    servers INTEGER,
                    avatar TEXT,
                    created_at DATETIME,
                    friends TEXT,
                    dms TEXT,
                    email TEXT,
                    phone TEXT,
                    password TEXT,
                    token TEXT
                )
            '''

            self.cursor.execute(table_structure)

            table_structure = '''
                CREATE TABLE guilds (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    channels TEXT,
                    roles TEXT,
                    members TEXT,
                    bans TEXT,
                    log TEXT,
                    invites TEXT,
                    image TEXT,
                    emojis TEXT,
                    owner TEXT
                )
            '''

            self.cursor.execute(table_structure)

            table_structure = '''
                CREATE TABLE images (
                    id INTEGER PRIMARY KEY,
                    base64 TEXT
                )
            '''

            self.cursor.execute(table_structure)

            table_structure = '''
                CREATE TABLE utils (
                    finder INTEGER PRIMARY KEY,
                    serverid INTEGER,
                    userid INTEGER
                )
            '''

            self.cursor.execute(table_structure)

            table_structure = '''
                CREATE TABLE invites (
                    id INTEGER PRIMARY KEY,
                    link TEXT,
                    sid INTEGER,
                    time DATETIME,
                    cnt INTEGER
                )
            '''

            self.cursor.execute(table_structure)

            insert_stmt = '''
                INSERT INTO utils (finder, serverid, userid)
                VALUES (?, ?, ?)
            '''

            self.cursor.execute(insert_stmt, (0, 0, 0))
            self.commit()

        except Exception as e:
            print(e)


    # def auth(self, server, user, ):

    def commit(self):
        self.connect.commit()

    def find_server_channels(self, id):
        res = self.cursor.execute(f"SELECT channels FROM guilds WHERE id={id}")
        channels = res.fetchone()[0]

        return channels

    def find_channel(self, channels, id):
        return json.loads(channels)[str(id)]

    def new_message(self, sid, cid, data):
        res = self.cursor.execute(f"SELECT channels FROM servers WHERE id={sid}")
        channels = json.loads(res.fetchone()[0])

        channels[cid]["messages"].append(data)

        self.cursor.execute(f"UPDATE channels SET channels={json.dumps(channels)} FROM servers WHERE id={sid}")
        self.commit()

    def get_user(self, by, val):
        res = self.cursor.execute(f"SELECT * FROM users WHERE {by}={val}")
        data = res.fetchone()
        user = {
            "name": data[0],
            "id": data[11],
            "discriminator": data[1],
            "avatar": data[3],
            "created_at": data[4]
        }
        return user

    def login(self, email, pwd):
        res = self.cursor.execute(f"SELECT password, token FROM users WHERE email={email}")
        correct = res.fetchone()[0]
        token = res.fetchone()[1]

        if correct == pwd:
            return token
        return False

    def new_user(self, email, name, pwd):
        # name, discriminator, servers, avatar, created_at, friends, dms, email, phone, password, token, id
        token = self.random_token()
        disc = self.find_valid_disc(name)
        id = self.new_user_id()
        if disc is False:
            return False

        insert_stmt = '''
            INSERT INTO users (name, discriminator, servers, avatar, created_at, friends, dms, email, phone, password, token, id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Execute the INSERT statement with the values
        self.cursor.execute(insert_stmt, (name, disc, "[]", "default", time.time(), "[]", "[]", email, "", pwd, token, id))
        return token

    # generates a random token

    def random_token(self):
        hash_1 = str(base64.b64encode(str(int(time.time()) - 960548982).encode()))[1:].replace("'", "")
        hash_2 = str(base64.b64encode(str(random.getrandbits(256)).encode()))[1:].replace("'", "")

        return f"{hash_1}{hash_2}"

    # find if username is available

    def find_valid_disc(self, name):
        try:
            select_stmt = f'''
                SELECT * FROM users WHERE name = {name} ORDER BY disc ASC
            '''
            res = self.cursor.execute(select_stmt)
            res = res.fetchall()

            if res:
                if res[0][2] < 9999:
                    return res[0][2] + 1
                else:
                    return False
        except:
            # SQL being annoying
            return 0

    def new_user_id(self):
        select_stmt = '''
            SELECT userid FROM utils
        '''

        res = self.cursor.execute(select_stmt)
        res = res.fetchone()[0]

        update_stmt = f'''
            UPDATE utils SET userid = {res+1} WHERE finder = 0
        '''

        self.cursor.execute(update_stmt)

        self.commit()

        return res

    def new_guild_id(self):
        select_stmt = '''
            SELECT serverid FROM utils
        '''

        res = self.cursor.execute(select_stmt)
        res = res.fetchone()[0]

        update_stmt = f'''
            UPDATE utils SET serverid = {res + 1} WHERE finder = 0
        '''

        self.cursor.execute(update_stmt)

        self.commit()

        return res

    def new_server(self, name, owner):
        id = self.new_guild_id()
        channels = {
            "0": {
                "name": "general",
                "nsfw": False,
                "messages": []
            }
        }
        insert_stmt = '''
            INSERT INTO guilds (id, name, channels, roles, members, bans, log, invites, image, emojis, owner)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        self.cursor.execute(insert_stmt, (id, name, json.dumps(channels), "[]", "[]", "[]", "[]", "[]", "", "[]", owner))
        self.commit()
