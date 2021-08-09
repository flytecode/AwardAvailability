from flask import Flask,jsonify,request

app = Flask(__name__)

######## DB CODE 

    

#  may be able to remove unique and nullable parameters

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test222.db'
db = SQLAlchemy(app)

# class Brand(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(40), unique=True, nullable=False)
#     def __repr__(self):
#         return '<User %r>' % self.username

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(40), unique=False,nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)

    # brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    def __repr__(self):
        return f'<Hotel {self.id}: {self.name}>'

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    def __repr__(self):
        return f'<Room {self.id}: {self.name}> at {self.hotel_id}'

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date(), unique=False, nullable=False)
    end_date = db.Column(db.Date(), unique=False,nullable= False)

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    def __repr__(self):
        return f'<Availability {self.id}: {self.start_date} {self.end_date}> in {self.room_id}'
############

# TODO remove GET
# TODO think about url structure

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/brands/', methods=['GET', 'POST'])
def get_brands():
    # run query to get brands
    brands = ["Hyatt","Hilton"]
    return jsonify(brands)

@app.route('/brands/<brand_id>/', methods=['GET', 'POST'])
def get_hotels(brand_id):
    # run sql query on brand id to get all hotels under that brand
    hotels = [{'hotel_id': 1, 'name': 'NYC Grand Hyatt'}, {'hotel_id': 2, 'name': "Los Angeles Lights Hotels"}]
    return jsonify(hotels)

@app.route('/brands/<brand_id>/<hotel_id>/', methods=['GET', 'POST'])
def get_availability(hotel):
    # run sql query to get availability of hotel in specified date range
    start_date = request.args.get("start_date") 
    end_date = request.args.get("end_date")
    # TODO check if start_date and end_date are valid
    if not start_date and not end_date:
        # TODO probably just search 30 days ahead
        start_date = "08-20-2021"
        end_date = "08-30-2021"
    if not start_date:
        # TODO probably search from max(today,30 days before end_date)
        start_date = "08-20-2021"
    if not end_date:
        # TODO probably search 30 days after start_date
        end_date = "08-30-2021"
    availability = {""}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)