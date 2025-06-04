import marimo

__generated_with = "0.13.11"
app = marimo.App(
    width="full",
    app_title="Kiwi Charge Demonstration",
    css_file="/Users/jumana/Documents/code/python-notebooks/custom.css",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    from matplotlib import pyplot as plt
    import random
    import sim

    return mo, sim


@app.cell(hide_code=True)
def _(mo):
    sim_duration = mo.ui.slider(label="Number of hours to run the simulation", show_value=True, start=1, stop=24)
    num_robots = mo.ui.slider(label="Number of bots", show_value=True, start=1, stop=5)
    cars_20 = mo.ui.slider(label="Number of cars that need 20% charge", show_value=True, start=0, stop=100)
    cars_40 = mo.ui.slider(label="Number of cars that need 40% charge", show_value=True, start=0, stop=100)
    cars_60 = mo.ui.slider(label="Number of cars that need 60% charge", show_value=True, start=0, stop=100)
    return cars_20, cars_40, cars_60, num_robots, sim_duration


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # 🥝 Welcome to the Kiwi Charge Demo! 🥝

    This simulation illustrates how Kiwi Charge's autonomous chargers replaces fixed chargers in your building. 

    Set your parameters to see how many cars Kiwi can service, and your total cost for this infrastructure.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## 🧠 Simulation Assumptions

    This simulation is not perfect -- but it does assume the worst-case. Our more accurate models will include Kiwi smart charging capabilities, allowing it to charge more vehicles than it does in this simulation.

    We assume:

    1) Kiwis are operating at random to charge the vehicles-- there is no "smart" charging to _efficiently_ charge cars

    2) Kiwi units are assumed to be a 45-kW unit, dispensing and recharging itself at Level 3 speeds

    3) Vehicles are set to be at a consistent battery capacity (70 kWh) - there is no variation in user battery size.

    4) All vehicles are present at the time of charging, and configured correctly - there's no missing/misconfigured vehicles.
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

    * Daily charging window (1 hour to 24 hours)
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
def _(cars_20, cars_40, cars_60, num_robots, sim, sim_duration):
    simulation = sim.Simulation(sim_duration=sim_duration.value, 
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
def _(num_robots, result):
    # kiwi cost calculation rq
    cost = 90
    if num_robots.value % 4 == 0:
        cost += (num_robots.value / 4)* 90
    cost += num_robots.value*45

    cost = cost*1000

    formatted_cost = f"${cost:,}"

    fixed_cost = sum(result[1])*10000
    formatted_fixed_cost = f"${fixed_cost:,}"

    savings = fixed_cost - cost
    formatted_savings = f"${savings}"
    return formatted_cost, formatted_fixed_cost, formatted_savings


@app.cell
def _(
    cars_20,
    cars_40,
    cars_60,
    formatted_cost,
    formatted_fixed_cost,
    formatted_savings,
    mo,
    num_robots,
    result,
):
    mo.md(
        f"""
    -----

    ## 🤖 Simulation Results

    🥝 It took {num_robots.value} kiwi(s) {round(max(result[2]), 2)} hours to charge {sum(result[1])} unique cars.

    🚘 It was able to charge **{round((sum(result[1])/(cars_20.value + cars_40.value + cars_60.value))*100, 2)}**% of the cars on the parking lot.

    ⚡ The Kiwi dispensed **{sum(result[4])}** kWh total.

    ------
    ## 💵 Cost breakdown

    💰 If you had placed fixed chargers to service the {sum(result[1])} unique cars, it would have cost you **{formatted_fixed_cost}**.

    🔖 With Kiwi Charge, you will be paying **{formatted_cost}** to service the same cars. This results in {formatted_savings} of savings for you!


    -----
    ## ⏱️ Time breakdown
    📉 Installing fixed chargers is a time intensive process, that takes anywhere between **12-24 months**. 

    📈 With Kiwi Charge, you will only need **1-3 business days** to replace {sum(result[1])} fixed chargers!
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
