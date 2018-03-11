## Solving Travelling Salesman Problem using Ant Colony Optimization

#### Install dependencies
`pip install -r requirements.txt`

#### Usage
The demo is given in the last section of the file. You can also import this file and do the following -
```python
// Instantiate SolveTSPUsingACO passing the desired parameters
acs = SolveTSPUsingACO(mode='ACS')
// Run the optimization
acs.run()
// Plot the tour
acs.plot()
```

#### Example
```python
acs = SolveTSPUsingACO(mode='ACS', colony_size=5, steps=50, num_nodes=15, x_range=(-400, 400), y_range=(-400, 400))
acs.run()
acs.plot()
elitist = SolveTSPUsingACO(mode='Elitist', colony_size=5, steps=50, nodes=acs.nodes)
elitist.run()
elitist.plot()
max_min = SolveTSPUsingACO(mode='MaxMin', colony_size=5, steps=50, nodes=acs.nodes)
max_min.run()
max_min.plot()
```

#### Output
```
Started: ACS
Ended: ACS
Tour: [2 -> 14 -> 1 -> 6 -> 12 -> 15 -> 8 -> 4 -> 7 -> 3 -> 5 -> 10 -> 13 -> 11 -> 9 -> 2]
Distance: 2893.66

Started: Elitist
Ended: Elitist
Tour: [4 -> 8 -> 15 -> 12 -> 6 -> 1 -> 14 -> 2 -> 9 -> 11 -> 13 -> 10 -> 5 -> 7 -> 3 -> 4]
Distance: 2818.66

Started: MaxMin
Ended: MaxMin
Tour: [7 -> 3 -> 4 -> 8 -> 15 -> 12 -> 6 -> 1 -> 14 -> 2 -> 9 -> 11 -> 13 -> 10 -> 5 -> 7]
Distance: 2818.66
```

#### Plots
ACS  
![ACS Tour](ACS_tour.png "ACS Tour")  
Elitist  
![Elitist Tour](Elitist_tour.png "Elitist Tour")   
MaxMin  
![MaxMin Tour](MaxMin_tour.png "MaxMin Tour")

#### Reference
www.theprojectspot.com/tutorial-post/ant-colony-optimization-for-hackers/10
