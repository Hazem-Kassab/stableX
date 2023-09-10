# stableX
 A Python library for stability analysis of frames

## Usage

```python
# frame_with_springs

from matplotlib import pyplot as plt
import stableX as stx

node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, 6000)
node_3 = stx.Node(6000, 6000)
node_4 = stx.Node(6000, 0)

node_22 = stx.Node(0, 6000)
node_33 = stx.Node(6000, 6000)

node_22.x_dof = node_2.x_dof
node_22.y_dof = node_2.y_dof

node_33.x_dof = node_3.x_dof
node_33.y_dof = node_3.y_dof

section = stx.Rectangle(100, 500)


e1 = stx.FrameElement(node_1, node_2, section)
e2 = stx.FrameElement(node_22, node_33, section)
e3 = stx.FrameElement(node_3, node_4, section)

s1 = stx.LinearRotationalSpringElement(node_2, node_22, 1e20)
s2 = stx.LinearRotationalSpringElement(node_3, node_33, 1e20)

node_1.x_dof.restrained = True
node_1.y_dof.restrained = True

node_4.x_dof.restrained = True
node_4.y_dof.restrained = True

node_2.x_dof.force = 5000000

structure = stx.Structure([e1, e2, e3, s1, s2])
solver = stx.Solver(structure)
solver.solve_first_order_elastic()

print(node_2.x_dof.displacement)

stx.plot_structure(structure)
plt.show()
```
## Output
 
![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Frame_with_springs.PNG?raw=true)

**The Cauchy-Schwarz Inequality**

$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$


## Cantilever Column with spring Example
![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Cantilever.PNG?raw=true)