// FILE: CityDb.h
// CLASS PROVIDED: city_db
//     (a custom class for a collection of city records)
//
// void insert (CityRecord):
// precondition: city_db instance cannot contain another CityRecord with the 
// same citycode, and CityRecord.citycode should be in the range [1000,9999].
// postcondition: the specified CityRecord is a new leaf node on the
// binary search tree, and the BST's storage rule is still satisfied.
// in this case, <= is left-node, > is right-node.  Though
// = doesn't need to be checked, really, since the city codes are unique
// by definition of the precondition.
//
// void remove (citycode or x,y)
// precondition: none
// the item in the tree which satisfies the searched criteria is removed,
// and the storage rule of the BST is still satisfied.
// if no item meets the criteria, no item is removed.
//
// 

#ifndef CITY_DB_H
#define CITY_DB_H

// include relevant header files here
#include "CityRecord.h"
#include "BinTree.h"

namespace cs3358Spring2007Assign08
{
   class city_db
   {
   public:
      city_db() :root_ptr(0){};
      void insert(city_record cr);
      void remove(int CityCode);
      void remove(int x, int y);
      bool search(int CityCode);
      bool search(int x, int y);
      bool empty();
      void printTree();
   private:
      binary_tree_node<city_record>* root_ptr;

   };
   void insertRecur(city_record cr,
                           binary_tree_node<city_record>* root_ptr);
   binary_tree_node<city_record>* searchRecur(int CityCode,
                                      binary_tree_node<city_record>* rootPtr);
   binary_tree_node<city_record>* searchRecur(int x, int y,
                                      binary_tree_node<city_record>* rootPtr);

   // NONMEMBER functions for the city_db class
}

#endif
