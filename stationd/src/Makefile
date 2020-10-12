TARGET = stationd
CC = gcc
override CFLAGS += -g -Og -Wall

.PHONY: all clean

OBJECTS = $(patsubst %.c, %.o, $(wildcard *.c))
HEADERS = $(wildcard *.h)

%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -Wall -o $@ -li2c -lpthread

all: $(TARGET)

clean:
	-rm -f *.o
	-rm -f $(TARGET)
