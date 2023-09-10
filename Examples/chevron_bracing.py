# chevron_bracing.py

import stableX as stx

w = 6000
h = 5000

# create nodes
n1 = stx.Node(0, 0)
n2 = stx.Node(0, h)
n3 = stx.Node(0, 2*h)
n4 = stx.Node(0, 3*h)

n5 = stx.Node(w, 0)
n6 = stx.Node(w, h)
n7 = stx.Node(w, 2*h)
n8 = stx.Node(w, 3*h)

n9 = stx.Node(w/2, h)
n10 = stx.Node(w/2, 2*h)
n11 = stx.Node(w/2, 3*h)

n12 = stx.Node(w/4, h/2)
n13 = stx.Node(w/4, 1.5*h)
n14 = stx.Node(w/4, 2.5*h)

n15 = stx.Node(3*w/4+10, h/2)
n16 = stx.Node(3*w/4+10, 1.5*h)
n17 = stx.Node(3*w/4+10, 2.5*h)

# create dummy nodes for strut releases
n2ds = stx.Node(n2.x, n2.y)
n3ds = stx.Node(n3.x, n3.y)
n4ds = stx.Node(n4.x, n4.y)
n6ds = stx.Node(n6.x, n6.y)
n7ds = stx.Node(n7.x, n7.y)
n8ds = stx.Node(n8.x, n8.y)

# couple dofs for dummy nodes
n2ds.x_dof = n2.x_dof
n2ds.y_dof = n2.y_dof
n3ds.x_dof = n3.x_dof
n3ds.y_dof = n3.y_dof
n4ds.x_dof = n4.x_dof
n4ds.y_dof = n4.y_dof
n6ds.x_dof = n6.x_dof
n6ds.y_dof = n6.y_dof
n7ds.x_dof = n7.x_dof
n7ds.y_dof = n7.y_dof
n8ds.x_dof = n8.x_dof
n8ds.y_dof = n8.y_dof

# create dummy nodes for bracing releases
n1db = stx.Node(n1.x, n1.y)
n2db = stx.Node(n2.x, n2.y)
n3db = stx.Node(n3.x, n3.y)
n4db = stx.Node(n4.x, n4.y)
n5db = stx.Node(n5.x, n5.y)
n6db = stx.Node(n6.x, n6.y)
n7db = stx.Node(n7.x, n7.y)
n8db = stx.Node(n8.x, n8.y)
n9dbr = stx.Node(n9.x, n9.y)
n10dbr = stx.Node(n10.x, n10.y)
n11dbr = stx.Node(n11.x, n11.y)

n9dbl = stx.Node(n9.x, n9.y)
n10dbl = stx.Node(n10.x, n10.y)
n11dbl = stx.Node(n11.x, n11.y)

# couple dofs for dummy nodes
n1db.x_dof = n1.x_dof
n1db.y_dof = n1.y_dof
n2db.x_dof = n2.x_dof
n2db.y_dof = n2.y_dof
n3db.x_dof = n3.x_dof
n3db.y_dof = n3.y_dof
n4db.x_dof = n4.x_dof
n4db.y_dof = n4.y_dof
n5db.x_dof = n5.x_dof
n5db.y_dof = n5.y_dof
n6db.x_dof = n6.x_dof
n6db.y_dof = n6.y_dof
n7db.x_dof = n7.x_dof
n7db.y_dof = n7.y_dof
n8db.x_dof = n8.x_dof
n8db.y_dof = n8.y_dof
n9dbr.x_dof = n9.x_dof
n9dbr.y_dof = n9.y_dof
n10dbr.x_dof = n10.x_dof
n10dbr.y_dof = n10.y_dof
n11dbr.x_dof = n11.x_dof
n11dbr.y_dof = n11.y_dof

n9dbl.x_dof = n9.x_dof
n9dbl.y_dof = n9.y_dof
n10dbl.x_dof = n10.x_dof
n10dbl.y_dof = n10.y_dof
n11dbl.x_dof = n11.x_dof
n11dbl.y_dof = n11.y_dof

# create section profile
section = stx.Rectangle(100, 100)

# create columns
c1 = stx.FrameElement(n1, n2, section)
c2 = stx.FrameElement(n2, n3, section)
c3 = stx.FrameElement(n3, n4, section)
c4 = stx.FrameElement(n5, n6, section)
c5 = stx.FrameElement(n6, n7, section)
c6 = stx.FrameElement(n7, n8, section)

# create struts
s1 = stx.FrameElement(n2ds, n9, section)
s2 = stx.FrameElement(n9, n6ds, section)
s3 = stx.FrameElement(n3ds, n10, section)
s4 = stx.FrameElement(n10, n7ds, section)
s5 = stx.FrameElement(n4ds, n11, section)
s6 = stx.FrameElement(n11, n8ds, section)

# create bracing
b1 = stx.FrameElement(n1db, n12, section)
b2 = stx.FrameElement(n12, n9dbr, section)
b3 = stx.FrameElement(n5db, n15, section, True)
b4 = stx.FrameElement(n15, n9dbl, section, True)

b5 = stx.FrameElement(n2db, n13, section)
b6 = stx.FrameElement(n13, n10dbr, section)
b7 = stx.FrameElement(n6db, n16, section, True)
b8 = stx.FrameElement(n16, n10dbl, section, True)

b9 = stx.FrameElement(n3db, n14, section)
b10 = stx.FrameElement(n14, n11dbr, section)
b11 = stx.FrameElement(n7db, n17, section, True)
b12 = stx.FrameElement(n17, n11dbl, section, True)

# assemble structure
structure = stx.Structure([c1, c2, c3, c4, c5, c6,
                           s1, s2, s3, s4, s5, s6,
                           b1, b2, b3, b4, b5, b6,
                           b7, b8, b9, b10, b11, b12])

# assign boundary conditions
n1.x_dof.restrained = True
n1.y_dof.restrained = True
n5.x_dof.restrained = True
n5.y_dof.restrained = True

# assign load
n4.x_dof.force = 4.88e5

# solve
solver = stx.NonlinearSolver(structure)
solver.solve_incrementally(100, n4.x_dof, n4.x_dof)


stx.plot_structure(structure, 5)
stx.plot(solver.displacement, solver.load, "displacement (mm)", "load P (N)")
