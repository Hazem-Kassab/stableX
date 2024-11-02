import math

import numpy as np

import stableX as stx

import matplotlib.pyplot as plt

h = 6000  # storey height
l = 6000  # span
n = 50  # number of stories

column_profile = stx.UserDefinedSection(area=1e10, inertia=1943e4)
beam_profile = stx.UserDefinedSection(area=1e10, inertia=column_profile.inertia)

elements = []
springs = []
left_columns = []

node_n_left = stx.Node(0, n*h)
node_n_right = stx.Node(l, n*h)
node_n_s_left = stx.Node(0, n * h)
node_n_s_right = stx.Node(l, n * h)

node_n_right.y_dof.force = -1
node_n_left.y_dof.force = -1

for i in range(n-1, -1, -1):
    node_left = stx.Node(0, i*h)
    node_right = stx.Node(l, i*h)
    node_s_left = stx.Node(0, i*h)
    node_s_right = stx.Node(l, i*h)

    # coupling
    node_n_s_left.x_dof = node_n_left.x_dof
    node_n_s_left.y_dof = node_n_left.y_dof
    node_n_s_right.x_dof = node_n_right.x_dof
    node_n_s_right.y_dof = node_n_right.y_dof

    column_left = stx.FrameElement(node_left, node_n_left, column_profile, True)
    column_right = stx.FrameElement(node_right, node_n_right, column_profile, True)
    beam = stx.FrameElement(node_n_s_left, node_n_s_right, beam_profile)

    kb = beam.section.inertia * beam.elasticity_modulus / l**2
    a = 1e-10
    ks = kb/a

    spring_left = stx.LinearRotationalSpringElement(node_n_left, node_n_s_left, ks)
    spring_right = stx.LinearRotationalSpringElement(node_n_right, node_n_s_right, ks)

    elements.extend([column_left, column_right, beam, spring_left, spring_right])
    springs.extend([spring_right, spring_left])
    left_columns.append(column_left)

    node_n_left = node_left
    node_n_right = node_right
    node_n_s_left = node_s_left
    node_n_s_right = node_s_right
    if i == 0:
        node_left.x_dof.restrained = True
        node_left.y_dof.restrained = True
        node_left.rz_dof.restrained = True

        node_right.x_dof.restrained = True
        node_right.y_dof.restrained = True
        node_right.rz_dof.restrained = True


kb = beam.elasticity_modulus * beam.section.inertia / l

structure = stx.Structure(elements)

euler_load = math.pi ** 2 * column_left.elasticity_modulus * column_profile.inertia / h ** 2


solver = stx.EigenSolver(structure)
# eigenvalue, eigenvector = solver.solve(mode_shape=1)
# print(elements[0].start_node.rz_dof.displacement, elements[5].end_node.rz_dof.displacement)
# print("%.4f" % (eigenvalue/euler_load))
# stx.plot_structure(structure, 6e4)

# no_elements = len(elements)
# rotations = []
# stories_range = range(no_elements, -5, -5)
#
# for i in stories_range:
#     rotation = float(elements[i].start_node.rz_dof.displacement)
#     rotations.append(rotation*1e6)

# for column in left_columns:
#     rotations.append(float(column.end_node.rz_dof.displacement))
#
# rotations.append(float(left_columns[-1].start_node.rz_dof.displacement))
#
# for r in rotations:
#     print(r)
#
# plt.plot(np.array(stories_range)/5, rotations)
# plt.xticks(range(0, 21, 1))
# plt.show()

range_ks_kc = np.arange(start=15, stop=20.1, step=0.1)
r_list = []

for ratio in range_ks_kc:
    for spring in springs:
        spring.rotational_stiffness = kb/ratio
    eigenvalue, eigenvector = solver.solve(mode_shape=1)
    print("%.4f" % (eigenvalue / euler_load))
