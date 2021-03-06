# QuadTree #

This is an implementation of a 2D QuadTree.

## Interface ##

The interface of the structure is in the file QuadTree.py with the functions:

   * __insert(self, Point)__ Inserts a given point in the structure.
   * __delete(self, Point)__ Deletes a given point from the structure.
   * __search(self, top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner)__ Returns a List of points included inside the created rectangle.
   * __kNN_query(self, Point, k) Returns a list of the k Nearest Neighbors of given Point.
   
## Project structure ##

 *  __QuadTree.py__ Provides an interface for the structure.
 *  __node.py__ Represents a node in the tree. Implements all the funcionality of the structure.
 *  __point.py__ Represents a 2D point stored in the tree.
 *  __rectangle.py__ Represents a 2D range to query the tree.
