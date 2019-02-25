#https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta

import sqlite3

class DatabaseManager:
    def __init__ (self, file_loc):
        self.conn = sqlite3.connect(file_loc)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, column_name, column_type):
        """
        Creates a new table with a name and the first column
        """
        with self.conn:
          if not self.doesTableExist(table_name):
              self.cursor.execute("CREATE TABLE %s (%s %s PRIMARY KEY)" % (table_name, column_name, column_type))
              self.conn.commit()
              return True
          else:
                return False

    def doesTableExist(self, table_name):
        try:
            self.cursor.execute("SELECT * FROM sqlite_master WHERE name = '%s' AND type = 'table'" % table_name)
            if self.cursor.fetchone()[1] == table_name:
                return True
            else:
                #print("Table already exists")
                return False
        except sqlite3.Error as er:
            print 'er:', er.message
            return False

    def create_table_list(self,table_name,column_name_list,column_type):
        self.create_table(table_name,column_name_list[0],column_type)
        for i in range(1,len(column_name_list)):
            self.add_column(table_name,column_name_list[i],'string')


    def add_column(self, table_name,column_name, column_type):
        try:
            self.cursor.execute("ALTER TABLE %s ADD COLUMN %s %s" % (table_name,'"{}"'.format(column_name) ,column_type))
            return True
        except sqlite3.Error as er:
            print 'er:', er.message
            return False

    def add_row_list(self, table_name, column_arr, row_arr):
        with self.conn:
            self.cursor.execute("INSERT OR IGNORE INTO %s (%s) VALUES(?)" % (table_name,'"{}"'.format(column_arr[0])), (row_arr[0],))
            for i in range(1,len(column_arr)):
                self.cursor.execute("UPDATE %s SET %s='%s' WHERE %s='%s'" % (table_name, '"{}"'.format(column_arr[i]), row_arr[i], column_arr[0], row_arr[0]))

    def clear_table(self, table_name):
        with self.conn:
                self.cursor.execute("DELETE FROM %s" % table_name)

    def return_table(self, table_name):
        try:
            self.cursor.execute("SELECT * FROM %s" % table_name)
            return self.cursor.fetchall()
        except sqlite3.Error as er:
            print 'er:', er.message
            return False
