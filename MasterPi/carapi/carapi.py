from app import app, db, models
from app.models import User, Car, Booking


def seed_data():
    users = [
        User(
            data={
                'username': 'admin',
                'email': 'admin@carshare.com',
                'password': 'adminpass'
            }
        ),
        User(
            data={
                'username': 'engineer',
                'email': 'heiye1996@outlook.com',
                'password': 'engineer'
            }
        ),
        User(
            data={
                'username': 'Jack',
                'email': 'user1@carshare.com',
                'password': 'jackpass'
            }
        ),
        User(
            data={
                'username': 'Will',
                'email': 'user2@carshare.com',
                'password': 'willpass'
            }
        ),
        User(
            data={
                'username': 'testuser3',
                'email': 'user3@carshare.com',
                'password': 'willpass'
            }
        ),
        User(
            data={
                'username': 'testuser4',
                'email': 'user4@carshare.com',
                'password': 'willpass'
            }
        ),
        User(
            data={
                'username': 'testuser5',
                'email': 'user5@carshare.com',
                'password': 'willpass'
            }
        )
    ]
    users[0].role = 0
    users[1].role = 1
    db.session.bulk_save_objects(users)

    cars = [
        Car(
            data={
                'name': 'car123',
                'make': 'tesla',
                'body_type': 1,
                'colour': 1,
                'seats': 4,
                'location': '[-37.177378, 144.159114]',
                'rate': 5.5,
                'status': 1
            }
        ),
        Car(
            data={
                'name': 'cybertruck',
                'make': 'tesla',
                'body_type': 2,
                'colour': 2,
                'seats': 6,
                'location': '[-37.277378, 144.259114]',
                'rate': 5.5,
                'status': 1
            }
        ),
        Car(
            data={
                'name': 'car2',
                'make': 'honda',
                'body_type': 3,
                'colour': 3,
                'seats': 4,
                'location': '[-37.377378, 144.359114]',
                'rate': 5.5,
                'status': 1
            }
        ),
        Car(
            data={
                'name': 'motorcycle',
                'make': 'kawasaki',
                'body_type': 4,
                'colour': 4,
                'seats': 4,
                'location': '[-37.477378, 144.459114]',
                'rate': 5.5,
                'status': 1
            }
        ),
        Car(
            data={
                'name': 'dragon',
                'make': 'SpaceX',
                'body_type': 6,
                'colour': 6,
                'seats': 7,
                'location': '[-37.577378, 144.559114]',
                'rate': 160000000,
                'status': 1
            }
        ),
        Car(
            data={
                'name': 'car1',
                'make': 'toyota',
                'body_type': 5,
                'colour': 5,
                'seats': 4,
                'location': '[-37.777378, 144.759114]',
                'rate': 5.5,
                'status': 1
            }
        )
    ]
    db.session.bulk_save_objects(cars)

    db.session.commit()

    bookings = [
        Booking(
            data={
                "car_id": 1,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-10T01:02:49",
                "timeend": "2020-06-10T03:16:24",
                "time_start": "2020-06-10T02:02:00",
                "user_id": 3
            }
        ),
        Booking(
            data={
                "car_id": 2,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-11T01:02:49",
                "timeend": "2020-06-11T03:16:24",
                "time_start": "2020-06-11T02:02:00",
                "user_id": 4
            }
        ),
        Booking(
            data={
                "car_id": 3,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-12T01:02:49",
                "timeend": "2020-06-12T03:16:24",
                "time_start": "2020-06-12T02:02:00",
                "user_id": 5
            }
        ),
        Booking(
            data={
                "car_id": 4,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-13T01:02:49",
                "timeend": "2020-06-13T03:16:24",
                "time_start": "2020-06-13T02:02:00",
                "user_id": 6
            }
        ),
        Booking(
            data={
                "car_id": 5,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-14T01:02:49",
                "timeend": "2020-06-14T03:16:24",
                "time_start": "2020-06-14T02:02:00",
                "user_id": 7
            }
        ),
        Booking(
            data={
                "car_id": 6,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-14T01:02:49",
                "timeend": "2020-06-14T03:16:24",
                "time_start": "2020-06-14T02:02:00",
                "user_id": 3
            }
        ),
        Booking(
            data={
                "car_id": 5,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-13T01:02:49",
                "timeend": "2020-06-13T03:16:24",
                "time_start": "2020-06-13T02:02:00",
                "user_id": 3
            }
        ),
        Booking(
            data={
                "car_id": 4,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-12T01:02:49",
                "timeend": "2020-06-12T03:16:24",
                "time_start": "2020-06-12T02:02:00",
                "user_id": 5
            }
        ),
        Booking(
            data={
                "car_id": 3,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-11T01:02:49",
                "timeend": "2020-06-11T03:16:24",
                "time_start": "2020-06-11T02:02:00",
                "user_id": 3
            }
        ),
        Booking(
            data={
                "car_id": 2,
                "hours": 1,
                "status": 2,
                "timebooked": "2020-06-11T01:02:49",
                "timeend": "2020-06-11T03:16:24",
                "time_start": "2020-06-11T02:02:00",
                "user_id": 7
            }
        ),
        Booking(
            data={
                "car_id": 1,
                "hours": 1,
                "status": 3,
                "timebooked": "2020-06-11T01:02:49",
                "timeend": "2020-06-11T03:16:24",
                "time_start": "2020-06-11T02:02:00",
                "user_id": 2
            }
        ),
        Booking(
            data={
                "car_id": 2,
                "hours": 1,
                "status": 3,
                "timebooked": "2020-06-11T01:02:49",
                "timeend": "2020-06-11T03:16:24",
                "time_start": "2020-06-11T02:02:00",
                "user_id": 2
            }
        ),
        Booking(
            data={
                "car_id": 2,
                "hours": 1,
                "status": 3,
                "timebooked": "2020-06-11T01:02:49",
                "timeend": "2020-06-11T03:16:24",
                "time_start": "2020-06-11T02:02:00",
                "user_id": 2
            }
        )
    ]
    db.session.bulk_save_objects(bookings)

    db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Car': Car, 'Booking': Booking}

user = User.query.filter_by(username="admin").first()
if not user:
    seed_data()
if __name__ == '__main__':
    app.run(host='192.168.1.109', port=10100)
