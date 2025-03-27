from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
api = Namespace('places', description='Place operations')


# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
                              
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security="token")
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        data_place = api.payload
        data_place['owner_id'] = current_user['id']
        print(data_place['owner_id'])
        try:
            
            new_place = facade.create_place(data_place)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner_id,
            }, 201
        except ValueError as error:
            return {"error": str(error)}, 400
        except TypeError as error:
            return {"error": str(error)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [
            {
                "id": all_place.id,
                "title": all_place.title,
                "price": all_place.price,
                "latitude": all_place.latitude,
                "longitude": all_place.longitude,
            } for all_place in places
        ],200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            data_place = facade.get_place(place_id)
            return {
                "id": data_place.id,
                "title": data_place.title,
                "description": data_place.description,
                "price": data_place.price,
                "latitude": data_place.latitude,
                "longitude": data_place.longitude,
                "owner_id": data_place.owner_id
            }, 200
        except ValueError as error:
            return {"error": str(error)}, 404

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="token")
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Invalid input data'}, 400
        if current_user['id'] != place.owner_id:
            return{'error': 'Unauthorized action'}, 403
        updated_data = api.payload
        updated_place = facade.update_place(place_id, updated_data)
        if not updated_place:
            return {'message': 'Place not found'}, 404
        
        return {
            "title": updated_place.title,
            "description": updated_place.description,
            "price": updated_place.price,
            "latitude": updated_place.latitude,
            "longitude": updated_place.longitude,
            "owner_id": updated_place.owner_id
            }, 200

