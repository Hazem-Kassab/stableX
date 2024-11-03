# pinned_column.py

import stablex as stx

# column length
l = 3000

# create nodes at quarter lengths
n1 = stx.Node(0, 0)
n2 = stx.Node(0, 0.25*l)
n3 = stx.Node(0, 0.5*l)
n4 = stx.Node(0, 0.75*l)
n5 = stx.Node(0, l)

# create section

section = stx.Rectangle(100, 100)
# create Frame elements and specify node connectivity and geometric non-linearity
e1 = stx.FrameElement(n1, n2, section, True)
e2 = stx.FrameElement(n2, n3, section, True)
e3 = stx.FrameElement(n3, n4, section, True)
e4 = stx.FrameElement(n4, n5, section, True)

# create structure assembly of elements
structure = stx.Structure([e1, e2, e3, e4])

# assign boundary conditions (pinned at base, roller at top)
n1.x_dof.restrained = True
n1.y_dof.restrained = True
n5.x_dof.restrained = True

# assign load
n5.y_dof.force = -1

solver = stx.EigenSolver(structure)

eigenvalue, eigenvector = solver.solve(mode_shape=1)

print(f"Critical Buckling Load: {eigenvalue:.3f} N")

stx.plot_structure(structure, 1000)
