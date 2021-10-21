import pymysql.cursors
import pymysql
import configparser
import os


class MySQLDB:
    def __init__(self, config_path='config.conf') -> None:
        config = configparser.RawConfigParser()
        config.read(config_path)
        config_dict = dict(config.items('user_info'))

        self.connection = pymysql.connect(host=config_dict.get("host"),
                                        user=config_dict.get("username"),
                                        password=config_dict.get("password"),
                                        database=config_dict.get("database"))

    def execute(self, sql, data=None):
        """
        execute Execute sql 

        Args:
            sql (string): Sample:  "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            data ([type], optional): [description]. Defaults to None.

        Raises:
            ValueError: [description]

        Returns:
            [type]: [description]
        """
        with self.connection.cursor() as cursor:        
            cursor.execute(sql)
            result = cursor.fetchall()
            return result


class User:
    def __init__(self, username, email, password) -> None:
        self.username = username
        self.email = email
        self.password = password


class UserDatabase:
    def __init__(self) -> None:
        self.client = MySQLDB()

    def _create_table(self, create_table_sql=None, sql_path='mysql_db', sql_file_name='users_table.sql'):
        if not create_table_sql:
            with open(os.path.join(sql_path, sql_file_name), 'r') as f:
                create_table_sql = f.read()
            
        self.client.execute(create_table_sql)

    def insert(self, user_obj, insert_table='users', insert_sql=None):
        username = user_obj.username
        email = user_obj.email
        password = user_obj.password

        basic_user_info = [username, email, password]

        table_list = self.client.execute("show tables")
        table_exist = False
        if len(table_list) >0:
            table_list = [x[0] for x in table_list]
            if insert_table in table_list:
                table_exist = True

        if not table_exist:
            print("table: {} doesn't exist, now to create it.".format(insert_table))
            self._create_table()

        insert_sql = "insert into `users` (`username`, `email`, `password`) values ('%s', '%s', '%s')" % tuple(basic_user_info)
        self.client.execute(insert_sql)
        
        print("Data insert finished.")

    def search_user(self, username):
        query_sql = "select * from users where username = '%s'" % username

        result = self.client.execute(query_sql)
        
        if len(result) == 0:
            return None, None, None
        elif len(result) > 1:
            print("Get over 2 records in MYSQL, please check!")
        else:
            username = result[0][1]
            email = result[0][2]
            password = result[0][3]
        
            return username, password, email

    def check_user(self, username, password=None, email=None):
        """
        check_user Check provided username exist in DB or not, also should check with password and email, if username is not correct, then 

        Args:
            username ([type]): [description]
            password ([type]): [description]
            email ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        username_db, password_db, email_db = self.search_user(username=username)

        msg = ""
        if username_db != username:
            msg += "username is not correct! "

        if password and password_db != password:
            if not msg:
                msg = "password is not correct! "
        
        if email and email_db != email:
            if not msg:
                msg = "Email is not correct!"
        
        if msg:
            return False, msg
        else:
            return True, msg


if __name__ == '__main__':
    user_data = UserDatabase()
    user_obj = User("lugq", '1131298218@qq.com', 'lugq1990')

    user_data.insert(user_obj)
    user_data.search_user("lugq")

    print(user_data.check_user('lugqd', 'lugq1990'))
