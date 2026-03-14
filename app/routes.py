from flask import current_app as app, request, jsonify
from app.models import db, Employee
from sqlalchemy import func

def init_app(app):
    # CRUD endpoints
    # Create employee
    @app.route('/employees', methods=['POST'])
    def add_employee():
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'job_title', 'country', 'salary')):
            return jsonify({"error": "Missing fields"}), 400
        new_employee = Employee(
            name=data['name'],
            job_title=data['job_title'],
            country=data['country'],
            salary=data['salary']
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify(new_employee.to_dict()), 201

    # Read all employees
    @app.route('/employees', methods=['GET'])
    def get_employees():
        employees = Employee.query.all()
        return jsonify([e.to_dict() for e in employees])

    # Read one employee details
    @app.route('/employees/<int:id>', methods=['GET'])
    def get_employee(id):
        employee = Employee.query.get_or_404(id)
        return jsonify(employee.to_dict())

    # Update employee details
    @app.route('/employees/<int:id>', methods=['PUT'])
    def update_employee(id):
        employee = Employee.query.get_or_404(id)
        data = request.get_json()
        if 'name' in data: employee.name = data['name']
        if 'job_title' in data: employee.job_title = data['job_title']
        if 'country' in data: employee.country = data['country']
        if 'salary' in data: employee.salary = data['salary']
        db.session.commit()
        return jsonify(employee.to_dict())

    # Delete
    @app.route('/employees/<int:id>', methods=['DELETE'])
    def delete_employee(id):
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Deleted"}), 200

    # Salary endpoint
    @app.route('/salary/<int:id>', methods=['GET'])
    def calculate_net_salary(id):
        employee = Employee.query.get_or_404(id)

        emp_gross_salary = employee.salary
        net_salary = emp_gross_salary

        if employee.country == 'USA':
            net_salary = emp_gross_salary - 0.12 * emp_gross_salary
        elif employee.country == 'India':
            net_salary = emp_gross_salary - 0.1 * emp_gross_salary
        return jsonify({"net_salary": net_salary})

    # salary stats endpoints
    @app.route('/salary_stats/<string:country>', methods=['GET'])
    def salary_stats(country):
        stats = db.session.query(
            func.min(Employee.salary).label('min_salary'),
            func.max(Employee.salary).label('max_salary'),
            func.avg(Employee.salary).label('avg_salary')
        ).filter(Employee.country == country).first()

        if stats.min_salary is None:
            return jsonify({"error": "No employees found in this country"}), 404

        return jsonify({
            "country": country,
            "min_salary": stats.min_salary,
            "max_salary": stats.max_salary,
            "avg_salary": round(stats.avg_salary, 2)
        })
