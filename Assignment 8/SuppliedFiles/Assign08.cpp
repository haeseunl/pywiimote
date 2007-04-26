// FILE: Assign08.cpp
// An interactive test program for the city_db class implemented with
// a binary search tree.

#include <cctype>   // provides toupper
#include <iostream> // provides cout, cin
#include <cstdlib>  // provides EXIT_SUCCESS, size_t
#include "CityDb.h" // provides city_db class
using namespace std;
using namespace cs3358Spring2007Assign08;

// PROTOTYPES for the functions used in this test program.
void print_menu();
// Precondition: (none)
// Postcondition: A menu of choices for this program has been written
// to cout.

char get_user_command();
// Precondition: (none)
// Postcondition: The user is prompted to enter a one character
// command. A line of input (with at least one character) is
// read, and the first character of the input line is returned.

void get_record(city_record& record);
// Precondition: (none)
// Postcondition: The user is prompted to enter the data for a
// city (city code, x-coordinate and y-coordinate). The data is
// read and returned via the reference parameter.

int get_code();
// Precondition: (none)
// Postcondition: The user is prompted to enter a city's code.
// The city code is read and returned.

int get_x_or_y(const char description[]);
// Precondition: (none)
// Postcondition: The user is prompted to enter a city's x or y
// coordinate (depending on the supplied description). The
// coordinate is read and returned.

int get_distance();
// Precondition: (none)
// Postcondition: The user is prompted to enter a desired
// distance. The desired distance is read and returned.

int main(int argc, char *argv[])
{
   city_db c;          // city db to perform tests on
   city_record record; // holder for a city's data
   char choice;        // command character entered by user

   cout << "An empty city db has been created." << endl;

   do
   {
	  if (argc < 2)
         print_menu();
      choice = get_user_command();
      switch (choice)
      {
         case 'I':
         case 'i':
                   get_record(record);
                   c.insert(record);
                   break;
         case 'P': if ( ! c.empty() )
                      ;// replace null statement with your code
                   else
                      cout << "db is empty." << endl;
                   break;
         case 'p': if ( ! c.empty() )
                   {
                      // write your code here
                   }
                   else
                      cout << "db is empty." << endl;
                   break;
         case 'D': if ( ! c.empty() )
                   {
                      // write your code here
                   }
                   else
                      cout << "db is empty." << endl;
                   break;
         case 'd': if ( ! c.empty() )
                   {
                      // write your code here
                   }
                   else
                      cout << "db is empty." << endl;
                   break;
         case 'S': if ( ! c.empty() )
                   {
                      if (c.search(get_code()))
                         cout << " that item was in the db." << endl;
                      else
                         cout << " that item was not in the db." << endl;
                      
                   }
                   else
                      cout << "db is empty." << endl;
                   break;
         case 's': if ( ! c.empty() )
                   {
                      int x = get_x_or_y("x-coordinate");
                      int y = get_x_or_y("y-coordinate");
                      if(c.search(x,y))
                         cout << " that item was in the db." << endl;
                      else
                         cout << " that item was not in the db." << endl;
                   }
                   else
                      cout << "db is empty." << endl;
                   break;
	      case 't':
	      case 'T': if ( ! c.empty() )
                      c.printTree();
                   else
                      cout << "db is empty." << endl;
                   break;
	      case 'q':
	      case 'Q': cout << "Bye..." << endl;
                   break;
         default:  cout << choice << " is invalid. Sorry... try again."
                        << endl;
      }
   }
   while ( toupper(choice) != 'Q' );

   return EXIT_SUCCESS;
}

void print_menu()
{
   cout << "Following choices are available with the city db: " << endl;
   cout << " I  Insert a city into db" << endl;
   cout << " D  Delete a city from db, given city code" << endl;
   cout << " d  Delete a city from db, given city coordinates" << endl;
   cout << " S  Search for a city in db, given city code" << endl;
   cout << " s  Search for a city in db, given city coordinates" << endl;
   cout << " P  Print all cities (in code order) in db" << endl;
   cout << " p  Print cities (in code order) within given distance "
        << "from given location" << endl;
   cout << " T  Print BST (backward_in_order print of city codes)"
        << endl;
   cout << " Q  Quit this program" << endl;
}

char get_user_command()
{
   char command;

   cout << "Enter choice: ";
   cin >> command;
   cin.ignore(999, '\n'); // clear input buffer up to first '\n'
   cout << "choice " << command << " read." << endl;
   return command;
}

void get_record(city_record& record)
{
   int city_code, city_x, city_y;

   city_code = get_code();
   record.set_code(city_code);

   city_x = get_x_or_y("x-coordinate");
   record.set_x(city_x);

   city_y = get_x_or_y("y-coordinate");
   record.set_y(city_y);
}

int get_code()
{
   int city_code;

   cout << "Enter city's code (1000 - 9999): ";
   cin  >> city_code;
   while (true)
   {
      while ( ! cin.good() )
      {
         cerr << "Invalid input..." << endl;
         cin.clear();
         cin.ignore(999, '\n');
         cout << "Please re-enter city's code (1000 - 9999): ";
         cin  >> city_code;
      }
      if (city_code >= 1000 && city_code <= 9999)
         break;
      else
      {
         cerr << "Invalid input..." << endl;
         cout << "Please re-enter city's code (1000 - 9999): ";
         cin  >> city_code;
      }
   }
   cout << "code " << city_code << " read." << endl;
   return city_code;
}

int get_x_or_y(const char description[])
{
   int input;

   cout << "Enter " << description << ": ";
   cin  >> input;
   while ( ! cin.good() )
   {
      cerr << "Invalid input..."<< endl;
      cin.clear();
      cin.ignore(999, '\n');
      cout << "Please re-enter " << description << ": ";
      cin  >> input;
   }
   cout << description << ' ' << input << " read." << endl;
   return input;
}

int get_distance()
{
   int distance;

   cout << "Enter desired distance: ";
   cin  >> distance;
   while (true)
   {
      while ( ! cin.good() )
      {
         cerr << "Invalid input..."<< endl;
         cin.clear();
         cin.ignore(999, '\n');
         cout << "Please re-enter desired distance: ";
         cin  >> distance;
      }
      if (distance > 0)
         break;
      else
      {
         cerr << "Invalid input..." << endl;
         cout << "Please re-enter desired distance: ";
         cin  >> distance;
      }
   }
   cout << "distance " << distance << " read." << endl;
   return distance;
}
