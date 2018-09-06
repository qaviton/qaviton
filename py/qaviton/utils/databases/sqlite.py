import sqlite3


class DataBase:
    """
    a very simple implementation
    to create local SQLite database connection
    specified by db_file

    you can integrate your database with your custom commands class
    example usage:
        class command:
            get_users = '''SELECT user_id, password FROM users;'''
            get_user_by_user_id = '''SELECT user_id, password FROM users WHERE user_id = '{}';'''
            get_user_by_id = '''SELECT user_id, password FROM users WHERE id = '{}';'''
            get_last_user = '''SELECT user_id, password FROM users ORDER BY ID DESC LIMIT 1'''
            add_user = '''INSERT INTO users (user_id, password) VALUES ('{}', '{}');'''
            drop_table = '''DROP TABLE IF EXISTS {};'''
            create_users_table = '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id text,
                password text);'''

        # preferably use 'with' to automatically commit and close the connection
        with DataBase('db') as db:
            db.command = command
            db.execute(db.command.drop_table.format('users'))
            db.execute(db.command.create_users_table)
            db.execute(db.command.add_user.format('id123', 'password1'))

        db = DataBase('db')
        db.command = command
        db.execute(db.command.add_user.format('id777', 'password1'))
        user1 = db.execute(db.command.get_user_by_id.format('id123'))
        user2 = db.execute(db.command.get_user_by_id.format('id777'))
        db.commit()
        db.close()
    """

    def __init__(self, db_file: str, commands=None):
        """ create database connection
        :param db_file: path of db file
        :param commands: custom useful commands
        """
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.version = sqlite3.version
        self.command = commands

    def __enter__(self):
        return self

    def __exit__(self, *tp):
        self.commit()
        self.close()

    def __call__(self, command):
        """:rtype: list"""
        return self.execute(command)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def execute(self, command):
        """:rtype: list"""
        return self.cursor.execute(command).fetchall()

    def export_table_to_file(self, table, file, titles, permission='w'):
        """ export an entire table to a file

        :param table: table name
        :param file: path to export
        :param titles: table titles
        :param permission: probably write
        """
        self.cursor.execute("select * from {}".format(table))
        table_list = self.cursor.fetchall()
        with open(file, permission) as f:
            f.write(','.join(titles) + '\n')
            for i in table_list:
                s = []
                for a in i:
                    s.append(str(a))
                f.write(','.join(s) + '\n')