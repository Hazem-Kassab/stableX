import math
import stableX as stx

import matplotlib.pyplot as plt


l = 3000

n1 = stx.Node(0, 0)
n2 = stx.Node(10, 0.25*l)
n3 = stx.Node(0, 0.5*l)
n4 = stx.Node(-10, 0.75*l)
n5 = stx.Node(0, l)

section = stx.Rectangle(100, 100)

e1 = stx.FrameElement(n1, n2, section, True)
e2 = stx.FrameElement(n2, n3, section, True)
e3 = stx.FrameElement(n3, n4, section, True)
e4 = stx.FrameElement(n4, n5, section, True)

n1.x_dof.restrained = True
n1.y_dof.restrained = True
# n1.rz_dof.restrained = True
n3.x_dof.restrained = True
n5.x_dof.restrained = True

p = -7.3e6

n5.y_dof.force = p

structure = stx.Structure([e1, e2, e3, e4])


solver = stx.NonlinearSolver(structure)
solver.solve_incrementally(100, n5.y_dof, n5.y_dof)

print(n5.y_dof.displacement)
print(4*math.pi**2 * e1.elasticity_modulus*section.inertia/l**2 / 1e6)

stx.plot_structure(structure, 1)

stx.plot(solver.displacement, solver.load)

