from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('admin', description='Admin operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user'),
    'password': fields.String(required=True,
                              description='Password of the user')
})

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

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
    'owner_id': fields.String(required=True,
                              description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True,
                             description="List of amenities ID's"),
})

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

"""User admin"""
@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_model)
    @jwt_required()
    @api.doc(security="token")
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email}, 201


@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.expect(user_model)
    @jwt_required()
    @api.doc(security="token")
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = api.payload
        email = data.get('email')

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

"""Places admin"""
@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(place_model)
    @jwt_required()
    @api.doc(security="token")
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        updated_place = facade.update_place(place_id, place)
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
    
"""Review admin"""
@api.route('/review/<review_id>')
class AdminReviewModify(Resource):
    @api.expect(review_model)
    @jwt_required()
    @api.doc(security="token")
    def put(self, review_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        updated_review = facade.review_place(review_id, review)
        if not updated_review:
            return {'message': 'review not found'}, 404
        
        try:
            updated_review = facade.update_review(review_id, updated_review)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review._user_id,
                'place_id': updated_review._place_id
            }, 200
        except ValueError as error:
            return {'error': str(error)}, 400



"""amenities admin"""
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.doc(security="token")
    @api.expect(amenity_model)
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        amenity_data = api.payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(amenity_model)
    @jwt_required()
    @api.doc(security="token")
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        amenity_data = api.payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.update_amenity(amenity_id, amenity_data)
        return {'id': amenity.id,
                    'name': amenity.name}, 200