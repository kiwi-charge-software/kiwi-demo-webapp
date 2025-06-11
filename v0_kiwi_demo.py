import marimo

__generated_with = "0.13.11"
app = marimo.App(
    width="full",
    app_title="Kiwi Charge Demonstration",
    css_file="/Users/jumana/Documents/code/python-notebooks/marimo-demo/custom.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    from matplotlib import pyplot as plt
    import random

    return mo, random


@app.cell(hide_code=True)
def _(random):
    # simulation code!

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
            self.battery_history = []
            self.kwh_dispensed = 0

        def update(self):
            if self.state == "charging":
                self.battery_level -= self.current_car.needed_energy
                self.time_elapsed += self.current_car.needed_energy / self.charge_rate 
                self.current_car.current_charge = self.current_car.needed_energy
                self.kwh_dispensed += self.current_car.needed_energy
                print("Car charged: ", self.current_car.cid)
                self.battery_history.append(self.battery_level)
                self.current_car = None
                self.cars_charged +=1
                self.state= "idle"


            elif self.state == "recharging":
                self.time_elapsed += (self.battery_capacity - self.battery_level) /self.charge_rate
                self.battery_level = self.battery_capacity
                self.battery_history.append(self.battery_level)
                self.state = "idle"
                print(f"Robot {self.rob_id} is done charging")

        

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
            time_elapsed = max([robot.time_elapsed for robot in self.robots])
            while (time_elapsed < self.sim_duration):
                if not self.car_queue: 
                    break
                self.assign_cars_to_robots()
                for robot in self.robots:
                    robot.update()
                time_elapsed = max([robot.time_elapsed for robot in self.robots])
                print("Time elapsed: ", time_elapsed)
                print(" ")
            for robot in self.robots:
                self.total_cars_charged += robot.cars_charged


        def report_results(self):  
            print("\n--- Simulation Results ---")
            time_elapsed = max([robot.time_elapsed for robot in self.robots])
            print(f"Total simulation time: {time_elapsed} hours")
            print(f"Overall cars charged: {self.total_cars_charged}")
            print(f"Fraction of total input cars charged: {(self.total_cars_charged/(self.cars_20 + self.cars_40 + self.cars_60))*100}%")
            print()
            print("Robot performance:")
            for robot in self.robots:
                print(f"  Robot {robot.rob_id}:")
                print(f"    Cars charged in {self.sim_duration}h: {robot.cars_charged}")
                print(f"    Final battery level: {robot.battery_level:.2f} kWh")
            return [robot.battery_history for robot in self.robots], [robot.cars_charged for robot in self.robots], [robot.time_elapsed for robot in self.robots], [robot.rob_id for robot in self.robots], [robot.kwh_dispensed for robot in self.robots]

        def plot_battery_history(self):
            print((self.robots[0].battery_history))
            print(self.robots[0].cars_charged)
            # for robot in self.robots:
            #     plt.plot(np.arange(robot.cars_charged), robot.battery_history, label=f"Robot {robot.rob_id}")
    return (Simulation,)


@app.cell(hide_code=True)
def _(mo):
    sim_duration = mo.ui.slider(label="Number of hours Kiwi is operational", show_value=True, start=1, stop=24)
    num_robots = mo.ui.slider(label="Number of Kiwi bots", show_value=True, start=1, stop=10)
    cars_20 = mo.ui.slider(label="Number of cars that need 20% charge", show_value=True, start=0, stop=150)
    cars_40 = mo.ui.slider(label="Number of cars that need 40% charge", show_value=True, start=0, stop=150)
    cars_60 = mo.ui.slider(label="Number of cars that need 60% charge", show_value=True, start=0, stop=150)
    return cars_20, cars_40, cars_60, num_robots, sim_duration


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # ⚡ Welcome to the future of EV charging!

    This simulation illustrates how Kiwi Charge's autonomous chargers replaces fixed chargers in your building. Set your parameters to see how many cars Kiwi can service, and your total cost for this infrastructure.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## 🧮 Set your parameters for the simulation

    Use the sliders below to set the following values: 

    * Daily charging window (1 hour to 24 hours)- we recommend setting this to 12 hours to mimic overnight charging
    * Number of active Kiwis during the charging window
    * Number of vehicles that require 20%, 40%, and 60% charge

    (Make sure that you have at least *one* car in the input - otherwise, you won't see any results!)
    """
    )
    return


@app.cell(hide_code=True)
def _(cars_20, cars_40, cars_60, mo, num_robots, sim_duration):
    mo.vstack([sim_duration, num_robots, cars_20, cars_40, cars_60])
    return


@app.cell
def _(Simulation, cars_20, cars_40, cars_60, num_robots, sim_duration):
    simulation = Simulation(sim_duration=sim_duration.value, 
                           num_robots=num_robots.value, 
                           cars_20 = cars_20.value, 
                           cars_40 = cars_40.value, 
                           cars_60 = cars_60.value)
    return (simulation,)


@app.cell
def _(simulation):
    simulation.run_sim()
    result = simulation.report_results()
    return (result,)


@app.cell
def _(cars_20, cars_40, cars_60, result):
    # fraction of cars charged
    total_cars = cars_20.value + cars_40.value + cars_60.value
    frac_charged = sum(result[1])/total_cars

    frac_charged = round(frac_charged, 2)*100

    frac_charged_month = (sum(result[1])*3) /total_cars
    frac_charged_month = round(frac_charged_month*100, 1)
    return frac_charged_month, total_cars


@app.cell
def _(num_robots, total_cars):
    # kiwi cost calculation rq
    cost = 90
    if num_robots.value % 4 == 0:
        cost += (num_robots.value / 4)* 90
    cost += num_robots.value*45

    cost = cost*1000

    formatted_cost = f"${cost:,}"

    fixed_cost = total_cars*10000
    formatted_fixed_cost = f"${fixed_cost:,}"

    savings = fixed_cost - cost
    formatted_savings = f"${savings}"
    return formatted_cost, formatted_fixed_cost


@app.cell
def _(
    formatted_cost,
    formatted_fixed_cost,
    frac_charged_month,
    mo,
    num_robots,
    result,
    total_cars,
):
    mo.md(
        f"""
    -----

    ## 🥝 The Kiwi Charge Advantage

    ⚡ Within the **{round(max(result[2]), 2)} hours** that the simulation ran for, the **{num_robots.value} kiwi(s) were able to charge {sum(result[1])} unique cars in a day**. The Kiwi provided **{sum(result[4])} kWh** in total across all the cars, adding **{round(sum(result[4])*5, 2)} km of range** across the parking lot.

    🚗 In a month, {num_robots.value} kiwi(s) would service **{sum(result[1])*3} unique cars of the same charging needs, which is {frac_charged_month}% of your parking lot.**

    ⏱️ Installing fixed chargers is a time intensive process, that takes anywhere between **12-24 months**. With Kiwi Charge, you will only need **1-3 business days** to electrify the entire parking lot!

    💰 With {total_cars} cars on your parking lot, **your building would have needed {total_cars} level 2** fixed chargers, which would **cost you {formatted_fixed_cost} **in just hardware costs. However, **with Kiwi Charge**, you can **service the cars in your parking lot at level 3 speeds, at a complete price of {formatted_cost}** ({num_robots.value} kiwi bot(s)).
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Assumptions for the model
    * _Kiwi Operations: Kiwis are operating at random to charge the vehicles, and not doing so with the personalization that we have in our real bots_
    * _Kiwi Capacity: Units are 45-kW, and dispense/recharge themselves at Level 3 speeds_
    * _Price: We assume that the cost of one fixed level 2 charger is roughly $10,000 CAD (only hardware, excluding operations and utility costs)_
    """
    )
    return


if __name__ == "__main__":
    app.run()
