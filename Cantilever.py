import matplotlib.pyplot as plt

import stableX as stx

n1 = stx.Node(0, 0)
n11 = stx.Node(0, 0)
n2 = stx.Node(0, 3000)

section = stx.Rectangle(200, 2000)

s1 = stx.LinearRotationalSpringElement(n1, n11, 2e20)
e1 = stx.FrameElement(n11, n2, section)

n1.x_dof.restrained = True
n1.y_dof.restrained = True
n1.rz_dof.restrained = True

n11.x_dof = n1.x_dof
n11.y_dof = n1.y_dof

n2.x_dof.force = 1e4

structure = stx.Structure([s1, e1])

solver = stx.Solver(structure)
solver.solve_first_order_elastic()

stx.plot_structure(structure)
plt.show()
