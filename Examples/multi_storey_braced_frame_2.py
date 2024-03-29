# multi_storey_braced_frame_2.py

import stableX as stx

w = 6000
h = 6000

n1 = stx.Node(0, 0)
n1a = stx.Node(0, 0.5*h)
n2 = stx.Node(0, h)
n2a = stx.Node(0, 1.5*h)
n3 = stx.Node(0, 2*h)
n3a = stx.Node(0, 2.5*h)
n4 = stx.Node(0, 3*h)

n5 = stx.Node(w, 0)
n5a = stx.Node(w, 0.5*h)
n6 = stx.Node(w, h)
n6a = stx.Node(w, 1.5*h)
n7 = stx.Node(w, 2*h)
n7a = stx.Node(w, 2.5*h)
n8 = stx.Node(w, 3*h)

section = stx.Rectangle(100, 100)

c1 = stx.FrameElement(n1, n1a, section, True)
c2 = stx.FrameElement(n1a, n2, section, True)
c3 = stx.FrameElement(n2, n2a, section, True)
c4 = stx.FrameElement(n2a, n3, section, True)
c5 = stx.FrameElement(n3, n3a, section, True)
c6 = stx.FrameElement(n3a, n4, section, True)


c7 = stx.FrameElement(n5, n5a, section, True)
c8 = stx.FrameElement(n5a, n6, section, True)
c9 = stx.FrameElement(n6, n6a, section, True)
c10 = stx.FrameElement(n6a, n7, section, True)
c11 = stx.FrameElement(n7, n7a, section, True)
c12 = stx.FrameElement(n7a, n8, section, True)


b1 = stx.FrameElement(n2, n6, section)
b2 = stx.FrameElement(n3, n7, section)
b3 = stx.FrameElement(n4, n8, section)

t1 = stx.TrussElement(n1, n6, section, True)
t2 = stx.TrussElement(n5, n2, section, True)
t3 = stx.TrussElement(n2, n7, section, True)
t4 = stx.TrussElement(n6, n3, section, True)
t5 = stx.TrussElement(n3, n8, section, True)
t6 = stx.TrussElement(n7, n4, section, True)

braced_frame = stx.Structure([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c6, b1, b2, b3, t1, t2, t3, t4, t5, t6])


# assign boundary conditions
n1.x_dof.restrained = True
n1.y_dof.restrained = True

n5.x_dof.restrained = True
n5.y_dof.restrained = True


# assign load
P = -7.29e5
n4.y_dof.force = P
n4.x_dof.force = 1000
n8.y_dof.force = P

# solve
solver = stx.NonlinearSolver(braced_frame)
solver.solve_incrementally(300, n4.y_dof, n3a.x_dof)

# plot results
stx.plot_structure(braced_frame, 50)

stx.plot(solver.displacement, solver.load, "displacement (mm)", "load P (N)")
