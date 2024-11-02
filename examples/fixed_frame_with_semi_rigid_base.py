# frame_with_springs
import math

import numpy as np

import stablex as stx

node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, 3000)
node_3 = stx.Node(0, 6000)
node_4 = stx.Node(6000, 6000)
node_5 = stx.Node(6000, 3000)
node_6 = stx.Node(6000, 0)

node_11 = stx.Node(0, 0)
node_66 = stx.Node(6000, 0)

node_11.x_dof = node_1.x_dof
node_11.y_dof = node_1.y_dof

node_66.x_dof = node_6.x_dof
node_66.y_dof = node_6.y_dof

section = stx.UserDefinedSection(area=2850, inertia=1943e4)


e1 = stx.FrameElement(node_11, node_2, section, include_geom_nonlinearity=True)
e2 = stx.FrameElement(node_2, node_3, section, include_geom_nonlinearity=True)
e3 = stx.FrameElement(node_3, node_4, section)
e4 = stx.FrameElement(node_4, node_5, section, include_geom_nonlinearity=True)
e5 = stx.FrameElement(node_5, node_66, section, include_geom_nonlinearity=True)

kc = e1.elasticity_modulus * section.inertia / 6000
a = 1e-8
ks = kc/a

s1 = stx.LinearRotationalSpringElement(node_1, node_11, ks)
s2 = stx.LinearRotationalSpringElement(node_6, node_66, ks)

node_1.x_dof.restrained = True
node_1.y_dof.restrained = True
node_1.rz_dof.restrained = True

node_6.x_dof.restrained = True
node_6.y_dof.restrained = True
node_6.rz_dof.restrained = True

p = 1

# node_3.x_dof.force = 10000
node_3.y_dof.force = -p
node_4.y_dof.force = -p

structure = stx.Structure([e1, e2, e3, e4, e5, s1, s2])

solver = stx.EigenSolver(structure)
eigenvalue, eigenvector = solver.solve(mode_shape=1)
stx.plot_structure(structure, 1000)
