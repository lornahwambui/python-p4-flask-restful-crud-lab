from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)  # Use double underscores for __name__
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Use JSONIFY_PRETTYPRINT_REGULAR for pretty-printing JSON responses

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            return make_response(jsonify(plant.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "Plant not found"}), 404)

    def patch(self, id):
        data = request.get_json()
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            for attr in data:
                setattr(plant, attr, data[attr])
            db.session.commit()
            return make_response(plant.to_dict(), 200)
        else:
            return make_response(jsonify({"error": "Plant not found"}), 404)

    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            db.session.delete(plant)
            db.session.commit()
            return make_response('Deleted plant successfully', 204)
        else:
            return make_response(jsonify({"error": "Plant not found"}), 404)

api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
