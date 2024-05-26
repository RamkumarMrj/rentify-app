import datetime
from werkzeug.security import check_password_hash


class User:
    def __init__(self, id, first_name, email, user_type, password, last_name=None, phone_number=None,):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.user_type = user_type
        self.password = password

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "user_type": self.user_type,
            "password": self.password
        }


class Properties:
    def __init__(self, id, seller_id, place, area, price, bedrooms, bathrooms, amenities, description, like_count=0, created_at=datetime.datetime.now(), updated_at=None, image=None, interestedUsers=None):
        if interestedUsers is None:
            interestedUsers = []
        self.id = id
        self.seller_id = seller_id
        self.place = place
        self.area = area
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.amenities = amenities
        self.description = description
        self.like_count = like_count
        self.created_at = created_at
        self.updated_at = updated_at
        self.image = image
        self.interestedUsers = interestedUsers

    
