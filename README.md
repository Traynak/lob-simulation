# lob-simulation

## References
*  [DrAshBooth's PyLOB Implementation](https://github.com/DrAshBooth/PyLOB/wiki/Implementation)

## Description
The lob-simulation project simulates a probabilistic Limit Order Book (LOB) with various Random Variables for price, quantity, trades, etc. The LOB implementation utilizes data structures to represent queueing theory in the arrival and departures of traders and trades allowing traders 4 basic types of trades: bid order, ask order, market buy order, market sell order.


## Install Instructions
##### Run on your local machine in a virtual environment with Python3.
```sh
git clone https://github.com/Traynak/lob-simulation.git
virtualenv -p python3 3envname
source 3envname/bin/activate
cd lob-simulation
pip3 install -r requirements.txt
python LOB-simulation.py
```

##### Run on your local machine with Docker.
```sh
git clone https://github.com/Traynak/lob-simulation.git
cd lob-simulation
docker build -t lob-sim .
docker run --name lob-sim
```

## Simulation Reporting
The `LOB-simulation.py` file leverages plotly to generate several images for visualizing the simulation results over time. The Figure below is an example of an image produced showing the evolving state of the LOB modeled with the best bid (blue) and best ask (red) for each simulated period.

<img src="images/lob_evolution.png"  width="700" height="500">
<br><br>

