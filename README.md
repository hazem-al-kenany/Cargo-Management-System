# Freight and Container Management System

This project is a Python-based simulation system for managing freight cars, stations, and various types of containers. The system enables the creation, management, and tracking of freight cars and containers while supporting actions such as loading, unloading, refueling, and traveling between stations.

## Features
- **Create Stations**: Add stations with specific coordinates.
- **Manage Freight Cars**: Create freight cars with customizable capacity and constraints.
- **Container Operations**: Support for multiple container types:
  - Normal Containers
  - Heavy Containers
  - Refrigerated Containers
  - Liquid Containers
- **Freight Car Actions**:
  - Load and unload containers.
  - Travel between stations with fuel consumption considerations.
  - Refuel freight cars.
- **Station Management**:
  - Track containers at each station.
  - Maintain a history of freight car activities.

## How It Works
The program operates in a command-line interface where users input actions to perform operations. The system supports multiple commands to manage freight cars, containers, and stations dynamically.

### Supported Actions:
1. **Create a Container**:
   - Command: `1 <Station_ID> <Weight> [Container_Type]`
   - Example: `1 0 1500` (Normal container) or `1 1 3500 R` (Refrigerated container)

2. **Create a Freight Car**:
   - Command: `2 <Station_ID> <Max_Weight> <Max_Count> <Max_Heavy> <Max_Refrigerated> <Max_Liquid> <Fuel_Consumption>`
   - Example: `2 0 10000 50 20 10 5 0.1`

3. **Create a Station**:
   - Command: `3 <X> <Y>`
   - Example: `3 10.5 20.5`

4. **Load a Container to a Freight Car**:
   - Command: `4 <FreightCar_ID> <Container_ID>`
   - Example: `4 0 1`

5. **Unload a Container from a Freight Car**:
   - Command: `5 <FreightCar_ID> <Container_ID>`
   - Example: `5 0 1`

6. **Travel a Freight Car to Another Station**:
   - Command: `6 <FreightCar_ID> <Station_ID>`
   - Example: `6 0 1`

7. **Refuel a Freight Car**:
   - Command: `7 <FreightCar_ID> <Fuel_Amount>`
   - Example: `7 0 500`

## Code Structure
### Main Classes:
1. **Main**:
   - Entry point for the program.
   - Handles user input and coordinates actions.

2. **Station**:
   - Manages stations, container storage, and history.

3. **FreightCar**:
   - Represents freight cars with attributes like fuel capacity, container limits, and station tracking.

4. **Container**:
   - Base class for all containers.
   - Includes subclasses for:
     - Normal Containers
     - Heavy Containers
     - Refrigerated Containers
     - Liquid Containers

### Methods Overview:
- **Station Methods**:
  - `create_station(X, Y)`
  - `distance_getter(other)`
  - `print_containers()`

- **FreightCar Methods**:
  - `create_freight_car(...)`
  - `load(carID, containerID)`
  - `unload(carID, containerID)`
  - `travel(carID, destination_stationID)`
  - `refuel(carID, amount)`

- **Container Methods**:
  - `create_container(...)`
  - `consumption()`

### Entry Point:
The program begins with `Main.auto_run()`, prompting the user to input actions and handle them sequentially.

## Prerequisites
- Python 3.8 or higher

## How to Run
1. Clone the repository:
   ```bash
   git clone <repository-url>
