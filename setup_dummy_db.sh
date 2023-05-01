#!/bin/bash
search_dir=tools/dummy_db_scripts
for py_file in "$search_dir"/*
do
    echo $py_file
    python3 $py_file
done
