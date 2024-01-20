# frame_with_springs

import stableX as stx

node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, 3000)
node_3 = stx.Node(0, 6000)
node_4 = stx.Node(6000, 6000)
node_5 = stx.Node(6000, 3000)
node_6 = stx.Node(6000, 0)


section = stx.Rectangle(100, 100)


e1 = stx.FrameElement(node_1, node_2, section, include_geom_nonlinearity=True)
e2 = stx.FrameElement(node_2, node_3, section, include_geom_nonlinearity=True)
e3 = stx.FrameElement(node_3, node_4, section)
e4 = stx.FrameElement(node_4, node_5, section, include_geom_nonlinearity=True)
e5 = stx.FrameElement(node_5, node_6, section, include_geom_nonlinearity=True)


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

structure = stx.Structure([e1, e2, e3, e4, e5])

# solver = stx.NonlinearSolver(structure)
# solver.solve_incrementally(300, node_3.y_dof, node_3.x_dof)
#
#
# stx.plot_structure(structure, 10)
#
# stx.plot(solver.displacement, solver.load, "displacement (mm)", "load P (N)")

solver = stx.EigenSolver(structure)

solver.solve(mode_shape=2)

stx.plot_structure(structure, 1000)
