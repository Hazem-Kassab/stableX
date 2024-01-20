# frame_with_springs
import math

import stableX as stx

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

# spring nodes
node_66 = stx.Node(0, 6000)
node_122 = stx.Node(6000, 6000)

# coupling
node_66.x_dof = node_6.x_dof
node_66.y_dof = node_6.y_dof

node_122.x_dof = node_12.x_dof
node_122.y_dof = node_12.y_dof

width = 100
kb_kc = 5

# section
section = stx.Rectangle(width, 100)
section_2 = stx.Rectangle(kb_kc*100, 100)

# left column elements
c1 = stx.FrameElement(node_1, node_2, section, True)
c2 = stx.FrameElement(node_2, node_3, section, True)
c3 = stx.FrameElement(node_3, node_4, section, True)
c4 = stx.FrameElement(node_4, node_5, section, True)
c5 = stx.FrameElement(node_5, node_6, section, True)

# right column elements
c6 = stx.FrameElement(node_7, node_8, section, True)
c7 = stx.FrameElement(node_8, node_9, section, True)
c8 = stx.FrameElement(node_9, node_10, section, True)
c9 = stx.FrameElement(node_10, node_11, section, True)
c10 = stx.FrameElement(node_11, node_12, section, True)

# beam elements
b1 = stx.FrameElement(node_66, node_122, section_2)


kb = b1.elasticity_modulus * section_2.inertia / 6000
a = 2
ks = kb/a

# spring elements
s1 = stx.LinearRotationalSpringElement(node_6, node_66, ks)
s2 = stx.LinearRotationalSpringElement(node_12, node_122, ks)

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

structure = stx.Structure([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, b1, s1, s2])

# solver = stx.NonlinearSolver(structure)
# solver.solve_incrementally(300, node_3.y_dof, node_3.x_dof)
#
#
# stx.plot_structure(structure, 10)
#
# stx.plot(solver.displacement, solver.load, "displacement (mm)", "load P (N)")

# kc = c1.elasticity_modulus * section.inertia / 6000
# ratios = [0.25, 0.5, 1, 2, 4, 10]
# print(math.pi**2 * section.inertia * c1.elasticity_modulus/6000**2)
# for i in ratios:
#     print(f"********kb/kc = {i}")
#     section_2.width = i * section.width
#     kb = b1.elasticity_modulus * section_2.inertia / 6000
#     print(kb/kc)
#     for j in ratios:
#         solver = stx.EigenSolver(structure)
#         print(f"kb/ks = {j}")
#         s1.rotational_stiffness = kb/j
#         eigenvalue, eigenvector = solver.solve(mode_shape=1)
#         print("%.3f KN" % (eigenvalue/1000))


euler_load = math.pi**2 * c1.elasticity_modulus * section.inertia / 6000**2
solver = stx.EigenSolver(structure)
eigenvalue, eigenvector = solver.solve(mode_shape=2)
print("%.3f" % (eigenvalue/euler_load))

stx.plot_structure(structure, 1000)


