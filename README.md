# Collaborative and intercommunicated mobile cyber-physical system

The activities of this project include:
1. Long Range communications protocol implemented in actual LoRa transceivers that aim to transmit low-frequency data between them.

![LoRa_bb](https://user-images.githubusercontent.com/58990107/190847572-1586fdb9-327f-4cee-9e63-fcb78f55a624.png)

2. Randomly generated data (Synthetic data) using consistent values from a previous research of variables of interest and real-time readings for a simple sensor station to simulate real data. 

![LoRa](https://user-images.githubusercontent.com/58990107/190847473-4385b4f1-0c05-4ff7-aa09-94bb4f01e0fb.png) ![Synthetic data](https://user-images.githubusercontent.com/58990107/190847527-c635cb84-4e1d-404b-b8d8-25466537c21c.png)

3. The design of a HMI that can showcase a dashboard of selected variables, implemented in InfluxDB. (TCP based). For a visualization of data in real-time.
   - Variables sucha as:
     - Weather variables as Temperature and Humidity
     - An interruption Alarm
     - Distance from an object
     - GPS position
     - IMU information
     - Speed of the vehicle
     - Fuel level

![dashboard_result](https://user-images.githubusercontent.com/58990107/190847462-f86f1cc9-10a4-4034-bbea-aa7e770c8fab.png)
