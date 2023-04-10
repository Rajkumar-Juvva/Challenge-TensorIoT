import random
import json

class ParkingLot:
    def __init__(self, size, spot_size=(8, 12)):
        self.spot_size = spot_size
        self.num_spots = (size // (spot_size[0] * spot_size[1]))
        # print(self.num_spots)
        self.spots = [None] * self.num_spots
    
    def find_empty_spot(self):
        empty_spots = [i for i, spot in enumerate(self.spots) if spot is None]
        if not empty_spots:
            return None
        else:
            return random.choice(empty_spots)
    
    def park(self, car, spot):
        if self.spots[spot] is None:
            self.spots[spot] = car
            print(f"Car with license plate {car.license_plate} parked successfully in spot {spot}.")
            return True
        else:
            print(f"Error: Spot {spot} is occupied.")
            return False
    
    def map_cars_to_spots(self):
        mapping = {i: self.spots[i].license_plate if self.spots[i] else None for i in range(self.num_spots)}
        return json.dumps(mapping)

class Car:
    def __init__(self, license_plate):
        self.license_plate = license_plate
    
    def __str__(self):
        return self.license_plate
    
    def park(self, parking_lot):
        spot = parking_lot.find_empty_spot()
        while spot is None:
            print("Error: Parking lot is full.")
            return True
        else:
            return parking_lot.park(self, spot)

lot = ParkingLot(2000)
cars = [Car(f"{random.randint(1000000, 9999999)}") for i in range(30)]

for car in cars:
        parked = False
        while not parked:
            parked = car.park(lot)
json_data = lot.map_cars_to_spots()
file_name = "parking_lot_data.json"
json_file = open(file_name,'w')
json_file.write(json_data)
json_file.close()

#string json file to s3 bucket
import boto3
s3 = boto3.resource('s3')
file_data = open(file_name,'rb')
buk = s3.Bucket('rajkumar-juvva-bucket-1')
buk.put_object(Key='parking_lot_josn_data',Body=file_data)
print(f"{file_name} saved to s3 bucket")
