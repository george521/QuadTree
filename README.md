# QuadTree #

This is an implementation of a 2D QuadTree.

## Interface ##

The interface of the structure is in the file QuadTree.py with the functions:

   * __insert(self, Point)__ Inserts a given point in the structure.
   * __delete(self, Point)__ Deletes a given point from the structure.
   * __query(self, top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner)__ Returns a List of points included inside the created rectangle.

## Project structure ##

 *  QuadTree.py Provides an interface for the structure.
 *  node.py Represents a node in the tree. Implements all the funcionality of the structure.
 *  point.py Represents a 2D point stored in the tree.
 *  rectangle.py Represents a 2D range to query the tree.
