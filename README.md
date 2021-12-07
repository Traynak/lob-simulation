# lob-simulation


## Description
The 


## LOB Data Structures
- order_book - dictionary contains all orders
```
"order_id": {
              "action": "bid" or "ask",
              "order_id": integer,
              "user_id": UUID,
              "quantity": integer,
              "price": integer,
              "timestamp": datetime.datetime.now()
          }
```          
- offer_queue - array of ask order_ids sorted by price
- bid_queue - array of bid order_ids sorted by price


## Install Instructions
##### Run on your local machine in a virtual environment with Python3.
* git clone https://github.com/Traynak/lob-simulation.git
* virtualenv -p python3 3envname
* source 3envname/bin/activate
* cd lob-simulation
* pip3 install -r requirements.txt
* python LOB-simulation.py

##### Run on your local machine with Docker.
- git clone https://github.com/Traynak/lob-simulation.git
- cd lob-simulation
- docker build -t lob-sim .
- docker run --name lob-sim -p 5001:5001 lob-sim



## References
*  [Reference]()
*  [LOB Class](https://github.com/FR4NKESTI3N/Limit-Order-Book-Simulation)
