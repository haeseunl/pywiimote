# FILE: Assign08.cpp
# An interactive test program for the city_db class implemented with
# a binary search tree.

#include <cctype>   # provides toupper
#include <iostream> # provides cout, cin
#include <cstdlib>  # provides EXIT_SUCCESS, size_t
#include "CityDb.h" # provides city_db class

# print_menu()
# Precondition: (none)
# Postcondition: A menu of choices for this program has been written
# to cout.

# get_user_command()
# Precondition: (none)
# Postcondition: The user is prompted to enter a one character
# command. A line of input (with at least one character) is
# read, and the first character of the input line is returned.

# get_record()
# Precondition: (none)
# Postcondition: The user is prompted to enter the data for a
# city (city code, x-coordinate and y-coordinate). The data is
# read and returned.

# get_code()
# Precondition: (none)
# Postcondition: The user is prompted to enter a city's code.
# The city code is read and returned.

# get_x_or_y(description)
# Precondition: (none)
# Postcondition: The user is prompted to enter a city's x or y
# coordinate (depending on the supplied description). The
# coordinate is read and returned.

# get_distance()
# Precondition: (none)
# Postcondition: The user is prompted to enter a desired
# distance. The desired distance is read and returned.

def main():
   c = city_db()   # city db to perform tests on
   record = city_record() # holder for a city's data
   choice = ""        # command character entered by user

   print "An empty city db has been created." + "\n"

   do
   {
	  if (argc < 2)
         print_menu();
      choice = get_user_command();
      switch (choice)
      {
         case 'I':
         case 'i':
                   # write your code here
                   break;
         case 'P': if ( ! c.empty() )
                      ;# replace null statement with your code
                   else
                      print "db is empty." + "\n"
                   break;
         case 'p': if ( ! c.empty() )
                   {
                      # write your code here
                   }
                   else
                      print "db is empty." + "\n"
                   break;
         case 'D': if ( ! c.empty() )
                   {
                      # write your code here
                   }
                   else
                      print "db is empty." + "\n"
                   break;
         case 'd': if ( ! c.empty() )
                   {
                      # write your code here
                   }
                   else
                      print "db is empty." + "\n"
                   break;
         case 'S': if ( ! c.empty() )
                   {
                      # write your code here
                   }
                   else
                      print "db is empty." + "\n"
                   break;
         case 's': if ( ! c.empty() )
                   {
                      # write your code here
                   }
                   else
                      print "db is empty." + "\n"
                   break;
	      case 't':
	      case 'T': if ( ! c.empty() )
                      ;# replace null statement with your code
                   else
                      print "db is empty." + "\n"
                   break;
	      case 'q':
	      case 'Q': print "Bye..." + "\n"
                   break;
         default:  print choice + " is invalid. Sorry... try again."
                        + "\n"
      }
   }
   while ( toupper(choice) != 'Q' );

   return EXIT_SUCCESS;
}

void print_menu()
{
   print "Following choices are available with the city db: " + "\n"
   print " I  Insert a city into db" + "\n"
   print " D  Delete a city from db, given city code" + "\n"
   print " d  Delete a city from db, given city coordinates" + "\n"
   print " S  Search for a city in db, given city code" + "\n"
   print " s  Search for a city in db, given city coordinates" + "\n"
   print " P  Print all cities (in code order) in db" + "\n"
   print " p  Print cities (in code order) within given distance "
        + "from given location" + "\n"
   print " T  Print BST (backward_in_order print of city codes)"
        + "\n"
   print " Q  Quit this program" + "\n"
}

char get_user_command()
{
   char command;

   print "Enter choice: ";
   cin >> command;
   cin.ignore(999, '\n'); # clear input buffer up to first '\n'
   print "choice " + command + " read." + "\n"
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

   print "Enter city's code (1000 - 9999): ";
   cin  >> city_code;
   while (true)
   {
      while ( ! cin.good() )
      {
         cerr + "Invalid input..." + "\n"
         cin.clear();
         cin.ignore(999, '\n');
         print "Please re-enter city's code (1000 - 9999): ";
         cin  >> city_code;
      }
      if (city_code >= 1000 && city_code <= 9999)
         break;
      else
      {
         cerr + "Invalid input..." + "\n"
         print "Please re-enter city's code (1000 - 9999): ";
         cin  >> city_code;
      }
   }
   print "code " + city_code + " read." + "\n"
   return city_code;
}

int get_x_or_y(const char description[])
{
   int input;

   print "Enter " + description + ": ";
   cin  >> input;
   while ( ! cin.good() )
   {
      cerr + "Invalid input..."+ "\n"
      cin.clear();
      cin.ignore(999, '\n');
      print "Please re-enter " + description + ": ";
      cin  >> input;
   }
   print description + ' ' + input + " read." + "\n"
   return input;
}

int get_distance()
{
   int distance;

   print "Enter desired distance: ";
   cin  >> distance;
   while (true)
   {
      while ( ! cin.good() )
      {
         cerr + "Invalid input..."+ "\n"
         cin.clear();
         cin.ignore(999, '\n');
         print "Please re-enter desired distance: ";
         cin  >> distance;
      }
      if (distance > 0)
         break;
      else
      {
         cerr + "Invalid input..." + "\n"
         print "Please re-enter desired distance: ";
         cin  >> distance;
      }
   }
   print "distance " + distance + " read." + "\n"
   return distance;
}
