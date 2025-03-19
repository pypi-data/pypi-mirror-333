# Dummy File Generator

A simple Python script to generate dummy files of specified sizes.

[![asciicast](https://asciinema.org/a/707507.svg)](https://asciinema.org/a/707507)

## Features

* User-friendly interface using `rich`
* Option to input **custom filename**
* Option to input **custom file size** (in KB, MB, or GB)
* Displays initial and final free disk space
* Displays disk space used by the generated file

## Requirements

* Python 3.x
* `rich` library (install using `pip install rich`)
* `shutil` library (part of the Python Standard Library)

## Usage

0. Run without installation using `uvx dummygen-cli.py`
1. Run the script using `python dummygen-cli.py`
2. Follow the prompts to input the desired filename and size
3. The script will generate a dummy file of the specified size

## Example
```
$ python dummygen-cli.py
# Enter the desired filename: example.txt
# Enter the desired size (e.g., 100MB, 2.5GB): 500MB
```
This will generate a dummy file named `example.txt` with a size of 500 MB.
