
  
# stableX    
 A Python library for stability analysis of structures  
    
## Usage    
```python 
# pinned_column.py

import stableX as stx

# column length
l = 3000

# create nodes at quarter lengths
n1 = stx.Node(0, 0)
n2 = stx.Node(0, 0.25*l)
n3 = stx.Node(10, 0.5*l)  # introduce imperfection of 10 mm
n4 = stx.Node(0, 0.75*l)
n5 = stx.Node(0, l)

# create section
section = stx.Rectangle(100, 100)

# create Frame elements and specify node connectivity and geometric non-linearity
e1 = stx.FrameElement(n1, n2, section, True)
e2 = stx.FrameElement(n2, n3, section, True)
e3 = stx.FrameElement(n3, n4, section, True)
e4 = stx.FrameElement(n4, n5, section, True)

# assign boundary conditions (pinned at base, roller at top)
n1.x_dof.restrained = True
n1.y_dof.restrained = True
n5.x_dof.restrained = True

# assign load
p = -1.813e6
n5.y_dof.force = p

# create structure assembly of elements
structure = stx.Structure([e1, e2, e3, e4])

# create a nonlinear solver object
solver = stx.NonlinearSolver(structure)

# solve in 100 load steps and record load at top and mid-span lateral displacement
solver.solve_incrementally(100, n5.y_dof, n3.x_dof)

# plot structure and deformation (buckled shape)
stx.plot_structure(structure, 1)

# plot recorded load-displacement curve
stx.plot(solver.displacement, solver.load, "displacement (mm)", "load P (N)")


``` 
## Output    
**Deformed (Buckled) Shape**![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Pinned_Pinned_Column.PNG?raw=true)

**Load-Displacement Plot**![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Pinned_Pinned_Column_Plot.PNG?raw=true)  

**Verification with Euler Critical Load**    
$$E=200\times10^3\space MPa$$ $$I=\frac{100^4}{12}= 8.33\times10^6\space mm^4$$  $$l=3000\space mm$$  $$P_E=\frac{\pi^2 E I}{l^2}=\frac{\pi^2 (200\times10^3) (8.33\times10^6)}{3000^2}=1.827\times10^6\space N$$  
    
    
## Other Buckling of Structures Examples  
**Fixed Frame with Semi-rigid joints (Rotational Springs) Under Axial Load**  
![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Fixed_Frame_with_springs.PNG?raw=true)  
  
**Multi-storey Frame with Chevron Bracing Under Lateral Load**  
![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Frame_with_chevron_bracing.PNG?raw=true)  
  
**Multi-storey Frame with X-Bracing Under Axial Load**  
![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/X-Braced_Frame.png?raw=true)  
  
**Multi-storey Fixed Frame Permitted to Sway Under Axial Load**  
![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Mulit-storey_Fixed_Frame_Unbraced.png?raw=true)  
  
**Cantilever Truss Under Tip Vertical Load**  
![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Cantilever%20Truss.PNG?raw=true)  
  
**Arch Frame Under Mid-Point Vertical Load**  
![alt_text](https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Arch.PNG?raw=true)