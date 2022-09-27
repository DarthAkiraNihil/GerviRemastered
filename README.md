# Gervi Remastered (True Gervi)
So, this is the remastered version of Gervi project. It's more structured, error-free, functional and optimized.
## List of changes 
In this version were removed the following elements, which were in the old version:
* Reading and writing different types of values (bool, int, word etc.)
* Operations with only one bit in BinaryData objects
* A virtual machine as a text file
* Different types of memory: working and RAM

In this version were improved:
* Math operations
* A virtual machine as a binary file with LZMA compression
* Less logic operations
* PrimaryMemory uses integers for the oparations, not BinaryObjects (they're deprecated now)
## Repository contest
This repository has this components:
* Gervi core
* Gervi core doc (in development)
* GIDE (IDE for Gervi scripts)
* gvmmake program (for creating vitrual machine files)
## License
This project is licensed under Apache 2.0 license
