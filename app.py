from flask import Flask, request, jsonify
from models.register import Register
from database import db
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'
db.init_app(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    food_name = data.get('food_name')
    description = data.get('description')
    dieta = data.get('dieta', False)

    if food_name:
        register = Register(food_name=food_name, description=description, dieta=dieta, horario=datetime.now())
        db.session.add(register)
        db.session.commit()
        return jsonify ({'message':'Seu lanche foi registrado com sucesso!'})
    
    return jsonify ({'message':'Dados necessarios nao foram enviados'}), 400

@app.route('/register/<int:id_register>', methods=['PUT'])
def update_register(id_register):
    data = request.json
    register = Register.query.get(id_register)
    
    if register:
         register.food_name = data.get('food_name')
         register.description = data.get('description')
         register.dieta = data.get('dieta')
         register.horario = datetime.now()
         db.session.commit()
         return jsonify ({'message':'Registro alterado com sucesso'})
    
    return jsonify ({'message":"Registro nao encontrado'}), 404

@app.route('/register/<int:id_register>', methods=['DELETE'])
def remove_register(id_register):
     register = Register.query.get(id_register)

     if register:
         db.session.delete(register)
         db.session.commit()
         return jsonify ({'message':f'Registro de id:{id_register} deletado com sucesso'})
     
     return jsonify ('"message':'Registro nao encontrador'}), 404

@app.route('/register/<int:id_register>', methods=['GET'])
def get_register(id_register):
    register = Register.query.get(id_register)
    if register:
        list_register = {'food_name': register.food_name,
                'description': register.description,
                'diet': register.dieta,
                'data_criacao': register.horario.strftime('%Y-%m-%d %H:%M:%S')}    
        return jsonify (list_register)

    return jsonify ({'message":"Registro nao encontrado'}), 404

@app.route('/registers', methods=['GET'])
def get_registers():
    all_registers = Register.query.all()
    list_register = [
        {
            'id': register.id,
            'name': register.food_name,
            'description': register.description,
            'data_criacao': register.horario.strftime('%Y-%m-%d %H:%M:%S'),
            'diet': register.dieta
        }
        for register in all_registers
    ]
    return jsonify(list_register)


if __name__ == "__main__":
    app.run(debug=True)