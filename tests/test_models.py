import unittest
from app.models import db, Employee
from app import create_app
from config import TestConfig
from sqlalchemy import Integer, String


class ModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_user_column_types(self):
        columns = Employee.__table__.columns

        self.assertIsInstance(columns.id.type, Integer)
        self.assertIsInstance(columns.name.type, String)
        self.assertIsInstance(columns.job_title.type, String)
        self.assertIsInstance(columns.country.type, String)
        self.assertIsInstance(columns.salary.type, Integer)

    def test_create_employee(self):
        user = Employee(name="Bob", job_title="Tester", country="USA", salary=1000)
        db.session.add(user)
        db.session.commit()

        data = user.to_dict()

        self.assertEqual(data["name"], "Bob")
        self.assertEqual(data["job_title"], "Tester")
        self.assertTrue(data["country"], "USA")
        self.assertEqual(data["salary"], 1000)

if __name__ == "__main__":
    unittest.main()