import unittest
import json

from app import create_app
from app.models import db, Employee
from config import TestConfig


class EmployeeTestCase(unittest.TestCase):

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

    # CREATE TEST
    def test_create_employee(self):
        response = self.client.post(
            "/employees",
            json={
                "name": "John",
                "country": "Netherlands",
                "job_title": "Developer",
                "salary": 5000,
            }
        )
        self.assertEqual(response.status_code, 201)
        emp = Employee.query.filter_by(name="John").first()
        self.assertIsNotNone(emp)
        self.assertEqual(emp.name, "John")

    def test_create_employee_failure(self):
        response = self.client.post(
            "/employees",
            json={
                "country": "Netherlands",
                "job_title": "Developer",
                "salary": 5000,
            }
        )
        self.assertEqual(response.status_code, 400)

    # READ ALL
    def test_get_employees(self):
        self.client.post("/employees",
            json={
                "name": "John",
                "country": "Netherlands",
                "job_title": "Developer",
                "salary": 5000,
            }
        )
        response = self.client.get("/employees")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

    # Read 1 employee
    def test_get_employee(self):
        self.client.post("/employees",
            json={
                "name": "John",
                "country": "Netherlands",
                "job_title": "Developer",
                "salary": 5000,
            }
        )
        response = self.client.get("/employees/1")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("John", data["name"])

    # UPDATE
    def test_update_employee(self):
        res = self.client.post("/employees",
            json={
                "name": "John",
                "country": "Netherlands",
                "job_title": "Developer",
                "salary": 5000,
            }
        )

        emp_id = json.loads(res.data)["id"]

        response = self.client.put(
            f"/employees/{emp_id}",
            json={"job_title": "Senior Developer"}
        )

        data = json.loads(response.data)

        self.assertEqual(data["job_title"], "Senior Developer")

    # DELETE
    def test_delete_employee(self):
        res = self.client.post("/employees",
            json={
                "name": "John",
                "country": "Netherlands",
                "job_title": "Developer",
                "salary": 5000,
            }
        )
        emp_id = json.loads(res.data)["id"]
        response = self.client.delete(f"/employees/{emp_id}")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()