# frame_with_springs

import stablex as stx

w = 6000
h = 6000
a = 0.1

# column nodes
node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, h/5)
node_3 = stx.Node(0, 2*h/5)
node_4 = stx.Node(0, 3*h/5)
node_5 = stx.Node(0, 4*h/5)
node_6 = stx.Node(0, h)

node_7 = stx.Node(2*w, 0)
node_8 = stx.Node(2*w, h/5)
node_9 = stx.Node(2*w, 2*h/5)
node_10 = stx.Node(2*w, 3*h/5)
node_11 = stx.Node(2*w, 4*h/5)
node_12 = stx.Node(2*w, h)

node_13 = stx.Node(w, h + a*w)

width = 100
kb_kc = 5

# section
column_profile = stx.UserDefinedSection(area=2850000, inertia=1943e4)
beam_profile = column_profile

# left column elements
c1 = stx.FrameElement(node_1, node_2, column_profile, True)
c2 = stx.FrameElement(node_2, node_3, column_profile, True)
c3 = stx.FrameElement(node_3, node_4, column_profile, True)
c4 = stx.FrameElement(node_4, node_5, column_profile, True)
c5 = stx.FrameElement(node_5, node_6, column_profile, True)

# right column elements
c6 = stx.FrameElement(node_7, node_8, column_profile, True)
c7 = stx.FrameElement(node_8, node_9, column_profile, True)
c8 = stx.FrameElement(node_9, node_10, column_profile, True)
c9 = stx.FrameElement(node_10, node_11, column_profile, True)
c10 = stx.FrameElement(node_11, node_12, column_profile, True)

# beam elements
b1 = stx.FrameElement(node_6, node_13, beam_profile, True)
b2 = stx.FrameElement(node_13, node_12, beam_profile, True)

# spring elements

# boundary conditions
node_1.x_dof.restrained = True
node_1.y_dof.restrained = True
node_1.rz_dof.restrained = True

node_7.x_dof.restrained = True
node_7.y_dof.restrained = True
node_7.rz_dof.restrained = True

# loading
p = 1

node_6.y_dof.force = -p
node_12.y_dof.force = -p
node_13.y_dof.force = -2*p

structure = stx.Structure([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, b1, b2])
solver = stx.EigenSolver(structure)
eigenvalue, eigenvector = solver.solve(mode_shape=1)
stx.plot_structure(structure, 1500)
