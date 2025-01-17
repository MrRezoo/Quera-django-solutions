class Train:

    def __init__(self, last_visited_city, weight_capacity, is_on_trip):
        self.last_visited_city = last_visited_city
        self.weight_capacity = weight_capacity
        self.is_on_trip = is_on_trip


class Trip:
    all_cities = (
        'Arak', 'Ardabil', 'Urmia', 'Isfahan', 'Ahvaz', 'Ilam', 'Bojnord', 'Bandar Abbas', 'Bushehr', 'Birjand',
        'Tabriz',
        'Tehran', 'Khorramabad', 'Rasht', 'Zahedan', 'Zanjan', 'Sari', 'Semnan', 'Sanandaj', 'Shahr-e Kord', 'Shiraz',
        'Qazvin', 'Qom', 'Karaj', 'Kermanshah', 'Gorgan', 'Mashhad', 'Hamadan', 'Yasuj', 'Yazd')

    def __init__(self, origin_city, destination_city, train):
        self.train = self.train_validation(train)
        self.destination_city = destination_city
        self.origin_city = self.origin_city_validation(origin_city)
        self.passengers = []

    def origin_city_validation(self, origin_city):
        if origin_city not in self.all_cities:
            raise ValueError('This input is not a verified city!')
        if origin_city == self.destination_city:
            raise ValueError('Origin and destination cities can\'t be the same!')
        if origin_city != self.train.last_visited_city:
            raise ValueError('The train of the trip is not available in the origin city!')
        return origin_city

    def train_validation(self, train):
        if not isinstance(train, Train):
            raise ValueError('This input is not a train!')
        if train.is_on_trip:
            raise ValueError('This train is not available!')
        return train

    # here implement the magic method
    def __call__(self):
        return self.train.weight_capacity - sum([passenger.load_weight for passenger in self.passengers])


class Passenger:

    def __init__(self, fullname, load_weight):
        self.fullname = fullname
        self.load_weight = load_weight

    def attend_trip(self, trip):
        occupied_capacity = sum([passenger.load_weight for passenger in trip.passengers])
        remain_capacity = trip.train.weight_capacity - occupied_capacity
        if self.load_weight <= remain_capacity:
            trip.passengers.append(self)
        else:
            raise ValueError('Heavy load!')

    def cancel_trip(self, trip):
        if self not in trip.passengers:
            raise ValueError('This passenger is not attended to this trip!')
        trip.passengers.remove(self)

    # here implement the magic method
    def __str__(self):
        return self.fullname
