from matplotlib import pyplot as plt
import stableX as stx

node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, 6000)
node_3 = stx.Node(6000, 6000)
node_4 = stx.Node(6000, 0)

section = stx.Rectangle(100, 500)


e1 = stx.FrameElement(node_1, node_2, section)
e2 = stx.FrameElement(node_2, node_3, section)
e3 = stx.FrameElement(node_3, node_4, section)

node_1.x_dof.restrained = True
node_1.y_dof.restrained = True

node_4.x_dof.restrained = True
node_4.y_dof.restrained = True

node_2.x_dof.force = 5000000

structure = stx.Structure([e1, e2, e3])
solver = stx.Solver(structure)
solver.solve_first_order_elastic()
print(node_2.x_dof.displacement)

stx.plot_structure(structure, 1)
plt.show()

