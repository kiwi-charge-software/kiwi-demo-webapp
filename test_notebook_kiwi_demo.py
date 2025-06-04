import marimo

__generated_with = "0.13.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    from matplotlib import pyplot as plt
    import random

    return mo, plt, random


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 20)

    return (slider,)


@app.cell
def _(slider):
    slider, slider.value
    return


@app.cell
def _(plt, slider):
    plt.plot(slider.value, slider.value*2, 'ro')
    plt.grid()
    plt.show()
    return


@app.cell
def _():
    charge_kiwi = 40
    num_kiwis = 3

    num_people_20 = 20
    num_people_40 = 5
    num_people_60 = 5

    avg_battery_capacity = 50

    len_day=12

    total_cars = num_people_20 + num_people_40 +num_people_60
    return (
        avg_battery_capacity,
        charge_kiwi,
        len_day,
        num_kiwis,
        num_people_20,
        num_people_40,
        num_people_60,
        total_cars,
    )


@app.cell
def _(mo, total_cars):
    mo.md(f"""You are charging {total_cars} cars today""")
    return


@app.cell
def _(avg_battery_capacity, mo, num_people_20, num_people_40, num_people_60):
    total_kwh_dispensed = num_people_20*(0.2*avg_battery_capacity) +\
    num_people_40*(0.4*avg_battery_capacity) + num_people_60*(0.6*avg_battery_capacity)

    mo.md(f'''Total kwh dispensed: {total_kwh_dispensed}''')
    return (total_kwh_dispensed,)


@app.cell
def _(charge_kiwi, mo, num_kiwis, total_kwh_dispensed):
    total_kwh_available_each_session = charge_kiwi*num_kiwis

    number_of_recharge = int(total_kwh_dispensed / total_kwh_available_each_session)

    mo.md(f"Number of recharging sessions for {num_kiwis} kiwis: {number_of_recharge}")
    return (number_of_recharge,)


@app.cell
def _(mo, num_kiwis, number_of_recharge):
    time_to_recharge_1k = 0.5


    total_recharge = time_to_recharge_1k*num_kiwis*number_of_recharge 

    mo.md(f"Time it takes to charge the kiwi: {total_recharge} hours")


    return (total_recharge,)


@app.cell
def _(charge_kiwi, mo, num_kiwis, total_kwh_dispensed):
    time_to_charge_veh = round(total_kwh_dispensed / (charge_kiwi*num_kiwis), ndigits=2)
    mo.md(f"Time it takes to charge all vehicles: {time_to_charge_veh} hours")
    return (time_to_charge_veh,)


@app.cell
def _(mo, time_to_charge_veh, total_recharge):
    total_time = time_to_charge_veh + total_recharge
    mo.md(f"Total time taken: {total_time}")


    return (total_time,)


@app.cell
def _(len_day, mo, num_kiwis, total_time):

    (
        mo.md(
            f"""
            **✨ Nice!** You are charging for less than {len_day} hours, with {num_kiwis} kiwi units today! 
            """
        )
        if total_time < len_day
        else mo.md(
            """
            Boo you need more hours in the day
            """
        )
    )
    return


@app.cell
def _(mo):
    mo.md(r"""### Now - moving into the real simulation""")
    return


@app.cell
def _(random):

    ROBOT_BATTERY_CAPACITY = 45 # kWh
    ROBOT_CHARGE_RATE_KWH_PER_HOUR = 60 # 40 minute charging from 20-80 (40 kWh)
    RECHARGE_THRESHOLD = 7 # kWh

    CAR_BATTERY_CAPACITY = 70 #KWH-- make sure that 20% to 80% is LESS than the robot_battery_capacity

    class Robot:
        def __init__(self, rob_id, capacity, charge_rate, recharge_threshold):
            self.rob_id = rob_id
            self.battery_level = capacity # starting with full charge
            self.battery_capacity = capacity
            self.charge_rate = charge_rate
            self.state = "idle" # can be idle, charging, or recharging
            self.current_car = None
            self.cars_charged = 0
            self.recharge_threshold = recharge_threshold
            self.time_elapsed = 0
            self.battery_history = [self.battery_level]

        def update(self):
            if self.state == "charging":
                self.battery_level -= self.current_car.needed_energy
                self.time_elapsed += self.current_car.needed_energy / self.charge_rate 
                self.current_car.current_charge = self.current_car.needed_energy
                print("Car charged: ", self.current_car.cid)
                self.current_car = None
                self.cars_charged +=1
                self.state= "idle"


            elif self.state == "recharging":
                self.time_elapsed += (self.battery_capacity - self.battery_level) /self.charge_rate
                self.battery_level = self.battery_capacity
                self.state = "idle"
                print(f"Robot {self.rob_id} is done charging")

            self.battery_history.append(self.battery_level)

        def check_battery_pct(self, potential_car):
            if self.battery_level <= self.recharge_threshold:
                self.state = "recharging"
                print(f"Robot {self.rob_id} needs recharge, because it is at {self.battery_level} kwH")
            elif self.battery_level <= potential_car.needed_energy:
                self.state = "recharging"
                print(f"Robot {self.rob_id} needs recharge, because it doesn't have sufficient energy ({potential_car.needed_energy} kw)")


        def is_available(self):
            if self.state == "idle" and self.battery_level > self.recharge_threshold:
                return True


    class Car:
        def __init__(self, cid, battery_capacity, current_charge):
            self.cid = cid
            self.battery_capacity = battery_capacity
            self.current_charge = current_charge
            self.needed_energy  = (0.8*battery_capacity) - current_charge # only charging to 80% max


    class Simulation:
        def __init__(self, sim_duration, num_robots, cars_20, cars_40, cars_60):
            self.num_robots = num_robots
            self.robots = []
            self.sim_duration = sim_duration
            self.cars_20 = cars_20
            self.cars_40 = cars_40
            self.cars_60 = cars_60
            self.car_queue = []
            self.total_cars_charged = 0
            self.simulation_time = 0
            self.car_id_counter = 0

        def deploy_robots(self):
            for i in range(self.num_robots):
                robot = Robot(rob_id = i+1, 
                             capacity= ROBOT_BATTERY_CAPACITY, 
                             charge_rate = ROBOT_CHARGE_RATE_KWH_PER_HOUR, 
                             recharge_threshold=RECHARGE_THRESHOLD)
                self.robots.append(robot)

        def car_list(self):
            for i in range(self.cars_20):
                car= Car(i+1, CAR_BATTERY_CAPACITY, 0.6*CAR_BATTERY_CAPACITY) #only need to charge from 60-80%
                self.car_queue.append(car)

            for i in range(self.cars_40):
                car = Car(i+self.cars_20+1, CAR_BATTERY_CAPACITY, 0.4*CAR_BATTERY_CAPACITY) # only need to charge from 40-80%
                self.car_queue.append(car)

            for i in range(self.cars_60):
                car = Car(i+self.cars_20 + self.cars_40 + 1, CAR_BATTERY_CAPACITY, 0.2*CAR_BATTERY_CAPACITY) # only need to charge from 20-80
                self.car_queue.append(car)

            # shuffle cars
            random.shuffle(self.car_queue)

        def assign_cars_to_robots(self):
            for robot in self.robots:
                if self.car_queue:
                    potential_car = self.car_queue[0]
                    robot.check_battery_pct(potential_car)
                if robot.is_available():
                    car = self.car_queue.pop()
                    robot.current_car =car
                    robot.state = "charging"
                    print(f"Robot {robot.rob_id} is charging car {robot.current_car.cid}")
                    print(f"Car current charge: {car.current_charge/CAR_BATTERY_CAPACITY}")
                    print(f"Car needed charge: {car.needed_energy/CAR_BATTERY_CAPACITY}")

        def run_sim(self):
            self.deploy_robots()
            self.car_list()
            time_elapsed = [robot.time_elapsed for robot in self.robots]
            while (time_elapsed[0] < self.sim_duration):
                if not self.car_queue: 
                    break
                self.assign_cars_to_robots()
                for robot in self.robots:
                    robot.update()
                time_elapsed = [robot.time_elapsed for robot in self.robots]
                print("Time elapsed: ", time_elapsed[0])
                print(" ")
            for robot in self.robots:
                self.total_cars_charged += robot.cars_charged


        def report_results(self):  
            print("\n--- Simulation Results ---")
            time_elapsed = [robot.time_elapsed for robot in self.robots]
            print(f"Total simulation time: {time_elapsed[0]:.2f} hours")
            print(f"Overall cars charged: {self.total_cars_charged}")
            print(f"Fraction of total input cars charged: {(self.total_cars_charged/(self.cars_20 + self.cars_40 + self.cars_60))*100}%")
            print("Robot performance:")
            for robot in self.robots:
                print(f"  Robot {robot.rob_id}:")
                print(f"    Cars charged in {self.sim_duration}h: {robot.cars_charged}")
                print(f"    Final battery level: {robot.battery_level:.2f} kWh")


    return (Simulation,)


@app.cell
def _():
    return


@app.cell
def _(Simulation):
    simulation = Simulation(sim_duration=24, 
                           num_robots=2, 
                           cars_20 = 0, 
                           cars_40 = 0, 
                           cars_60 = 30)
    simulation.run_sim()
    simulation.report_results()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
