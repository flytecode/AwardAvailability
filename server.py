from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request

app = Flask(__name__)

# DB CODE
# TODO use scraper to update database instead of update_database_test
# TODO check on INSERT IF EXISTS instead of INSERt
# TODO schedule update_database to run every ~15 minutes (maybe even continuously)


def update_database_test():
    hotel1 = Hotel(brand='Hyatt', name='Hyatt Rosemont')
    hotel2 = Hotel(brand='Hyatt', name='Hyatt Regency Indianapolis')
    db.session.add(hotel1)
    db.session.add(hotel2)

    room1 = Room(name="King Suite", hotel_id=1)
    room2 = Room(name="Two Double Standard", hotel_id=1)
    room3 = Room(name="Queen Deluxe Suite", hotel_id=2)
    room4 = Room(name="Standard Room", hotel_id=2)
    db.session.add(room1)
    db.session.add(room2)
    db.session.add(room3)
    db.session.add(room4)

    from datetime import date
    a1 = Availability(start_date=date(2021, 8, 28),
                      end_date=date(2021, 8, 29), room_id=1)
    a2 = Availability(start_date=date(2021, 9, 1),
                      end_date=date(2021, 9, 20), room_id=1)

    a3 = Availability(start_date=date(2021, 10, 28),
                      end_date=date(2021, 10, 29), room_id=2)
    a4 = Availability(start_date=date(2021, 11, 1),
                      end_date=date(2021, 11, 20), room_id=2)

    a5 = Availability(start_date=date(2021, 11, 28),
                      end_date=date(2021, 11, 29), room_id=3)
    a6 = Availability(start_date=date(2021, 12, 1),
                      end_date=date(2021, 12, 20), room_id=3)

    a7 = Availability(start_date=date(2022, 8, 28),
                      end_date=date(2022, 8, 29), room_id=4)
    a8 = Availability(start_date=date(2022, 9, 1),
                      end_date=date(2022, 9, 20), room_id=4)

    a_session = [a1, a2, a3, a4, a5, a6, a7, a8]
    for a in a_session:
        db.session.add(a)
    db.session.commit()
    return


def update_database():
    # TODO fetch data using main.py functions (make sure you import them)
    # TODO insert using flask_sqlalchemy
    # update_database_test()
    print(Hotel.query_all())
    return

#  may be able to remove unique and nullable parameters


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# TODO may want to write make each class json serializable

# class Brand(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(40), unique=True, nullable=False)
#     def __repr__(self):
#         return '<User %r>' % self.username


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(40), unique=False, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)

    # brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    def __repr__(self):
        return f'<Hotel {self.id}: {self.name}>'

    @property
    def serialize(self):
        return {'id': self.id, 'brand': self.brand, 'name': self.name}


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))

    def __repr__(self):
        return f'<Room {self.id}: {self.name}> at {self.hotel_id}'

    @property
    def serialize(self):
        return {'id': self.id, 'name': self.name, 'hotel_id': self.hotel_id}


class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date(), unique=False, nullable=False)
    end_date = db.Column(db.Date(), unique=False, nullable=False)

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return f'<Availability {self.id}: {self.start_date} {self.end_date}> in {self.room_id}'

    @property
    def serialize(self):
        return {'id': self.id, 'start_date': self.start_date, 'end_date': self.end_date}
############

# TODO remove GET
# TODO think about url structure


@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"


@app.route('/brands/', methods=['GET', 'POST'])
def get_brands():
    brands = []
    # TODO check this query: https://stackoverflow.com/questions/2175355/selecting-distinct-column-values-in-sqlalchemy-elixir
    for hotel in db.session.query(Hotel.brand).distinct():
        brands.append(hotel.brand)
    return jsonify(brands)


@app.route('/brands/<brand>/', methods=['GET', 'POST'])
def get_hotels(brand):
    # run sql query on brand id to get all hotels under that brand
    brand = brand.lower()
    hotels = []
    for hotel in Hotel.query.filter_by(brand="Hyatt"):
        hotels.append(hotel.serialize)
    return jsonify(hotels)


@app.route('/brands/<brand>/<hotel_id>/', methods=['GET', 'POST'])
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
