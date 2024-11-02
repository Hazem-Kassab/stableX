import stablex as stx

node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, 3000)
node_2_dummy = stx.Node(0, 3000)
node_3 = stx.Node(0, 6000)

# coupling
node_2_dummy.x_dof = node_2.x_dof
node_2_dummy.y_dof = node_2.y_dof

section = stx.Rectangle(1000, 1000)

rigid_bar_1 = stx.FrameElement(node_1, node_2_dummy, section, True)
rigid_bar_2 = stx.FrameElement(node_2, node_3, section, True)

spring = stx.LinearRotationalSpringElement(node_2, node_2_dummy, 1e6)

structure = stx.Structure([rigid_bar_1, rigid_bar_2, spring])

node_1.x_dof.restrained = True
node_1.y_dof.restrained = True
node_3.x_dof.restrained = True

node_3.y_dof.force = -1

solver = stx.EigenSolver(structure)
eigenvalue, eigenvector = solver.solve(mode_shape=1)
print(eigenvalue)
stx.plot_structure(structure, -1000)

print(2*spring.rotational_stiffness / 3000)
