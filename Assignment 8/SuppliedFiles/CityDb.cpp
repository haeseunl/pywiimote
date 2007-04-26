// FILE: CityDb.cpp
// CLASS IMPLEMENTED: city_db (see CityDb.h for documentation)
// INVARIANT of the ADT:
// ????
//
// Documentation for functions client don't have to know:
//
// void bst_remove_max(binary_tree_node<city_record>*& root_ptr,
//                     city_record& removed)
//   Precondition: root_ptr is a root pointer of a non-empty
//   binary search tree.
//   Postcondition: The city record with the largest city code
//   in the binary search tree has been removed, and root_ptr
//   now points to the root of the new (smaller) binary search
//   tree. The reference parameter, removed, has been set to a
//   copy of the removed city record.
//
// void bst_remove(binary_tree_node<city_record>*& root_ptr,
//                 const city_record& target)
//   Precondition: root_ptr is a root pointer of a binary search
//   tree (or may be 0 for the empty tree)
//   Postcondition: If target was in the tree, then one copy of
//   target has been removed, and root_ptr now points to the
//   root of the new (smaller) binary search tree. Otherwise,
//   if target was not in the tree, then the tree is unchanged.
//
// ...
//

// include relevant header files here
#include "CityDb.h"
#include "BinTree.h"
#include "CityRecord.h"
#include <iostream>

namespace cs3358Spring2007Assign08
{
   
   // NONMEMBER FUNCTIONS
   
   void bst_remove(binary_tree_node<city_record>*& root_ptr,
                 const city_record& target)
   {
      if (root_ptr->data() == target)
         delete bst_remove_max(root_ptr);// get rid of city code.
         return;
      bst_remove(root_ptr->left())
      bst_remove(root_ptr->right())
   }
   
   void bst_remove_max(binary_tree_node<city_record>*& root_ptr,
                     city_record& removed)
   {
      // we traverse the root_ptr -> left, taking all rights until we find the
      // largest value.
      if (root_ptr->left() != 0)
         binary_tree_node<city_record>* biggest = root_ptr->left();
         
         if (biggest->right() == 0) // nothing to the right of our node.
            biggest->set_left(root_ptr->left());
            biggest->set_right(root_ptr->right());
         while ( biggest->right() != 0)
            biggest = biggest -> right();
         
         removed = root_ptr->data();
         biggest->right()->set_left(root_ptr->left());
         biggest->right()->set_right(root_ptr->right());
         root_ptr = biggest->right();
         biggest->set_right(0);
         
            
      
      
      
      
   binary_tree_node<city_record>* searchRecur(int CityCode,
                                      binary_tree_node<city_record>* rootPtr)
   {
      if (rootPtr == 0) return 0;
      if (rootPtr->data().get_code() == CityCode)
         return rootPtr;
      binary_tree_node<city_record>* temp = searchRecur(CityCode,
                                                        rootPtr->left());
      if (temp != 0)
         return temp;
      temp = searchRecur(CityCode, rootPtr->right());
      if (temp != 0)
         return temp;
      return 0;
   }
   
   binary_tree_node<city_record>* searchRecur(int x, int y,
                                      binary_tree_node<city_record>* rootPtr)
   {
      if (rootPtr == 0) return 0;
      if (rootPtr->data().get_x() == x && rootPtr->data().get_y() == y)
         return rootPtr;
      binary_tree_node<city_record>* temp = searchRecur(x,y,
                                                        rootPtr->left());
      if (temp != 0)
         return temp;
      temp = searchRecur(x,y, rootPtr->right());
      if (temp != 0)
         return temp;
      return 0;
   }
   
   void insertRecur(city_record cr,
                                 binary_tree_node<city_record>* rootPtr)
   {
     assert(rootPtr != 0); //this should never happen.
     if (cr.get_code() <= rootPtr->data().get_code())
     {
          if (rootPtr->left() == 0)
          {
              rootPtr->set_left(new binary_tree_node<city_record>(cr));
              //rootPtr.left.data = cr;
          }
          else
              insertRecur(cr,rootPtr->left());
      }
      else
      {
          if (rootPtr->right() == 0)
          {
              rootPtr->set_right(new binary_tree_node<city_record>(cr));
          }
          else
              insertRecur(cr,rootPtr->right());
      }
   }
   
   
   
   
   
   
   
   
   
   
   void city_db::insert(city_record cr)
   {
      std::cout << "about to start operation."<<std::endl;
      if (root_ptr == 0) // no items, we can do this insert ourselves.
      {
         std::cout << "about to insert into the tree!!"<<std::endl;
         root_ptr = new binary_tree_node<city_record>(cr);
         std::cout << "inserted! phew!"<<std::endl;
         //root_ptr.data = cr;
      }
     else
         insertRecur(cr,root_ptr); 
   }
   
   void city_db::remove(int CityCode)
   {
   }
   void city_db::remove(int x, int y)
   {
   }
   bool city_db::search(int CityCode)
   {
      binary_tree_node<city_record>* temp = searchRecur(CityCode,root_ptr);
      if(temp != 0)
          return true;
      else
          return false;
   }
   
   bool city_db::search(int x, int y)
   {
      binary_tree_node<city_record>* temp = searchRecur(x,y,root_ptr);
      if(temp != 0)
          return true;
      else
          return false;
   }
      

   
    bool city_db::empty()
   {
      return (root_ptr == 0);
   }
   
   void city_db::printTree()
   {
      print(root_ptr, 0);
   }
   

}








