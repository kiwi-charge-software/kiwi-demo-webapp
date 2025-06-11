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
    import sim

    return mo, sim


@app.cell(hide_code=True)
def _(mo):
    sim_duration = mo.ui.slider(label="Number of hours to run the simulation", show_value=True, start=1, stop=24)
    num_robots = mo.ui.slider(label="Number of bots", show_value=True, start=1, stop=10)
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

    ⚡ Within the **{round(max(result[2]), 2)} hours** that the simulation ran for, the **{num_robots.value} kiwi(s) were able to charge {sum(result[1])} unique cars in a day**. The Kiwi provided {sum(result[4])} kWh in total across all the cars, adding {round(sum(result[4])*0.16, 2)} km of range across the parking lot.

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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
