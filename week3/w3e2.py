import os
import csv

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)


    def get_photo_file_ext(self):
        photo = [".jpg", ".jpeg", ".png", ".gif"]
        if os.path.splitext(self.photo_file_name)[1] in photo:
            return os.path.splitext(self.photo_file_name)[1]
        else:
            raise ValueError


class Car(CarBase):

    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):

    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl
        self.body_length, self.body_width, self.body_height = self.parse_whl(self.body_whl)

    def parse_whl(self, whl):
        try:
            length, width, height = (float(c) for c in whl.split("x", 2))
        except Exception:
            length, width, height = 0.0, 0.0, 0.0
        return length, width, height

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width


class SpecMachine(CarBase):

    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def valid_photo(photo):
    photos = [".jpg", ".jpeg", ".png", ".gif"]
    if os.path.splitext(photo)[1] in photos:
        return photo
    else:
        raise ValueError


def valid_value(value):
    if value == "":
        raise ValueError
    return value


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename, encoding="utf-8") as csv_f:
        reader = csv.reader(csv_f, delimiter=';')
        next(reader)
        for row in reader:
            try:
                brand = valid_value(row[1])
                photo_file_name = valid_photo(valid_value(row[3]))
                carrying = float(valid_value(row[5]))
                if row[0] == "car":
                    passenger_seats_count = row[2]
                    car_list.append(Car(brand, photo_file_name, carrying, passenger_seats_count))
                elif row[0] == "truck":
                    body_whl = row[4]
                    car_list.append(Truck(brand, photo_file_name, carrying, body_whl))
                elif row[0] == "spec_machine":
                    extra = valid_value(row[6])
                    car_list.append(SpecMachine(brand, photo_file_name, carrying, extra))
                else:
                    raise ValueError("I don't know this car_type")
            except Exception:
                pass
    return car_list