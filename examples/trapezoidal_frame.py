# trapezoidal_frame.py

import stablex as stx

node_1 = stx.Node(0, 0)
node_2 = stx.Node(10000, 0)
node_3 = stx.Node(2500, 5000)
node_4 = stx.Node(7500, 5000)

section = stx.UserDefinedSection(area=1000, inertia=1e6)

element_1 = stx.FrameElement(node_1, node_3, section, True)
element_2 = stx.FrameElement(node_2, node_4, section, True)
element_3 = stx.FrameElement(node_3, node_4, section, True)


frame = stx.Structure([element_1, element_2, element_3])

# assign boundary conditions
node_1.x_dof.restrained = True
node_1.y_dof.restrained = True
node_1.rz_dof.restrained = True

node_2.x_dof.restrained = True
node_2.y_dof.restrained = True
node_2.rz_dof.restrained = True

# assign loading
node_3.y_dof.force = -1
node_4.y_dof.force = -1


solver = stx.EigenSolver(frame)
eigenvalue, eigenvector = solver.solve(mode_shape=1)
stx.plot_structure(frame, -1000)
