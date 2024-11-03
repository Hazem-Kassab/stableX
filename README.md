# stablex

A Python library for stability analysis of structures

## Installation

```bash
>> pip install stablex
```

## Usage

```bash
# pinned_column.py

import stablex as stx

# column length
l = 3000

# create nodes at quarter lengths
n1 = stx.Node(0, 0)
n2 = stx.Node(0, 0.25*l)
n3 = stx.Node(0, 0.5*l)
n4 = stx.Node(0, 0.75*l)
n5 = stx.Node(0, l)

# create section
section = stx.Rectangle(100, 100)

# create Frame elements and specify node connectivity and geometric non-linearity (Modulus of elasticity = 200000 MPa by default)
e1 = stx.FrameElement(n1, n2, section, True)
e2 = stx.FrameElement(n2, n3, section, True)
e3 = stx.FrameElement(n3, n4, section, True)
e4 = stx.FrameElement(n4, n5, section, True)

# assign boundary conditions (pinned at base, roller at top)
n1.x_dof.restrained = True
n1.y_dof.restrained = True
n5.x_dof.restrained = True

# assign load
p = -1
n5.y_dof.force = p

# create structure assembly of elements
structure = stx.Structure([e1, e2, e3, e4])

# create an Eigenvalue solver
solver = stx.EigenSolver(structure)

# solve for the required mode shape
eigenvalue, eigenvector = solver.solve(mode_shape=1)

# visualize the buckling mode shape
stx.plot_structure(structure, 1000)
```
#### Executing this script will open a window displaying the buckling mode and print the associated critical buckling load value.
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/pinned_column_1st_mode.png)

```bash
print(f"Critical Buckling Load: {eigenvalue/1000:.3f} N")
```
<pre> Output: Critical Buckling Load: 182.864 kN </pre>

#### Verification with Euler's formula

$$ P_{cr} = \frac{\pi^2 EI}{l^2} = \frac{\pi^2 \times 200 \times 10^3 \times (100)^4/12}{3000^2 \times 1000} = 182.770 kN $$

With an error = 0.05%

#### For the second mode:
```bash
eigenvalue, eigenvector = solver.solve(mode_shape=2)

stx.plot_structure(structure, 1000)
```
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/pinned_column_2nd_mode.png)
```bash
print(f"Critical Buckling Load: {eigenvalue:.3f} N")
```
<pre> Output: Critical Buckling Load: 7365.812 kN </pre>

#### Verification with Euler's formula

$$ P_{cr} = n^2 \frac{\pi^2 EI}{l^2} = 2^2 \frac{\pi^2 \times 200 \times 10^3 \times (100)^4/12}{3000^2 \times 1000} = 7310.818 kN $$

With an error = 0.75%

## Other Examples:
### Rigid Bars with Intermediate Spring
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/rigid_bars_with_springs_sketch.png)
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/rigid_bars_with_springs.png)
<pre> Output: Critical Buckling Load: 666.667 N </pre>
$$ P_{cr} = 2 \frac{k}{l} = 2 \frac{1 \times 10^6}{3000} = 666.667 N $$

With an error = 0.75%

### Trapezoidal Frame
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/trapezoidal_frame.png)

### Triangulated Frame
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/triangulated_frame.png)

### Trussed Column
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/trussed_column.png)

### Arch

1st mode

![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/arch_1st_mode.png)

2nd mode

![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/arch_2nd_mode.png)

### Mult-storey Frame

1st mode

![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/mulit_storey_frame_1st_mode.png)

4th mode

![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/mulit_storey_frame_4th_mode.png)

2nd mode (Braced)

![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/multi_storey_braced_frame_2nd_mode.png)

### Portal Frame
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/portal_frame.png)

### Overhang
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/overhang.png)

### Truss Cantilever
![Alt text](https://github.com/Hazem-Kassab/stableX/blob/master/examples/Images/truss_cantilever.png)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`stablex` was created by Hazem Kassab. It is licensed under the terms of the MIT license.

## Credits

`stablex` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

