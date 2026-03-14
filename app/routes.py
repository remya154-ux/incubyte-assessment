from flask import current_app as app, request, jsonify
from app.models import db, Employee

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

