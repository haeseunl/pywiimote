// FILE: CityRecord.h
// PROVIDES: A class for a city record.
//
// CONSTRUCTOR for the city_record class:
//   city_record( int init_code = int(),
//                int init_x = int(),
//                int init_y = int() )
//     Precondition: (none)
//     Postcondition: The new city_record has its code set
//     to init_code, x set to init_x, and y set to init_y.
//
// CONST MEMBER FUNCTIONS for the city_record class:
//
//   int get_code() const
//     Precondition: (none)
//     Postcondition: The code of the city_record is returned.
//   int get_x() const
//     Precondition: (none)
//     Postcondition: The x coordinate of the city_record is
//     returned.
//   int get_y() const
//     Precondition: (none)
//     Postcondition: The y coordinate of the city_record is
//     returned.
//   bool operator<=(const city_record& rhs) const
//     Precondition: (none)
//     Postcondition: If code of invoking object is <= code
//     of rhs, true is returned, otherwise false is returned.
//   bool operator>(const city_record& rhs) const
//     Precondition: (none)
//     Postcondition: If code of invoking object is > code
//     of rhs, true is returned, otherwise false is returned.
//   bool operator==(const city_record& rhs) const
//     Precondition: (none)
//     Postcondition: If code of invoking object is == code
//     of rhs, true is returned, otherwise false is returned.
//   bool operator<(const city_record& rhs) const
//     Precondition: (none)
//     Postcondition: If code of invoking object is < code
//     of rhs, true is returned, otherwise false is returned.
//
// MODIFICATION MEMBER FUNCTIONS for the city_record class:
//
//   void set_code(int city_code)
//     Precondition: 1000 <= city_code <= 9999
//     Postcondition: The code of the city_record is set to
//     city_code.
//   void set_x(int city_x)
//     Precondition: (none)
//     Postcondition: The x coordinate of the city_record is
//     set to city_x.
//   void set_y(int city_y)
//     Precondition: (none)
//     Postcondition: The y coordinate of the city_record is
//     set to city_y.
//
// NON-MEMBER FUNCTIONS for the city_record class:
//
//   bool xyIdentical(const city_record& first,
//                    const city_record& second)
//     Precondition: (none)
//     Postcondition: If the x coordinate of first == the x
//     coordinate of second AND the y coordinate of first ==
//     the y coordinate of second, true is returned, otherwise
//     false is returned.
//   std::ostream& operator<<(std::ostream& out,
//                            const city_record& source)
//     Precondition: (none)
//     Postcondition: The code and x and y coordinates of source
//     is written to out and a reference to out is returned. An
//     example of the format of output written (for source with
//     code of 1234, x coordinate of 2345, and y coordinate of
//     3456 is shown below:
//
//     1234 (2345, 3456)
//
//     For usage flexibility, no newline is written at the end.

#ifndef CITY_RECORD_H
#define CITY_RECORD_H
#include <iostream>

namespace cs3358Spring2007Assign08
{
   class city_record
   {
   public:
      city_record(int init_code = 0,
                  int init_x = 0,
                  int init_y = 0);
      bool operator<=(const city_record& rhs) const;
      bool operator>(const city_record& rhs) const;
      bool operator==(const city_record& rhs) const;
      bool operator<(const city_record& rhs) const;
      int get_code() const;
      int get_x() const;
      int get_y() const;
      void set_code(int city_code);
      void set_x(int city_x);
      void set_y(int city_y);
   private:
      int code; // unique code for city
      int x;    // x-coordinate
      int y;    // y-coordinate
   };
   bool xyIdentical(const city_record& first,
                    const city_record& second);
   std::ostream& operator<<(std::ostream& out,
                            const city_record& source);
}

#endif
