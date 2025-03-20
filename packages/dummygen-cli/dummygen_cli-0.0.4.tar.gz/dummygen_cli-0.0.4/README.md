# dummygen-cli

A command-line tool to quickly generate dummy files of specified sizes.

[![asciicast](https://asciinema.org/a/707507.svg)](https://asciinema.org/a/707507)

## Features

* **Simple Command-Line Interface:** Easy-to-use prompts powered by `rich`.
* **Custom Filename:** Specify the desired filename for your dummy file.
* **Flexible File Size:** Define the file size in KB, MB, GB, or TB.
* **Disk Space Monitoring:** Displays initial and final free disk space, and the space used.
* **Robust Error Handling:** Checks for sufficient disk space during file generation.

## Installation & Usage

```bash
pip install dummygen-cli # or execute direcly "uvx dummygen-cli"
# 2. Input the desired filename and size
# 3. The script will generate a dummy file of the specified size
```

## Example

```
$ python dummygen-cli.py
# Enter the desired filename: example.txt
# Enter the desired size (e.g., 100MB, 2.5GB): 500MB
```

## Requirements

* Python 3.x
* `rich` library (install using `pip install rich`)
* `shutil` library (part of the Python Standard Library)

This will generate a dummy file named `example.txt` with a size of 500 MB.