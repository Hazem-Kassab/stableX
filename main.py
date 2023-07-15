from matplotlib import pyplot as plt
import stableX as stx

node_1 = stx.Node(0, 0)
node_2 = stx.Node(0, 1)
node_3 = stx.Node(1, 1)
node_4 = stx.Node(1, 0)

section = stx.Rectangle(.001, .002)


e1 = stx.FrameElement(node_1, node_2, section)
e2 = stx.FrameElement(node_2, node_3, section)
e3 = stx.FrameElement(node_3, node_4, section)

structure = stx.Structure([e1, e2, e3])

stx.graph_structure(structure)
plt.show()



