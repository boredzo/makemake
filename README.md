# makemake
## A command to quickly create a robust Makefile

This is a command-line tool that quickly and configurably creates a Makefile for one or more single-file C/Objective-C/C++/Objective-C++ program targets.

The Makefile can contain an ARCHS variable, an LDFLAGS variable, both, or neither.

Running `makemake -framework Cocoa test` produces this:

    LDFLAGS+=-framework Cocoa
    
    test: test.o
    
    clean:
    	rm *.o
    .PHONY: clean

Running “make” will implicitly make “test”, which will implicitly make “test.o”; if test.c, test.m, test.cc, test.cpp, or test.mm exists, make will compile it, then link the program from the .o file.
