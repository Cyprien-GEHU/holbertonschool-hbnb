from app import db
from .basemodel import BaseModel
from app.models.user import User
from sqlalchemy.orm import validates ,relationship
from .relationship import place_amenity


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviews = relationship('Review', backref='place', lazy = True)
    amenities = relationship('Amenity', secondary=place_amenity, lazy = 'subquery',
                             backref=db.backref('places', lazy=True))

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @validates('title', include_backrefs=False)
    def validate_title(self, key, value):
        if not value:
            raise ValueError("title is required")
        if len(value) > 100:
            raise ValueError("title must be less than 100 characters")
        return value

    @validates('price', include_backrefs=False)
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("price must be greater than 0")
        return value

    @validates('latitude', include_backrefs=False)
    def validate_latitude(self, key, value):
        if not (90.0 >= value >= -90.0):
            raise ValueError("Latitude must be beewteen 90.0 and -90.0")
        return value

    @validates('longitude', include_backrefs=False)
    def validate_longitude(self, key, value):
        if not (180.0 >= value >= -180.0):
            raise ValueError("longitude must be beewteen 180 and -180")
        return value

    @validates('owner_id')
    def validate_owner_id(self, key, value):
        if not isinstance(value, str):
            raise TypeError("owner_id must be a string")
        if len(value) != 36:
            raise ValueError("the id have 36 letters")
        return value
