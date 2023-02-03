from flask import Blueprint,request
store = Blueprint('store-api', __name__, url_prefix='/api/v1/store/')
from common.responses import response

@store.route("/", methods=['POST'])
def insert_polygon_data():
    from common.model import Delivery
    from app import db 
    from sqlalchemy import func
  
    # db.session.execute(Delivery.insert().values(outletid=id,location=func.ST_GeomFromText('POLYGON((28.4684730 77.1078357,28.4744336 77.1106681,28.4711893 77.1096382,28.4684730 77.1078357))', 4326)))
    insert_polygon_data = Delivery(outletid="2",location=func.ST_GeomFromText('POLYGON([(28.5894880754974 77.04467967572955,28.599448399178602 77.03008845868854,28.602738992882216 77.02536777082233,28.5894880754974 77.04467967572955))', 4326))

    db.session.add(insert_polygon_data)
    db.session.commit()

    result = db.session.query(Delivery).all()
    for row in result:
        print(row)
    return "Polygon data inserted and retrieved successfully!"

# Query against polygon field
def find_nearest_store(lat, lng):
    from app import db 
    from common.model import Delivery
    from sqlalchemy import func
    query = db.session.query(Delivery.outletid, func.ST_Distance(Delivery.location, func.ST_GeomFromText(f'POINT({lng} {lat})', 4326).label('distance')))
    query = query.order_by(func.ST_Distance(Delivery.location, func.ST_GeomFromText(f'POINT({lng} {lat})', 4326)))
    result = query.first()
    print(result)
    return result

@store.route('/nearest_store', methods=['GET'])
def nearest_store():
   
    lat = request.json['Latitude']
    lng = request.json['Longitude']
    
    store = find_nearest_store(lat,lng)
    return str(store.outletid)
    
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

# Query against Point field
@store.route("/insertpointdata", methods=['POST'])
def insert_point_data():
    from app import db
    from common.model import Outlet
    outletid = request.json['outletid']
    name = request.json['name']
    city = request.json['city']
    lat = request.json['Latitude']
    lon = request.json['Longitude']

    new_store = Outlet(id=outletid,name=name,city=city,location=db.text("ST_MakePoint(:lon, :lat)").bindparams(lon=lon, lat=lat))
    db.session.add(new_store)
    db.session.commit()
    return "Point data inserted Succesfully!"

@store.route('/nearby_store', methods=['GET'])
def nearby_store():
    from app import db
    from common.model import Outlet
    from sqlalchemy import text
    lat = request.json['Latitude']
    long = request.json['Longitude']
    result =db.session.query(Outlet, text("""
    ST_DistanceSphere(location, ST_SetSRID(ST_Point(:long, :lat), 4326)) AS distance
    """))\
    .order_by(text("""
        location <-> ST_SetSRID(ST_Point(:long, :lat), 4326)
    """))\
    .params(long=long, lat=lat)\
    .first()
    return str(result)

