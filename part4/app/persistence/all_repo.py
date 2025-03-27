from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    
class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

class AmenitiesRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_review_by_place(self, place_id):
        return self.model.query.filter_by(place_id=place_id).all()