// FILE: CityRecord.cpp
// IMPLEMENTS: The city_record class (see CityRecord.h for
//             documentation).

#include "CityRecord.h"
#include <cassert>

namespace cs3358Spring2007Assign08
{
   city_record::city_record(int init_code, int init_x, int init_y)
               : code(init_code), x(init_x), y(init_y) { }
   bool city_record::operator<=(const city_record& rhs) const
   { return code <= rhs.code; }

   bool city_record::operator>(const city_record& rhs) const
   { return code > rhs.code; }

   bool city_record::operator==(const city_record& rhs) const
   { return code == rhs.code; }

   bool city_record::operator<(const city_record& rhs) const
   { return code < rhs.code; }

   int city_record::get_code() const
   { return code; }

   int city_record::get_x() const
   { return x; }

   int city_record::get_y() const
   { return y; }

   void city_record::set_code(int city_code)
   {
      assert(city_code >= 1000 && city_code <= 9999);
      code = city_code;
   }

   void city_record::set_x(int city_x)
   { x = city_x; }

   void city_record::set_y(int city_y)
   { y = city_y; }

   bool xyIdentical(const city_record& first, const city_record& second)
   {
      return first.get_x() == second.get_x() &&
             first.get_y() == second.get_y();
   }
   std::ostream& operator<<(std::ostream& out, const city_record& source)
   {
      out << source.get_code();
      /* un-comment the following output statement if desired */
      // out << source.get_code() << " (" << source.get_x()
      //     << ", " << source.get_y() << ')';
      return out;
   }

}
