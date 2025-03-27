from app import db
from .basemodel import BaseModel
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    """Represents an amenity in the hbnb app."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    @validates("name")
    def validator(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Name must be a required with a maximum of " 
                             "50 characters")
        return value
