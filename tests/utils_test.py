import unittest
import sqlite3
import sys
from .. import utils

class TestUtilsMethods(unittest.TestCase):

    def test_create_connection(self):
        self.conn = sqlite3.connect(':memory:')

    def test_create_table():
        sql_table = """ CREATE TABLE IF NOT EXISTS submissions (
                                           id text PRIMARY KEY,
                                           title text NOT NULL,
                                           date text,
                                           score integer,
                                           type text
                                       ); """
        utils.create_table(self.conn, sql_table)



    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()
