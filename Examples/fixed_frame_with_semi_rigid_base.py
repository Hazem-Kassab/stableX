# frame_with_springs
import math
import pandas as pd

import numpy as np

import stableX as stx

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

section = stx.Rectangle(100, 100)


e1 = stx.FrameElement(node_11, node_2, section, include_geom_nonlinearity=True)
e2 = stx.FrameElement(node_2, node_3, section, include_geom_nonlinearity=True)
e3 = stx.FrameElement(node_3, node_4, section)
e4 = stx.FrameElement(node_4, node_5, section, include_geom_nonlinearity=True)
e5 = stx.FrameElement(node_5, node_66, section, include_geom_nonlinearity=True)

kc = e1.elasticity_modulus * section.inertia / 6000
ks = 0

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

# solver = stx.NonlinearSolver(structure)
# solver.solve_incrementally(300, node_3.y_dof, node_3.x_dof)
#
#
# stx.plot_structure(structure, 10)
#
# stx.plot(solver.displacement, solver.load, "displacement (mm)", "load P (N)")

ratios_2 = np.arange(0.01, 20, 0.1)
results = []

solver = stx.EigenSolver(structure)
eigenvalue, eigenvector = solver.solve(mode_shape=1)
print("%.2f" % (eigenvalue/1000))
stx.plot_structure(structure, 1000)


# pe = math.pi ** 2 * e1.elasticity_modulus * section.inertia / 6000 ** 2
# print(0.74766*pe)
# for ratio in ratios_2:
#     s1.rotational_stiffness = 1/ratio * kc
#     s2.rotational_stiffness = 1/ratio * kc
#     eigenvalue, eigenvector = solver.solve(mode_shape=1)
#     p_pe = eigenvalue.real/pe
#     results.append(p_pe)
#
# df = pd.DataFrame(results)
# df.to_excel("fixed_frame_with_semi_rigid_base.xlsx", index=False)

# stx.plot(ratios_2, results, "Kc/Ks","P/Pe")
#
# stx.plot_structure(structure, 1000)