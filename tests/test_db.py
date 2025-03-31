import unittest
from k3 import create_app
from k3.config import TestingConfig
from k3.storage import init_db, insert_reservatie, select_reservaties

class DBTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app.testing = True
        
    def test_insert_reservatie(self):
        naam = "A"
        with self.app.app_context():
            init_db()
            resultaat_voor = select_reservaties()
            last_rowid = insert_reservatie(naam, 1, 1, 1)
            resultaat_na = select_reservaties()
            self.assertEqual(len(resultaat_na), len(resultaat_voor) + 1)
            self.assertEqual(resultaat_na[-1][0], last_rowid)
            self.assertEqual(resultaat_na[-1][1], naam)

if __name__ == '__main__':
    unittest.main()