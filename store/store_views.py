from flask import Blueprint,request
store = Blueprint('store-api', __name__, url_prefix='/api/v1/store/')
from common.responses import response

@store.route("/", methods=['POST'])
def insert_polygon_data():
    # insert data into the table
    from common.model import Delivery
    from app import db 
    from sqlalchemy import func
  
    # insert
    # db.session.execute(Delivery.insert().values(outletid=id,location=func.ST_GeomFromText('POLYGON((28.4684730 77.1078357,28.4744336 77.1106681,28.4711893 77.1096382,28.4684730 77.1078357))', 4326)))
    insert_polygon_data = Delivery(outletid="2",location=func.ST_GeomFromText('POLYGON([(28.5894880754974 77.04467967572955,28.599448399178602 77.03008845868854,28.602738992882216 77.02536777082233,28.5894880754974 77.04467967572955))', 4326))

    db.session.add(insert_polygon_data)
    db.session.commit()

    # query the data from the table
    result = db.session.query(Delivery).all()
    for row in result:
        print(row)
    return "Polygon data inserted and retrieved successfully!"


@store.route('/nearest_store', methods=['GET'])
def nearest_store():
    from app import db 
    from common.model import Delivery
    from shapely.geometry import Point,Polygon
    from sqlalchemy import func

    lat = request.json['Latitude']
    lng = request.json['Longitude']

    stores = db.session.query(Delivery.outletid,func.ST_AsText(Delivery.location)).all()
    print(stores)
    nearest_store = None
    min_distance = float('inf')
    point = Point(float(lng), float(lat))
    
    for store in stores:
        outletid, location = store
        print(location)
        
        from shapely.wkt import loads
        polygon= loads(location)
        print(polygon.contains(point))
        if polygon.contains(point):
            nearest_store = outletid
            break
        else:
            distance = point.distance(polygon.centroid)
            if distance < min_distance:
                nearest_store = outletid
                min_distance = distance
    
    return (str(nearest_store))

@store.route('csvdata', methods = ['POST','GET'])
def csvdata():
    import csv
    from app import db 
    from common.model import Outlet
    with open('outlet.csv', 'r') as csv_file:
        csv_records = csv.reader(csv_file, delimiter = ',')
        fields = next(csv_records)
        for row in csv_records:
            if not db.session.query(Outlet.id).filter(Outlet.name==row[1]).count() > 0:
                csvdata = Outlet(id=row[0], name=row[1],city=row[2],outlet_lat=row[3],outlet_long=row[4])
                db.session.add(csvdata)
                db.session.commit()
        return "Done !!"



