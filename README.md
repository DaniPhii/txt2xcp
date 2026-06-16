# txt2xcp

This project consists of a Bash script and two Python programs to transcode from UTF-8/Unicode characters to ClassPad-specific encoding, then convert the resulting text to an XCP file and vice versa for the calculator Casio ClassPad II (fx-CP400). I've used Google Gemini 3.5 Flash to create some of the functions and adjusted them manually to fit my needs. I have manually extracted the byte codes from the device to create a table mapping the hex values in Unicode and ClassPad-specific encoding. I could have chosen faster ways of doing this but didn't want to, as I enjoyed spending time doing this my own way with no automations involved.

This project is a detached fork of [the original repository](https://github.com/SnailMath/txt2xcp "SnailMath/txt2xcp") by SnailMath. This fork has been detached to translate [the original C code](https://github.com/DaniPhii/txt2xcp/blob/dd5c923b6b3b93ac31a0e849f64dd743c1fb1cac/txt2xcp.c "txt2xcp.c") to Python. After this, I went on adding additional features to the original program.

## classpad_converter.sh

This is the main script to use when converting from TXT to XCP files and vice versa, as this checks the user's input and calls the Python programs to either extract text and convert it to UTF-8 or transcode text files into ClassPad-specific encoding and pack it as XCP files.

This script uses a regular expression to validate the variable and directory names when converting from TXT to XCP to ensure there are no issues when the calculator imports the variable. For example, if the variable's name starts with a digit, it will bug the calculator and might be difficult to select it in the ClassPad from the list of variables to rename or remove it. This validation could also been included in the Python programs, but I chose to keep this logic in a separate Bash script.

This script will use the option `-l` by default when calling the program `txt2xcp.py`, so newline characters are always converted when packing and unpacking files.

```
🛈 Use: ./classpad_converter.sh [-v] -i <in_file> -o <out_file> [-n <name> -d <dir>]
       ./classpad_converter.sh -h
       ./classpad_converter.sh --help

🛈 General options:
       -i, --input  PATH  path to .txt or .xcp file (required)
       -o, --output PATH  path to .xcp or .txt file (required)
       -v, --verbose      shows additional debugging messages
       -h, --help         shows this help message

🛈 Specific options (required only when converting from .txt to .xcp):
       -n, --name     string that identifies the program 
                      (maximum length of 8 basic characters)
       -d, --dir      name for the Casio ClassPad folder 
                      (maximum length of 8 basic characters)

🛈 Detailed constraints for --name and --dir strings:
     ◦ Maximum of 8 characters
     ◦ Standard/basic characters only (no accents or specific
     characters i.e. 'ñ', 'ç' or similar)
     ◦ The string must not begin with a digit, but digits can
     be found in the middle or end of the string

🛈 Valid string examples:
     ◦ test123
     ◦ calculus
     ◦ Deg2Rad

🛈 Invalid string examples:
     ◦ 123test
     ◦ cálculos
     ◦ DegreesToRadians

🛈 Parameters --name and --dir are ignored when converting from XCP to TXT.
```

The Python scripts `classpad_encoder.py` and `txt2xcp.py` can be used as standalone programs if needed, so details for each are provided below.

### classpad_encoder.py

This script transcodes characters from Unicode to ClassPad-specific encoding and vice versa. This is useful to extract Casio BASIC programs that use specific symbols and characters and make the resulting text readable and editable.

You can check the fx-CP400 character sets that will be transcoded into Unicode and vice versa in the [NOTES.md](https://github.com/DaniPhii/txt2xcp/blob/main/NOTES.md) document.

```
🛈 Usage: classpad_encoder.py [-h] (--toUTF8 | --fromUTF8) input_path [output_path]

🛈 This script transcodes text characters for the Casio ClassPad II (fx-CP400).

🛈 Arguments:
       input_path   input file path
       output_path  output file path (optional)

🛈 Options:
       -h, --help   shows the help message and exit
       --toUTF8     transcodes characters from Casio fx-CP400 to UTF-8
       --fromUTF8   transcodes characters from UTF-8 to Casio fx-CP400
```

### txt2xcp.py

SnailMath's original C program can be downloaded from [this link](https://github.com/SnailMath/txt2xcp/releases "SnailMath/txt2xcp Releases Page").

The original C program converts `.txt` or `.bin` files to `.xcp` files for the calculator ClassPad II (fx-CP400).

Using Google Gemini 3.5 Flash, [the original C code](https://github.com/DaniPhii/txt2xcp/blob/dd5c923b6b3b93ac31a0e849f64dd743c1fb1cac/txt2xcp.c "txt2xcp.c") has been translated to this Python version of the program, and additional features have been added since, i.e. unpacking feature to extract the text from a `.xcp` file and making the program aware of custom header bytes to avoid corrupting ClassPad-encoded characters when replacing newline characters.

```
🛈 Usage: ./txt2xcp.py [OPTIONS] SOURCE [DEST]

🛈 Converts the file SOURCE to an .xcp file called DEST.

🛈 Options:
       -l       Convert newline Characters from "\r\n" (Windows) or "\n"
                (Linux) to "\r" (The newline characters used by the calc). Use
                this only for text, and don't use it for programs or binary data.
       -n NAME  Specify the name of the variable
       -d NAME  Specify the name of the folder
       -o NAME  Specify the output filename, if not provided at the end
       -v       Verbose the output
       -p       Don't use it! Specify character used for padding (default \x00)
       -u       Unpack text/binary data from an XCP file

🛈 Examples:
       ./txt2xcp.py yourfile1.bin newfile1.xcp
       ./txt2xcp.py -l yourfile2.txt newfile2.xcp
       ./txt2xcp.py -l -o newfile3.xcp -n newfile3 -d main yourfile3.txt
       ./txt2xcp.py -l -u -o newfile4.txt yourfile4.xcp

🛈 The xcp file is of the type Casio Program(Text).
```

In the third example, the variable will be called `newfile3` when you import it on the calculator, but you can also rename it later on the device. Also, it doesn't matter that the directory is anything different from `main`, as you can also choose where to import the variable.

For more details about SnailMath's work related to the Casio fx-CP400, you can check [this repository](https://github.com/SnailMath/classpad "SnailMath/classpad").

## License & Modifications

This project is a detached fork of [the original repository](https://github.com/SnailMath/txt2xcp "SnailMath/txt2xcp") by Pascal aka SnailMath. 
[All original code](https://github.com/DaniPhii/txt2xcp/tree/dd5c923b6b3b93ac31a0e849f64dd743c1fb1cac "DaniPhii/txt2xcp/tree/dd5c923") is Copyright (c) 2020 SnailMath.

Modifications, feature additions and extra scripts since 2026 are Copyright (c) Dani Poveda aka DaniPhii and licensed under the same MIT License.
