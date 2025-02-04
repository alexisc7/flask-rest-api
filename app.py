from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"
db = SQLAlchemy(app)


# Crear modelo de base de datos
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone 
        }
        
# Crear las tablas en la base de datos 
with app.app_context():
    db.create_all()


# Endpoints 

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    lista_contact = []
    for contact in contacts:
        lista_contact.append(contact.serialize())

    return jsonify({'contacts': lista_contact}) # [contact.serialize() for contact in contacts]


@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    contact = Contact(name = data['name'], email = data['email'], phone = data['phone'])
    db.session.add(contact)
    db.session.commit()

    return jsonify({'message': 'Contacto creado con éxtito', 'contact': contact.serialize()}), 201 # ,201 -> ret. status 201(creado)


@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)    
    if not contact:
        return jsonify({'message': 'Contacto no encontrado'}), 404 
    return jsonify(contact.serialize())


@app.route('/contacts/<int:id>', methods=['PUT', 'PATCH'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)

    data = request.get_json()

    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']
    if 'phone' in data:
        contact.phone = data['phone']
    
    # Guardar cambios en la bd
    db.session.commit()

    return jsonify({'message': 'Contacto actualizado con éxtito', 'contact': contact.serialize()})

