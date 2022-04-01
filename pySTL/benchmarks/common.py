##
#
# Common helper functions for defining STL specifications.
#
##

import numpy as np
from pySTL.STL import STLTree, STLPredicate
from matplotlib.patches import Rectangle

def inside_rectangle_formula(bounds, y1_index, y2_index, d, name=None):
    """
    Create an STL formula representing being inside a
    rectangle with the given bounds:

    ::

       y2_max   +-------------------+
                |                   |
                |                   |
                |                   |
       y2_min   +-------------------+
                y1_min              y1_max

    :param bounds:      Tuple ``(y1_min, y1_max, y2_min, y2_max)`` containing
                        the bounds of the rectangle. 
    :param y1_index:    index of the first (``y1``) dimension
    :param y2_index:    index of the second (``y2``) dimension
    :param d:           dimension of the overall signal
    :param name:        (optional) string describing this formula

    :return inside_rectangle:   An ``STLFormula`` specifying being inside the
                                rectangle at time zero.
    """
    assert y1_index < d , "index must be less than signal dimension"
    assert y2_index < d , "index must be less than signal dimension"

    # Unpack the bounds
    y1_min, y1_max, y2_min, y2_max = bounds

    # Create predicates a*y >= b for each side of the rectangle
    a1 = np.zeros((1,d)); a1[:,y1_index] = 1
    right = STLPredicate(a1, y1_min)
    left = STLPredicate(-a1, -y1_max)

    a2 = np.zeros((1,d)); a2[:,y2_index] = 1
    top = STLPredicate(a2, y2_min)
    bottom = STLPredicate(-a2, -y2_max)

    # Take the conjuction across all the sides
    inside_rectangle = right & left & top & bottom

    # set the names
    if name is not None:
        right.name = "right of " + name
        left.name = "left of " + name
        top.name = "top of " + name
        bottom.name = "bottom of " + name
        inside_rectangle.name = name

    return inside_rectangle

def outside_rectangle_formula(bounds, y1_index, y2_index, d, name=None):
    """
    Create an STL formula representing being outside a
    rectangle with the given bounds:

    ::

       y2_max   +-------------------+
                |                   |
                |                   |
                |                   |
       y2_min   +-------------------+
                y1_min              y1_max

    :param bounds:      Tuple ``(y1_min, y1_max, y2_min, y2_max)`` containing
                        the bounds of the rectangle. 
    :param y1_index:    index of the first (``y1``) dimension
    :param y2_index:    index of the second (``y2``) dimension
    :param d:           dimension of the overall signal
    :param name:        (optional) string describing this formula
    
    :return outside_rectangle:   An ``STLFormula`` specifying being outside the
                                 rectangle at time zero.
    """
    assert y1_index < d , "index must be less than signal dimension"
    assert y2_index < d , "index must be less than signal dimension"

    # Unpack the bounds
    y1_min, y1_max, y2_min, y2_max = bounds

    # Create predicates a*y >= b for each side of the rectangle
    a1 = np.zeros((1,d)); a1[:,y1_index] = 1
    right = STLPredicate(a1, y1_max)
    left = STLPredicate(-a1, -y1_min)

    a2 = np.zeros((1,d)); a2[:,y2_index] = 1
    top = STLPredicate(a2, y2_max)
    bottom = STLPredicate(-a2, -y2_min)

    # Take the disjuction across all the sides
    outside_rectangle = right | left | top | bottom

    # set the names
    if name is not None:
        right.name = "right of " + name
        left.name = "left of " + name
        top.name = "top of " + name
        bottom.name = "bottom of " + name
        outside_rectangle.name = name

    return outside_rectangle

def make_rectangle_patch(xmin, xmax, ymin, ymax, **kwargs):
    """
    Convienience function for making a ``matplotlib.patches.Rectangle`` 
    patch for visualizing a rectangle:

    ::

       ymax   +-------------------+
              |                   |
              |                   |
              |                   |
       ymin   +-------------------+
              xmin                xmax

    :param xmin:        horizontal lower bound of the rectangle.
    :param xmax:        horizontal upper bound of the rectangle.
    :param ymin:        vertical lower bound of the rectangle.
    :param ymax:        vertical upper bound of the rectangle.
    :param kwargs:    (optional) keyword arguments passed to
                        the Rectangle constructor.

    :return patch:  a ``matplotlib.pathces.Rectangle`` patch.

    """
    x = xmin
    y = ymin
    width = xmax-x
    height = ymax-y

    return Rectangle((x,y), width, height, **kwargs)
