# Solving Travelling Salesman Problem using Ant Colony Optimization (ACS/Elitist/MaxMin)

**Reference** - www.theprojectspot.com/tutorial-post/ant-colony-optimization-for-hackers/10

**Recommended** - Python 2.7

You will have to install **Pillow** as a requirement to use **draw_tour()**

The demo is given in the last section of the file. You can also import this file into another and follow the steps below -
1. Create an object of the AntColonyOptimization class passing the desired parameters -
   - `acs = AntColonyOptimization(mode='ACS')` or
   - `acs = AntColonyOptimization(mode='ACS', nodes=[(1,3),(5,6),(2,5),(30,4)])`
2. Run the optimization -
    `acs.run()`
3. Draw the tour -
    `acs.draw_tour()`

**Demo Output** - 
1. ACS

![image](https://cloud.githubusercontent.com/assets/14920774/24602433/60adab84-187a-11e7-811b-a827ed48650f.png)

2. Elitist

![image](https://cloud.githubusercontent.com/assets/14920774/24602450/6baf85c0-187a-11e7-98a1-3416004f0dbd.png)

3. MaxMin

![image](https://cloud.githubusercontent.com/assets/14920774/24602452/6fde2b2e-187a-11e7-80a6-556e734f840a.png)
