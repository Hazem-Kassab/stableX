# cantilever.py

import stablex as stx

l = 3000

n1 = stx.Node(0, 0)
n11 = stx.Node(0, 0)
n2 = stx.Node(1, l)

section = stx.Rectangle(200, 2000)


s1 = stx.LinearRotationalSpringElement(n1, n11, 1e14)
e1 = stx.FrameElement(n11, n2, section, True)

n1.x_dof.restrained = True
n1.y_dof.restrained = True
n1.rz_dof.restrained = True

n11.x_dof = n1.x_dof
n11.y_dof = n1.y_dof

p = 1

n2.y_dof.force = -p

structure = stx.Structure([s1, e1])

solver = stx.EigenSolver(structure)
eigenvalue, eigenvector = solver.solve(mode_shape=2)
stx.plot_structure(structure, scale=1000)
