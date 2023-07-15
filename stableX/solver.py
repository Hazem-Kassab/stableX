import numpy as np

from stableX.structure import Structure


def _assemble_stiffness_matrix(structure: Structure, load):
    dofs_count = (len(structure.degrees_of_freedom))
    global_matrix = np.zeros((dofs_count, dofs_count))
    for element in structure.elements:
        i = 0
        for dof_i in element.dofs:
            j = 0
            for dof_j in element.dofs:
                if dof_i.restrained and dof_j.restrained:
                    stiffness_term = element.stability_stiffness_matrix(load)[i, j]
                    global_matrix[dof_i.id - 1, dof_j.id - 1] += stiffness_term
