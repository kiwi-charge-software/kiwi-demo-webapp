# Kiwi Charge Demo- Webapp

### Jumana Fathima | Version 1.0 | Last updated: 06/03/25

### Context:

Many people we spoke to (investors, property managers) wanted to understand how we got to the numbers we did, when we made claims about how many vehicles Kiwi Charge could service in a multi-unit building. To help answer questions, and create a more dynamic (but not _super_ accurate) projection, we created this demo tool.

This repository contains code that has the simulation, as well as the demo code that displays the output of the simulation based on some adjustable parameters.

### Screenshots 
See a screenshot of this below:

<img src="images/Screenshot 2025-06-04 at 2.39.58 PM.png" height=500 />
<img src="images/Screenshot 2025-06-04 at 2.39.36 PM.png" height=500/>

### Stack
The raw simulation code can be found in `sim.py` and is written in Python. The visualizations are done on [marimo](https://marimo.io/) to run this simulation (easier than creating a tailwind/react native app for the first version.) The app will be hosted on github pages (for now). To run the app locally, run `marimo edit` after cloning this repo.