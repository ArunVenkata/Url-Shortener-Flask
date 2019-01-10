import sqlite3 as sql


class URLFunctions:
    def __init__(self, url_code):
        print("URL: ", url_code)
        self.__url_code = url_code

    def __init__sql(self):
        self.connection = sql.connect("data.db")
        self.cursor = self.connection.cursor()

    def __disable__sql(self, commit=False):
        if commit:
            self.connection.commit()
        self.connection.close()

    def get_url(self):
        self.__init__sql()
        li = [x[0] for x in self.cursor.execute("SELECT url FROM url_codes where url_code=?", (self.__url_code,))]
        print(li)
        self.__disable__sql()
        return li[0]
