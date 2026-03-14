import unittest
from app.models import Employee
from app import db, create_app
from config import TestConfig


class SalaryStats(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        db.create_all()
        # Add test employees
        db.session.add(Employee(id=1, name="John", job_title="Tester", salary=50000, country='USA'))
        db.session.add(Employee(id=2, name="Steven", job_title="Tester", salary=100000, country='USA'))
        db.session.add(Employee(id=3, name="Chris", job_title="Developer", salary=75000, country='USA'))
        db.session.add(Employee(id=4, name="Bob", job_title="Tester", salary=30000, country='India'))
        db.session.add(Employee(id=5, name="Mary", job_title="Manager", salary=50000, country='India'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_salary_stats_usa(self):
        response = self.client.get('/salary_stats/USA')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['country'], 'USA')
        self.assertEqual(data['min_salary'], 50000)
        self.assertEqual(data['max_salary'], 100000)
        self.assertEqual(data['avg_salary'], 75000.0)

    def test_salary_stats_india(self):
        response = self.client.get('/salary_stats/India')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['country'], 'India')
        self.assertEqual(data['min_salary'], 30000)
        self.assertEqual(data['max_salary'], 50000)
        self.assertEqual(data['avg_salary'], 40000.0)

    def test_salary_stats_no_employees(self):
        response = self.client.get('/salary_stats/Germany')
        self.assertEqual(response.status_code, 404)
        data = response.json
        self.assertEqual(data['error'], "No employees found in this country")

    def test_average_salary_tester(self):
        response = self.client.get('/average_salary/Tester')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertEqual(data["job_title"], "Tester")
        self.assertEqual(data["average_salary"], 60000.0)


if __name__ == '__main__':
    unittest.main()
