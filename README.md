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
p = -1
n5.y_dof.force = p

# create structure assembly of elements
structure = stx.Structure([e1, e2, e3, e4])

solver = stx.EigenSolver(structure)

eigenvalue, eigenvector = solver.solve(mode_shape=1)

print(f"Critical Buckling Load: {eigenvalue:.3f}")

stx.plot_structure(structure, 1000)

```
Executing this script will open a window displaying the buckling mode and print the associated critical buckling load value.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`stablex` was created by Hazem Kassab. It is licensed under the terms of the MIT license.

## Credits

`stablex` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

## Images
<div style="display: flex; overflow: hidden; width: 100%; max-width: 600px;">
  <div style="display: flex; transition: transform 0.5s ease;">
    <!-- Slide 1 -->
    <div style="min-width: 100%; box-sizing: border-box;">
      <img src="https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Arch.PNG" alt="Slide 1" style="width: 100%; height: auto;">
    </div>
    <!-- Slide 2 -->
    <div style="min-width: 100%; box-sizing: border-box;">
      <img src="https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Fixed_Frame_with_springs.PNG" alt="Slide 2" style="width: 100%; height: auto;">
    </div>
    <!-- Slide 3 -->
    <div style="min-width: 100%; box-sizing: border-box;">
      <img src="https://github.com/Hazem-Kassab/stableX/blob/master/Examples/Images/Fixed_Frame_with_springs.PNG" alt="Slide 3" style="width: 100%; height: auto;">
    </div>
  </div>
</div>