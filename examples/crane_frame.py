import math

import stablex as stx

L = 10000
b = 0.8
a = 0.01
N = 80

W = (1-b)*L


n1 = stx.Node(0, 0)
n1a = stx.Node(0, 0.25 * b * L)
n1b = stx.Node(0, 0.5 * b * L)
n1c = stx.Node(0, 0.75 * b * L)
n2 = stx.Node(0, b * L)
n2a = stx.Node(0, 0.5 * (1-b) * L + b*L)
n3 = stx.Node(0, L)

n4 = stx.Node(W, 0)
n4a = stx.Node(W, 0.25 * b * L)
n4b = stx.Node(W, 0.5 * b * L)
n4c = stx.Node(W, 0.75 * b * L)
n5 = stx.Node(W, b * L)
n5a = stx.Node(W, 0.5 * (1-b) * L + b*L)
n6 = stx.Node(W, L)

section_2 = stx.Rectangle(100, 200)
section_1 = stx.Rectangle(section_2.width * N, section_2.height)

c1a = stx.FrameElement(n1, n1a, section_1, True)
c1b = stx.FrameElement(n1a, n1b, section_1, True)
c1c = stx.FrameElement(n1b, n1c, section_1, True)
c1d = stx.FrameElement(n1c, n2, section_1, True)
c2a = stx.FrameElement(n2, n2a, section_2, True)
c2b = stx.FrameElement(n2a, n3, section_2, True)

c3a = stx.FrameElement(n4, n4a, section_1, True)
c3b = stx.FrameElement(n4a, n4b, section_1, True)
c3c = stx.FrameElement(n4b, n4c, section_1, True)
c3d = stx.FrameElement(n4c, n5, section_1, True)
c4a = stx.FrameElement(n5, n5a, section_2, True)
c4b = stx.FrameElement(n5a, n6, section_2, True)

b1 = stx.FrameElement(n3, n6, section_2)

n1.x_dof.restrained = True
n1.y_dof.restrained = True
n1.rz_dof.restrained = True

n4.x_dof.restrained = True
n4.y_dof.restrained = True
n4.rz_dof.restrained = True

n3.y_dof.force = -1
n2.y_dof.force = n3.y_dof.force * (1-a)/a

n6.y_dof.force = -1
n5.y_dof.force = n6.y_dof.force * (1-a)/a

structure = stx.Structure([c1a, c1b, c1c, c1d, c2a, c2b, c3a, c3b, c3c, c3d, c4a, c4b, b1])

solver = stx.EigenSolver(structure)
eigenvalue, eigenvectors = solver.solve(1)
total_critical_load = eigenvalue/a
euler_load = math.pi**2 * c1a.elasticity_modulus * c1a.section.inertia / L**2
total_critical_load_ratio = total_critical_load/euler_load
print(total_critical_load_ratio)
stx.plot_structure(structure, 1000)
