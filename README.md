
Code base is assuming we are only downloading from the zinc15 database
and using the file name structure.


Layout:
- ligands     - A directory containing lingands organized into directories
                of their source followed by their type such as, ligands/zinc15/mol2
                will contain all the mol2 files that were downloaded from ZINC15

- schema.sql  - Database schema

- utils       - Set of tools for parsing and interpreting files in ligands
                when adding a new type of file, make sure to create 
                the tools for parsing that file here

- db.py       - script to load the data when provided a directory containing
                the files to add
