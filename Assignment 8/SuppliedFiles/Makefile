NAME = a8
CC = c++
DEP = Assign08.o CityDb.o CityRecord.o
OBJ = $(DEP)
CFLAGS = -g -Wall -O2 -pedantic -ansi

$(NAME): $(DEP)
	$(CC) $(OBJ) -o $(NAME)
Assign06.o: Assign08.cpp CityDb.h CityDb.cpp CityRecord.h CityRecord.cpp BinTree.h BinTree.template
	$(CC) $(CFLAGS) -c Assign08.cpp
CityRecord.o: CityRecord.h CityRecord.cpp
	$(CC) $(CFLAGS) -c CityRecord.cpp
CityDb.o: CityDb.h CityDb.cpp
	$(CC) $(CFLAGS) -c CityDb.cpp

clean:
	@rm -rf $(DEP)
cleanall:
	@rm -rf $(DEP) $(NAME)

