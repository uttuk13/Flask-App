import unittest
import cx_Oracle
import sqlite3
from app import app

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = sqlite3.connect('test_db.sqlite')
        cls.cursor = cls.connection.cursor()
        cls.cursor.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
        cls.cursor.execute("INSERT INTO students VALUES ('John', '123 Main St', 'Anytown', '12345')")
        cls.connection.commit()

    @classmethod
    def tearDownClass(cls):
        cls.cursor.execute('DROP TABLE students')
        cls.connection.commit()
        cls.connection.close()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)

    def test_enternew(self):
        response = self.app.get('/enternew')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add New Record', response.data)

    def test_addrec(self):
        data = {'nm': 'Jane', 'add': '456 Park Ave', 'city': 'Othertown', 'pin': '67890'}
        response = self.app.post('/addrec', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Record successfully added', response.data)

        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM students WHERE name = ?', ('Jane',))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'Jane')
        self.assertEqual(result[1], '456 Park Ave')
        self.assertEqual(result[2], 'Othertown')
        self.assertEqual(result[3], '67890')

    def test_list(self):
        response = self.app.get('/list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'List of Students', response.data)
        self.assertIn(b'John', response.data)
        self.assertIn(b'123 Main St', response.data)
        self.assertIn(b'Anytown', response.data)
        self.assertIn(b'12345', response.data)

    def test_listOracleDB(self):
        conn = cx_Oracle.connect("system/system@localhost:1521/XE")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DUAL")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        response = self.app.get('/listOracleDB')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
