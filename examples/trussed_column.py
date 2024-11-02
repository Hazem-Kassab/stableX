import stablex as stx

bottom_node = stx.Node(0, 0)

nodes = []

h = 10000
w = 1000

n = h / w  # should be integer

for i in range(int(n)-1):
    node_l = stx.Node(-w/2, w*(i+1))
    node_r = stx.Node(w/2, w*(i+1))
    nodes.extend([node_l, node_r])

top_node = stx.Node(0, h)

section = stx.Rectangle(100, 100)

elements = []

i = 0

while i <= n+4:
    horizontal = stx.TrussElement(nodes[i], nodes[i+1], section, True)
    diagonal = stx.TrussElement(nodes[i], nodes[i+3], section, True)
    vertical_l = stx.TrussElement(nodes[i], nodes[i+2], section, True)
    vertical_r = stx.TrussElement(nodes[i+1], nodes[i+3], section, True)
    elements.extend([horizontal, diagonal, vertical_l, vertical_r])
    i += 2

last_horizontal = stx.TrussElement(nodes[-2], nodes[-1], section, True)
top_diagonal_l =stx.TrussElement(nodes[-2], top_node, section, True)
top_diagonal_r =stx.TrussElement(nodes[-1], top_node, section, True)
bottom_diagonal_l =stx.TrussElement(bottom_node, nodes[0], section, True)
bottom_diagonal_r =stx.TrussElement(bottom_node, nodes[1], section, True)

elements.extend([last_horizontal, top_diagonal_l, top_diagonal_r, bottom_diagonal_l, bottom_diagonal_r])

structure = stx.Structure(elements)

# assign boundary conditions
bottom_node.x_dof.restrained = True
bottom_node.y_dof.restrained = True
top_node.x_dof.restrained = True

# assign loading
top_node.y_dof.force = -1

s = stx.Solver(structure)
s.solve_first_order_elastic()

# solve
solver = stx.EigenSolver(structure)
eigenvalue, eigenvector = solver.solve(mode_shape=2)
stx.plot_structure(structure, scale=2000)
