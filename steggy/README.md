
# Embedded Data Steganography Utility

This Python utility allows you to embed files or directories into cover images using steganography techniques. It also provides options to extract embedded data from images and extract directory contents from cover files. Additionally, you can extract EXIF data from images and generate passwords.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [License](#license)

## Requirements

- Python 3.x
- Required Python packages can be found in requirements.txt 

## Installation

1. Clone this repository or download the script file.
2. Make sure you have Python installed on your system.
3. Install the required Python package using pip:
```bash
pip install -r requirements.txt 
```

## Usage

Run the script from the command line:
```bash
python steggy.py
```

Follow the prompts to embed, extract, or perform other operations.

## Options

- **Embed file in cover file**: Embed a file into an image.
- **Extract file from cover file**: Extract a file from an image.
- **Embed directory in cover file**: Embed a directory into an image.
- **Extract directory from cover file**: Extract a directory from an image.
- **Extract EXIF data from image**: Extract geotag information from an image.
- **Generate password**: Generate a strong password.

## License

This project is licensed under the [MIT License](LICENSE).

