from app.persistence.all_repo import UserRepository, PlaceRepository, AmenitiesRepository, ReviewRepository
from app.models.place import Place
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity
from app import bcrypt


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenitiesRepository()


    """User facade"""
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user_data['password'] = bcrypt.generate_password_hash(user_data['password'])
        self.user_repo.update(user_id, user_data)
        return user
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password"""
        return bcrypt.check_password_hash(self.password, password)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    """Place facade"""
    def create_place(self, place_data):
        """the function crrate a new place with the data we provided"""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """The function get a place with place_id"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place

    def get_all_places(self):
        """The function get all places in the repo"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """the function will update a place with new data"""
        place = self.place_repo.get(place_id)
        for keys, value in place_data.items():
            if hasattr(place, keys):
                setattr(place, keys, value)

        self.place_repo.update(place_id, place.__dict__)
        return place

    """Review facade"""
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(
                "Review not found, please enter a valid review title")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found, please enter a valid place")
        return [review for review in self.review_repo.get_all()
                if review.place_id == place_id]

    def update_review(self, review_id, review_update):
        review = self.review_repo.get(review_id)
        for key, value in review_update.items():
            if hasattr(review, key):
                setattr(review, key, value)
        self.review_repo.update(review_id, review.__dict__)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return {'message': 'Review deleted successfully'}

    """Amenity Facades"""
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity by ID"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise KeyError("Amenity not found")
        
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
