from app import db
from geoalchemy2.types import Geometry

class Outlet(db.Model):
    __tablename__ = 'outlet'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    city = db.Column(db.String())
    location = db.Column(Geometry("POINT", srid=4326))
    
    def __init__(self, id,name,city,location):
        self.id = id
        self.name = name
        self.city = city
        self.location = location

    def __repr__(self):
        return f"{self.id}:{self.name}:{self.city}:{self.location}"

class Delivery(db.Model):
    __tablename__ = 'delivery'
    outletid = db.Column(db.Integer, primary_key = True)
    location = db.Column(Geometry("POLYGON", srid=4326))

    def __init__(self, outletid,location):
        self.outletid = outletid
        self.location = location
    def __repr__(self):
        return f"{self.outletid}:{self.location}"


db.create_all()
db.session.commit()
