# frame_with_springs
import math

import numpy as np

import src.stablex as stx

# column nodes
node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, 1200)
node_3 = stx.Node(0, 2400)
node_4 = stx.Node(0, 3600)
node_5 = stx.Node(0, 4800)
node_6 = stx.Node(0, 6000)

node_7 = stx.Node(6000, 0)
node_8 = stx.Node(6000, 1200)
node_9 = stx.Node(6000, 2400)
node_10 = stx.Node(6000, 3600)
node_11 = stx.Node(6000, 4800)
node_12 = stx.Node(6000, 6000)

# dummy nodes
node_66 = stx.Node(0, 6000)
node_122 = stx.Node(6000, 6000)
node_111 = stx.Node(0, 0)
node_77 = stx.Node(6000, 0)

# coupling
node_66.x_dof = node_6.x_dof
node_66.y_dof = node_6.y_dof

node_122.x_dof = node_12.x_dof
node_122.y_dof = node_12.y_dof

node_111.x_dof = node_1.x_dof
node_111.y_dof = node_1.y_dof

node_77.x_dof = node_7.x_dof
node_77.y_dof = node_7.y_dof


# section
column_profile = stx.UserDefinedSection(area=2850, inertia=1943e4)
beam_profile = stx.UserDefinedSection(area=2850, inertia=column_profile.inertia)

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
b1 = stx.FrameElement(node_66, node_122, beam_profile)


kc = c1.elasticity_modulus * column_profile.inertia / 6000

a1 = 0.5
a2 = 0.0001
ks1 = kc/a1
ks2 = kc/a2

# spring elements at connection
s1 = stx.LinearRotationalSpringElement(node_6, node_66, ks2)
s2 = stx.LinearRotationalSpringElement(node_12, node_122, ks2)

# spring elements at base
s3 = stx.LinearRotationalSpringElement(node_1, node_111, ks1)
s4 = stx.LinearRotationalSpringElement(node_7, node_77, ks1)

# boundary conditions
node_111.x_dof.restrained = True
node_111.y_dof.restrained = True
node_111.rz_dof.restrained = True

node_77.x_dof.restrained = True
node_77.y_dof.restrained = True
node_77.rz_dof.restrained = True

# loading
p = 1

node_6.y_dof.force = -p
node_12.y_dof.force = -p

structure = stx.Structure([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, b1, s1, s2, s3, s4])

euler_load = math.pi ** 2 * c1.elasticity_modulus * column_profile.inertia / 6000 ** 2
solver = stx.EigenSolver(structure)
# eigenvalue, eigenvector = solver.solve(mode_shape=1)
# print("%.4f" % (eigenvalue/euler_load))

range_ks_kc = np.arange(start=0.1, stop=20.1, step=0.1)
r_list = []

for ratio in range_ks_kc:
    s1.rotational_stiffness = kc / ratio
    s2.rotational_stiffness = kc / ratio
    eigenvalue, eigenvector = solver.solve(mode_shape=1)
    print("%.4f" % (eigenvalue / euler_load))


stx.plot_structure(structure, 2000)
