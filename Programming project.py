# Detailed explanation of all classes, attributes, methods, etc. + testing is found in my report

class Main:
    def fright_car_getter(self, ID):  # freight car getter method
        for car in FreightCar.freight_cars_list:
            if car.id_getter() == ID:
                return car
        return None

    def container_getter(self, ID):  # container car getter method
        for container in Container.containers:
            if container.id_getter() == ID:
                return container
        return None

    def auto_run(self):  # is called automatically on run
        n = int(input("Please Type No. Of Inputs/Actions: \n"))
        actions = []  # actions are the first letter (like report document)
        for i in range(n):
            line = input().split()  # splits user input into iterable sections
            actions.append(line)
        for line in actions:
            action = int(line[0])

            if action == 1:  # Creating a container
                station_id = int(line[1])
                weight = int(line[2])
                container_id = Container.create_container(station_id, weight, *line[3:])
                if container_id:
                    pass
                else:
                    print("Station Doesn't Exist")

            elif action == 2:  # Creating a freight car
                station_id, max_weight, max_count, max_heavy, max_refrigerated, max_liquid, fuel_consumption \
                    = map(float, line[1:])
                FreightCar.create_freight_car(station_id, max_weight, max_count, max_heavy, max_refrigerated,
                                              max_liquid,
                                              fuel_consumption)

            elif action == 3:  # Creating a station
                x, y = map(float, line[1:])
                Station.create_station(x, y)

            elif action == 4:  # Loading a container to a freight car
                freight_car_id = int(line[1])
                container_id = int(line[2])
                car = self.fright_car_getter(freight_car_id)
                if car:
                    car.load(freight_car_id, container_id)
                else:
                    print("Container Can't be Loaded")

            elif action == 5:  # Unloading a container from a freight car
                freight_car_id = int(line[1])
                container_id = int(line[2])
                car = self.fright_car_getter(freight_car_id)
                if car:
                    car.unload(freight_car_id, container_id)
                else:
                    print("Freight Car Doesn't Exist")

            elif action == 6:  # Freight car goes to another station
                freight_car_id = int(line[1])
                station_id = int(line[2])
                car = self.fright_car_getter(freight_car_id)
                if car:
                    car.travel(freight_car_id, station_id)
                else:
                    print("Freight Car Doesn't Exist")

            elif action == 7:  # Freight car is refueled
                freight_car_id = int(line[1])
                amount = int(line[2])
                car = self.fright_car_getter(freight_car_id)
                if car:
                    car.refuel(freight_car_id, amount)
                else:
                    print("Freight Car Doesn't Exist")

        for station in Station.my_stations:
            station.print_containers()
            print("")
        for car in FreightCar.freight_cars_list:
            car.print_containers()
            print("")


class Station:
    x = []
    y = []
    ID = 0
    stations_IDs = []
    my_stations = []

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.ID = Station.ID
        Station.ID = Station.ID + 1  # Increments every new ID
        self.containers = {'Normal_container': [], 'Heavy_container': [], 'Refrigerated_container': [],
                           'Liquid_container': []}
        self.history = []
        self.current = []
        Station.stations_IDs.append(self.ID)
        Station.x.append(X)
        Station.y.append(Y)
        Station.my_stations.append(self)

    def __str__(self):  # string representation
        return f"Station {self.ID}: ({'{:.2f}'.format(self.X)}, {'{:.2f}'.format(self.Y)}) "

    @staticmethod
    def create_station(X, Y):  # create stations using coordinates
        for station in Station.my_stations:
            if station.X == X and station.Y == Y:
                print("Station Already Exists")
                return None
        return Station(X, Y)

    def current_getter(self):
        return self.current

    def history_getter(self):
        return self.history

    def distance_getter(self, other):  # distance calculation
        x2_minus_x1 = self.X - other.X
        y2_minus_y1 = self.Y - other.Y
        distance = ((x2_minus_x1 ** 2) + (y2_minus_y1 ** 2)) ** 0.5  # pythagoras
        return distance

    def id_getter(self):
        return self.ID

    @staticmethod
    def find_station(ID):  # search for station by id
        for i in Station.my_stations:
            if i.id_getter() == ID:
                return i
        print("Station Doesn't Exist")
        return None

    def print_containers(self):  # print a list of all containers in a specific station
        print(self)
        for key, value in self.containers.items():
            if value:
                print(f"{key}: {' '.join(str(j) for j in value)}")


class FreightCar:
    freight_cars_list = []
    ID = 0

    def __init__(self, current_station, total_weight_capacity, max_no_of_all_containers, max_no_of_heavy_containers,
                 max_no_of_refrigerated_containers, max_no_of_liquid_containers, fuel_consumption_per_km):
        self.ID = FreightCar.ID
        FreightCar.ID = FreightCar.ID + 1
        self.fuel = 0.0
        self.current_station = current_station
        self.total_weight_capacity = total_weight_capacity
        self.max_no_of_all_containers = max_no_of_all_containers
        self.max_no_of_heavy_containers = max_no_of_heavy_containers
        self.max_no_of_refrigerated_containers = max_no_of_refrigerated_containers
        self.max_no_of_liquid_containers = max_no_of_liquid_containers
        self.fuel_consumption_per_km = fuel_consumption_per_km
        self.containers = {'Normal_container': [], 'Heavy_container': [], 'Refrigerated_container': [],
                           'Liquid_container': []}
        FreightCar.freight_cars_list.append(self)
        self.list_of_containers = []

    def __str__(self):  # string representation
        return f"Freight car {self.ID}: {'{:.2f}'.format(self.fuel)}"

    @staticmethod
    def create_freight_car(current_station, total_weight_capacity, max_no_containers, max_no_heavy_containers,
                           max_no_liquid_containers, max_no_ref_containers, fuel_cons_per_km):
        for station in Station.my_stations:
            if station.id_getter() == current_station:
                if total_weight_capacity <= 0:
                    print("Invalid Total Weight Capacity")
                    return None
                if max_no_containers < 0:
                    print("Invalid Max No. Of Containers")
                    return None
                if max_no_heavy_containers < 0:
                    print("Invalid Max No. Of Heavy Containers")
                    return None
                if max_no_liquid_containers < 0:
                    print("Invalid Max No. Of Liquid Containers")
                    return None
                if max_no_ref_containers < 0:
                    print("Invalid Max No. Of Refrigerated Containers")
                    return None
                if fuel_cons_per_km <= 0.0:
                    print("Invalid Fuel Consumption")
                    return None
                else:
                    freight_car = FreightCar(current_station, total_weight_capacity, max_no_containers,
                                             max_no_heavy_containers, max_no_liquid_containers, max_no_ref_containers,
                                             fuel_cons_per_km)
                    station.history_getter().append(freight_car)
                    station.current_getter().append(freight_car)
                    return freight_car
        print("Station Doesn't Exist")
        return None

    def id_getter(self):
        return self.ID

    def station_getter(self):
        return self.current_station

    def count_containers(self):  # count by incrementing
        count = 0
        for i in self.containers.values():
            for j in i:
                count += 1
        return count

    def weight_getter2(self):
        weight = 0
        for i in self.containers.values():
            for j in i:
                weight += j.weight_getter1()
        return weight

    def get_current_containers(self):
        for key, value in self.containers.items():
            for container in value:
                self.list_of_containers.append(container)
        sorted_list_of_containers = sorted(self.list_of_containers, key=lambda c: c.ID)
        return sorted_list_of_containers  # returns list of all containers currently in the freight car (sorted by ID)

    def find_container(self, ID):  # lookup a container
        for i in self.containers.values():
            for container in i:
                if container.id_getter() == ID:
                    return True
        return False

    def load(self, carID, containerID):  # load freight car onto container
        if self.id_getter() != carID:
            print("Freight Car Doesn't Exist")
            return

        for station in Station.my_stations:
            for car in station.current:
                if self.ID != car.id_getter() and car.find_container(containerID):
                    print("Container Currently Loaded On Another Freight Car")
                    return None

        for container in Container.containers:
            stationID = container.station_getter()
            station = Station.find_station(stationID)
            if container.id_getter() == containerID:
                if container.station_getter() == self.current_station:
                    if self.count_containers() < self.max_no_of_all_containers and \
                            (self.weight_getter2() + container.weight_getter1()) < self.total_weight_capacity:

                        if isinstance(container, Normal_container):
                            self.containers['Normal_container'].append(container)
                            station.containers['Normal_container'].remove(container)
                        elif isinstance(container, Heavy_container) and not \
                                isinstance(container, Refrigerated_container) \
                                and not isinstance(container, Liquid_container) and \
                                len(self.containers['Heavy_container']) < self.max_no_of_heavy_containers:
                            self.containers['Heavy_container'].append(container)
                            station.containers['Heavy_container'].remove(container)
                        elif isinstance(container, Refrigerated_container) and \
                                len(self.containers['Refrigerated_container']) < self.max_no_of_refrigerated_containers:
                            self.containers['Refrigerated_container'].append(container)
                            station.containers['Refrigerated_container'].remove(container)
                        elif isinstance(container, Liquid_container) and \
                                len(self.containers['Liquid_container']) < self.max_no_of_liquid_containers:
                            self.containers['Liquid_container'].append(container)
                            station.containers['Liquid_container'].remove(container)
                        else:
                            print("Reached Container's Capacity limit")
                            return None
                    else:
                        print("Reached Container/Weight Capacity Limit")
                        return None
                else:
                    print("Freight Car And Container Aren't At The Same Station")
                    return None
                return
        print("Container Doesn't Exist")
        return None

    def unload(self, carID, containerID):  # unload freight car onto container
        if self.id_getter() != carID:
            print("Freight Car Doesn't Exist")
            return
        container_found = False
        for container_type in self.containers:
            for container in self.containers[container_type]:
                if container.id_getter() == containerID:
                    stationID = self.current_station
                    station = Station.find_station(stationID)

                    if isinstance(container, Normal_container):
                        station.containers['Normal_container'].append(container)
                        self.containers['Normal_container'].remove(container)
                    elif isinstance(container, Heavy_container) and not isinstance(container, Refrigerated_container) \
                            and not isinstance(container, Liquid_container):
                        station.containers['Heavy_container'].append(container)
                        self.containers['Heavy_container'].remove(container)
                    elif isinstance(container, Refrigerated_container):
                        station.containers['Refrigerated_container'].append(container)
                        self.containers['Refrigerated_container'].remove(container)
                    elif isinstance(container, Liquid_container):
                        station.containers['Liquid_container'].append(container)
                        self.containers['Liquid_container'].remove(container)
                    container_found = True
                    break
            if container_found:
                break

        if not container_found:
            print("Container Doesn't Exist In Freight Car's Containers")

    def containers_consumption(self):  # get total consumption relative to type
        total_consumption = 0
        for container_type in self.containers:
            for container in self.containers[container_type]:
                total_consumption += container.consumption()
        return total_consumption

    def travel(self, carID, destination_stationID):  # move freight cars between stations
        if self.id_getter() != carID:
            print("Freight Car Doesn't Exist")
            return
        station = Station.find_station(self.current_station)
        destination_station = Station.find_station(destination_stationID)
        distance = station.distance_getter(destination_station)
        fuel_consumption = self.fuel_consumption_per_km + self.containers_consumption()
        fuel_consumed = distance * fuel_consumption
        if self.fuel < fuel_consumed:
            print(f"Current Fuel Is Insufficient, this distance requires {fuel_consumed - self.fuel}")
            return None
        else:
            self.fuel -= fuel_consumed
            for st in Station.my_stations:
                if st.id_getter() == self.current_station:
                    st.current.remove(self)
            self.current_station = destination_stationID
            for st in Station.my_stations:
                if st.id_getter() == self.current_station:
                    st.current.append(self)
                    st.history.append(self)

    def refuel(self, carID, amount):  # refuel with specific amount
        if self.id_getter() != carID:
            print("Freight Car Doesn't Exist")
            return
        self.fuel += amount
        return self.fuel

    def print_containers(self):  # print containers in a freight car
        print(self)
        for key, value in self.containers.items():
            if value:
                print(f"{key}: {' '.join(str(j) for j in value)}")


class Container:
    ID = 0
    containers = []

    def __init__(self, station, weight):
        self.station = station
        self.weight = weight
        self.ID = Container.ID
        Container.ID += 1
        Container.containers.append(self)

    def __eq__(self, other):  # Checks if 2 containers are equal using their id & weight
        if isinstance(other, Container) and self.ID == other.ID and self.weight == other.Weight:
            return True
        else:
            return False

    def __str__(self):  # string representation
        return f"{self.ID}"

    def consumption(self):
        return 0.0

    def station_getter(self):
        return self.station

    def id_getter(self):
        return self.ID

    def id_setter(self, ID):
        self.ID = ID

    def weight_getter1(self):
        return self.weight

    def weight_setter(self, weight):
        self.weight = weight

    @staticmethod
    def create_container(stationID, weight, container_type=None):
        for station in Station.my_stations:
            if station.id_getter() == stationID:
                if weight <= 0:
                    return "Invalid Weight"

                elif 3000 >= weight > 0 and container_type is None:
                    normal_container = Normal_container(stationID, weight)
                    station.containers['Normal_container'].append(normal_container)
                    return normal_container

                elif weight > 3000:
                    if container_type == 'R' or container_type == 'r':
                        refrigerated_container = Refrigerated_container(stationID, weight)
                        station.containers['Refrigerated_container'].append(refrigerated_container)
                        return refrigerated_container

                    elif container_type == 'L' or container_type == 'l':
                        liquid_container = Liquid_container(stationID, weight)
                        station.containers['Liquid_container'].append(liquid_container)
                        return liquid_container

                    elif container_type is None:
                        heavy_container = Heavy_container(stationID, weight)
                        station.containers['Heavy_container'].append(heavy_container)
                        return heavy_container

                    else:
                        print("Invalid Heavy Container Type")
                        return None
                return None
        print("Station Doesn't Exist")
        return None


class Normal_container(Container):
    def __init__(self, station, weight):
        super().__init__(station, weight)

    def __str__(self):  # string representation
        return f"{self.ID}"

    def consumption(self):
        return self.weight * 2.5


class Heavy_container(Container):
    def __init__(self, station, weight):
        super().__init__(station, weight)

    def __str__(self):  # string representation
        return f"{self.ID}"

    def consumption(self):
        return self.weight * 3


class Refrigerated_container(Heavy_container):
    def __init__(self, station, weight):
        super().__init__(station, weight)

    def __str__(self):  # string representation
        return f"{self.ID}"

    def consumption(self):
        return self.weight * 5


class Liquid_container(Heavy_container):
    def __init__(self, station, weight):
        super().__init__(station, weight)

    def __str__(self):  # string representation
        return f"{self.ID}"

    def consumption(self):
        return self.weight * 4


if __name__ == '__main__':
    main = Main()
    main.auto_run()
