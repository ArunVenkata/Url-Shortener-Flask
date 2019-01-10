from werkzeug.security import generate_password_hash
import sqlite3 as sql
import httplib2
import random as r


class HashURLStore:

    def __init__(self, url):
        self.__url = url

    def __init__sql(self):
        self.connection = sql.connect("data.db")
        self.cursor = self.connection.cursor()

    def __disable__sql(self, commit=False):
        if commit:
            self.connection.commit()
        self.connection.close()

    def __url_exist_db_check(self, disable_sql=False):
        self.__init__sql()
        res = [x for x in self.cursor.execute("select * from urls where url=?", (self.__url,))]
        if disable_sql:
            self.__disable__sql()
        return False if len(res) == 0 else True

    def __url_exist_check(self):
        try:
            resp = httplib2.Http().request(self.__url, 'HEAD')
            assert int(resp[0]['status']) < 400
            return int(resp[0]['status'])
        except AssertionError:
            return "NOT FOUND!"

    def __get_hash(self):
        return generate_password_hash(self.__url, method="pbkdf2:sha256:1000")

    def hash_url_store(self):
        self.__init__sql()

        hsh = self.__get_hash()

        if not self.__url_exist_db_check():
            self.cursor.execute("INSERT INTO urls(url, url_hash) values(?, ?)", (self.__url, hsh,))
            self.cursor.execute("INSERT INTO url_codes(url, url_code) values(?, ?)", (self.__url, hsh[19:27],))

        # if self.__url_exist_check() == "NOT FOUND!":
        #     raise AssertionError("URL NOT FOUND!")

        li_codes = [x[0] for x in self.cursor.execute("SELECT url_code from url_codes where url=?", (self.__url,))]

        self.__disable__sql(commit=True)

        return li_codes[0]

    def get_url(self, url_code):
        self.__init__sql()
        li = [x[0] for x in self.cursor.execute("SELECT url FROM url_codes where url_code=?", (url_code, ))]
        self.__disable__sql()
        return li[0]
