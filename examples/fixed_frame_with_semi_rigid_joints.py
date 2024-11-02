# frame_with_springs
import math

import stablex as stx

node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, 3000)
node_3 = stx.Node(0, 6000)
node_4 = stx.Node(6000, 6000)
node_5 = stx.Node(6000, 3000)
node_6 = stx.Node(6000, 0)

node_33 = stx.Node(0, 6000)
node_44 = stx.Node(6000, 6000)

node_33.x_dof = node_3.x_dof
node_33.y_dof = node_3.y_dof

node_44.x_dof = node_4.x_dof
node_44.y_dof = node_4.y_dof

section = stx.Rectangle(100, 100)


e1 = stx.FrameElement(node_1, node_2, section, include_geom_nonlinearity=True)
e2 = stx.FrameElement(node_2, node_3, section, include_geom_nonlinearity=True)
e3 = stx.FrameElement(node_33, node_44, section, include_geom_nonlinearity=False)
e4 = stx.FrameElement(node_4, node_5, section, include_geom_nonlinearity=True)
e5 = stx.FrameElement(node_5, node_6, section, include_geom_nonlinearity=True)

kb = e1.elasticity_modulus * section.inertia / 6000
ks = 1e6*kb

s1 = stx.LinearRotationalSpringElement(node_3, node_33, ks)
s2 = stx.LinearRotationalSpringElement(node_4, node_44, ks)

node_1.x_dof.restrained = True
node_1.y_dof.restrained = True
node_1.rz_dof.restrained = True

node_6.x_dof.restrained = True
node_6.y_dof.restrained = True
node_6.rz_dof.restrained = True

p = 1

node_3.y_dof.force = -p
node_4.y_dof.force = -p

structure = stx.Structure([e1, e2, e3, e4, e5, s1, s2])

solver = stx.EigenSolver(structure)

eigenvalue, eigenvector = solver.solve(mode_shape=1)

stx.plot_structure(structure, 1000)
