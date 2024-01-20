# pinned_column.py
import math

import stableX as stx

# column length
l = 3000

# create nodes at quarter lengths
n1 = stx.Node(0, 0)
n2 = stx.Node(0, 0.25*l)
n3 = stx.Node(0, 0.5*l)  # introduce imperfection of 10 mm
n4 = stx.Node(0, 0.75*l)
n5 = stx.Node(0, l)

# create section
section = stx.Rectangle(100, 100)

# create Frame elements and specify node connectivity and geometric non-linearity
e1 = stx.FrameElement(n1, n2, section, True)
e2 = stx.FrameElement(n2, n3, section, True)
e3 = stx.FrameElement(n3, n4, section, True)
e4 = stx.FrameElement(n4, n5, section, True)

# assign boundary conditions (pinned at base, roller at top)
n1.x_dof.restrained = True
n1.y_dof.restrained = True
n5.x_dof.restrained = True

# assign load
p = -1
n5.y_dof.force = p

# create structure assembly of elements
structure = stx.Structure([e1, e2, e3, e4])

# # create a nonlinear solver object
# solver = stx.NonlinearSolver(structure)
#
# # solve in 100 load steps and record load at top and mid-span lateral displacement
# solver.solve_incrementally(200, n5.y_dof, n3.x_dof)
#
# # plot structure and deformation (buckled shape)
# stx.plot_structure(structure, 0.1)
# # plot recorded load-displacement curve
# stx.plot(solver.displacement, solver.load, "displacement (mm)", "load P (N)")
#
# print(n5.y_dof.displacement)

solver = stx.EigenSolver(structure)

eigenvalue, eigenvector = solver.solve(mode_shape=2)
print(eigenvalue)

stx.plot_structure(structure, 1000)

print(4 * math.pi**2 * e1.elasticity_modulus * section.inertia / l**2)
