import math

import stableX as stx

radius = 6000
height = 4000
number_of_segments = 16

theta = 2*math.acos((radius-height)/radius)
delta_theta = theta/number_of_segments
beta = (math.pi - theta)/2

nodes = []
elements = []

section = stx.Rectangle(100, 100)


for n in range(number_of_segments+1):
    alpha = beta + n * delta_theta
    x = radius * math.cos(alpha)
    y = radius * math.sin(alpha)
    nodes.append(stx.Node(x, y))

i = 0
while i < number_of_segments:
    elements.append(stx.FrameElement(nodes[i], nodes[i+1], section, True))
    i += 1

arch = stx.Structure(elements)

# assign boundary conditios
nodes[0].y_dof.restrained = True
nodes[0].x_dof.restrained = True
nodes[0].rz_dof.restrained = True
nodes[-1].y_dof.restrained = True
nodes[-1].x_dof.restrained = True
nodes[-1].rz_dof.restrained = True

# assign force
middle_node_index = int(number_of_segments/2)
nodes[middle_node_index].y_dof.force = -5.8e5


solver = stx.NonlinearSolver(arch)
solver.solve_incrementally(100, nodes[middle_node_index].y_dof,
                           nodes[middle_node_index].y_dof)

stx.plot_structure(arch, 1)

stx.plot(solver.displacement, solver.load)
