# overhang.py

import stablex as stx

node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, 3000)
node_3 = stx.Node(0, 4500)

section = stx.UserDefinedSection(area=1000, inertia=1e6)

element_1 = stx.FrameElement(node_1, node_2, section, True)
element_2 = stx.FrameElement(node_2, node_3, section, True)

overhang = stx.Structure([element_1, element_2])

# assign boundary conditions
node_1.x_dof.restrained = True
node_1.y_dof.restrained = True
node_1.rz_dof.restrained = True
node_2.x_dof.restrained = True

# assign loading
node_3.y_dof.force = -1

solver = stx.EigenSolver(overhang)
eigenvalues, eigenvectors = solver.solve(mode_shape=1)
stx.plot_structure(overhang, scale=1000)
