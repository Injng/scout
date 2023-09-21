# scout
## Dependencies
`networkx` was used to create the graph for the model city.
Washington DC was used as a proof of concept for our application.
`numpy` can be used as a dependency for linear algebra predictions, if using Markov matrices.
`flask` was used to create a web interface for the algorithm.
## Running
To run the application, run the `app.py` file with the following:
```
python3 app.py
```
## Using
In the interface, click the "Send Data" button to send location data and receive the optimal location for an Uber.
To simulate more Ubers, edit the `data/ubers.csv` file by adding an index, latitude, and longitude for the Uber location.
