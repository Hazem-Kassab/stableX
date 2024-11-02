# truss_cantilever.py

import stablex as stx


n1 = stx.Node(0, 0)
n1a = stx.Node(1000, 0)
n2 = stx.Node(2000, 0)
n2a = stx.Node(3000, 0)
n3 = stx.Node(4000, 0)
n3a = stx.Node(5000, 0)
n4 = stx.Node(6000, 0)


n5 = stx.Node(0, 2000)
n6 = stx.Node(2000, 1800)
n7 = stx.Node(4000, 1600)
n8 = stx.Node(6000, 1400)

section = stx.Rectangle(100, 100)

e1 = stx.FrameElement(n1, n1a, section, True)
e1a = stx.FrameElement(n1a, n2, section, True)
e2 = stx.FrameElement(n2, n2a, section, True)
e2a = stx.FrameElement(n2a, n3, section, True)
e3 = stx.FrameElement(n3, n3a, section, True)
e3a = stx.FrameElement(n3a, n4, section, True)

e4 = stx.FrameElement(n5, n6, section)
e5 = stx.FrameElement(n6, n7, section)
e6 = stx.FrameElement(n7, n8, section)

e7 = stx.TrussElement(n5, n2, section)
e8 = stx.TrussElement(n6, n3, section)
e9 = stx.TrussElement(n7, n4, section)

e10 = stx.TrussElement(n6, n2, section, include_geom_nonlinearity=True)
e11 = stx.TrussElement(n7, n3, section, include_geom_nonlinearity=True)
e12 = stx.TrussElement(n8, n4, section, include_geom_nonlinearity=True)


structure = stx.Structure([e1, e1a, e2, e2a, e3, e3a, e4, e5, e6, e7, e8, e9, e10, e11, e12])

n1.x_dof.restrained = True
n1.y_dof.restrained = True

n5.x_dof.restrained = True
n5.y_dof.restrained = True

n8.y_dof.force = -1

solver = stx.EigenSolver(structure)

eigenvalue, eigenvector = solver.solve(mode_shape=1)

stx.plot_structure(structure, 1000)
