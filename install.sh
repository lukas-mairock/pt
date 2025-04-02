#! /usr/bin/bash

python_version=$(python3 --version | awk '{print $2}' | grep -Eo '^[0-9]+\.[0-9]+')
python_directory="/usr/lib/python$python_version"

if [[ -z $python_version ]]; then
	echo "No supported version of python found"
	exit
fi

if [[ ! -d $python_directory ]]; then
	echo "Python lib directory cannot be found"
	exit
fi

sudo cp pt.py $python_directory
