from abc import ABC

import numpy as np

from stablex.elements.element import Element


class SpringElement(Element, ABC):
    """
    Abstract base class for spring elements, representing a structural spring
    in the framework.

    This class provides the structure for implementing spring-specific behavior
    within the analysis but does not currently define `first_order_elastic_stiffness_matrix`
    or `transformation_matrix`, which must be implemented in subclasses.

    Methods
    -------
    first_order_elastic_stiffness_matrix()
        Abstract method to compute the elastic stiffness matrix of the spring element.

    transformation_matrix()
        Abstract method to define the transformation matrix for the spring element.
    """

    def first_order_elastic_stiffness_matrix(self) -> np.ndarray:
        """
                Computes the elastic stiffness matrix for the spring element.

        This abstract method should be implemented by subclasses to provide
        spring-specific stiffness characteristics.

        Returns
        -------
        np.ndarray
            The elastic stiffness matrix of the spring element.
        """
        raise NotImplementedError

    def transformation_matrix(self) -> np.ndarray:
        """
        Defines the transformation matrix for the spring element.

        This abstract method should be implemented by subclasses to transform
        the spring element based on its orientation and configuration.

        Returns
        -------
        np.ndarray
            The transformation matrix for the spring element.
        """
        raise NotImplementedError
