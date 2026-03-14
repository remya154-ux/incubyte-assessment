import unittest
from app import create_app
from app.models import db, Employee
from config import TestConfig

class EmployeeSalary(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        # Add test employees
        db.session.add(Employee(id=1, name="John", job_title="Tester", salary=1000, country='USA'))
        db.session.add(Employee(id=2, name="Steven", job_title="Tester", salary=1000, country='India'))
        db.session.add(Employee(id=3, name="Chris", job_title="Tester", salary=1000, country='Germany'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_salary_usa(self):
        response = self.client.get('/salary/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['net_salary'], 880)  # 1000 - 12%

    def test_salary_india(self):
        response = self.client.get('/salary/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['net_salary'], 900)  # 1000 - 10%

    def test_salary_other_country(self):
        response = self.client.get('/salary/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['net_salary'], 1000)  # No deduction

    def test_employee_not_found(self):
        response = self.client.get('/salary/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
