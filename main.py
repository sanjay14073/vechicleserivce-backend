from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:user@127.0.0.1:3307/vechiledbms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example Model
class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone_no = db.Column(db.String(14))
    address = db.Column(db.String(60))

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    owner_name = db.Column(db.String(50))
    vehicle_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    make = db.Column(db.String(60))
    model = db.Column(db.String(60))
    make_year = db.Column(db.Integer)
    vehicle_identification_number = db.Column(db.String(10))
    licence_number = db.Column(db.String(20))
    user = db.relationship('Users', backref='vehicle', lazy=True)

class RegistrationDocuments(db.Model):
    __tablename__ = 'registration_documents'
    registration_id = db.Column(db.Integer, primary_key=True, nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    document_number = db.Column(db.String(20), unique=True)
    expiration_date = db.Column(db.Date)
    vehicle = db.relationship('Vehicle', backref='registration_documents', lazy=True)

class InsuranceDocuments(db.Model):
    __tablename__ = 'insurance_documents'
    insurance_id = db.Column(db.Integer, primary_key=True, nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    policy_number = db.Column(db.String(40))
    expire_date = db.Column(db.Date)
    file_document_path = db.Column(db.String(255))
    docs_status = db.Column(db.String(20))
    upload_date = db.Column(db.Date)
    vehicle = db.relationship('Vehicle', backref='insurance_documents', lazy=True)

class InspectionDocuments(db.Model):
    __tablename__ = 'inspection_documents'
    inspection_id = db.Column(db.Integer, primary_key=True, nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    certificate_number = db.Column(db.String(30))
    expiration_date = db.Column(db.Date)
    inspection_station = db.Column(db.String(100))
    vehicle = db.relationship('Vehicle', backref='inspection_documents', lazy=True)

class EmissionDocuments(db.Model):
    __tablename__ = 'emission_documents'
    emission_id = db.Column(db.Integer, primary_key=True, nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    certificate_number = db.Column(db.String(30))
    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    vehicle = db.relationship('Vehicle', backref='emission_documents', lazy=True)

class ComplaintRegistration(db.Model):
    __tablename__ = 'complaint_registration'
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False, primary_key=True)
    complaint = db.Column(db.String(500), unique=True)
    complaint_date = db.Column(db.DateTime)
    file_document_path = db.Column(db.String(255))
    upload_date = db.Column(db.Date)
    file_type = db.Column(db.String(10))
    file_size = db.Column(db.Integer)
    vehicle = db.relationship('Vehicle', backref='complaint_registration', lazy=True)


# Home route
@app.route('/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    user_list = []
    for user in users:
        user_data = {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'email': user.email,
            'phone_no': user.phone_no,
            'address': user.address
        }
        user_list.append(user_data)
    return jsonify({'users': user_list})

# GET route to fetch all vehicles
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicle.query.all()
    vehicle_list = []
    for vehicle in vehicles:
        vehicle_data = {
            'user_id': vehicle.user_id,
            'owner_name': vehicle.owner_name,
            'vehicle_id': vehicle.vehicle_id,
            'make': vehicle.make,
            'model': vehicle.model,
            'make_year': vehicle.make_year,
            'vehicle_identification_number': vehicle.vehicle_identification_number,
            'licence_number': vehicle.licence_number
        }
        vehicle_list.append(vehicle_data)
    return jsonify({'vehicles': vehicle_list})

# POST route to add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = Users(
        user_name=data['user_name'],
        email=data['email'],
        phone_no=data['phone_no'],
        address=data['address']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

# POST route to add a new vehicle
@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    new_vehicle = Vehicle(
        user_id=data['user_id'],
        owner_name=data['owner_name'],
        vehicle_id=data['vehicle_id'],
        make=data['make'],
        model=data['model'],
        make_year=data['make_year'],
        vehicle_identification_number=data['vehicle_identification_number'],
        licence_number=data['licence_number']
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle added successfully'}), 201


# admin routes
@app.route('/admin/control',methods=['GET'])
def fun1():
    return "Yes admin route touched"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=3300)
