import matplotlib.pyplot as plt

import stableX as stx

l = 3000

n1 = stx.Node(0, 0)
n11 = stx.Node(0, 0)
n2 = stx.Node(0, l)

section = stx.Rectangle(200, 2000)

s1 = stx.LinearRotationalSpringElement(n1, n11, 1e15)
e1 = stx.FrameElement(n11, n2, section)

n1.x_dof.restrained = True
n1.y_dof.restrained = True
n1.rz_dof.restrained = True

n11.x_dof = n1.x_dof
n11.y_dof = n1.y_dof

p = 1e4

n2.x_dof.force = p

structure = stx.Structure([s1, e1])


solver = stx.Solver(structure)
solver.solve_first_order_elastic()

print(n2.x_dof.displacement)
print(p*l**3/(3*e1.elasticity_modulus*section.inertia) -
      n11.rz_dof.displacement * l)

stx.plot_structure(structure, 1)
plt.show()
