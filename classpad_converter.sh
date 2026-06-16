#!/bin/bash

# Output when -h or --help is provided
classpad_converter_help() {
    echo "🛈 Use: $0 [-v] -i <input_file> -o <output_file> [-n <name> -d <dir>]"
    echo "       $0 [--verbose] --input <input_file> --output <output_file> [--name <name> --dir <directory>]"
    echo "       $0 -h"
    echo "       $0 --help"
    echo ""
    echo "🛈 General options:"
    echo "       -i, --input    path to .txt or .xcp file (required)"
    echo "       -o, --output   path to .xcp or .txt file (required)"
    echo "       -v, --verbose  shows additional debugging messages"
    echo "       -h, --help     shows this help message"
    echo ""
    echo "🛈 Specific options (required only when converting from .txt to .xcp):"
    echo "       -n, --name     string that identifies the program (maximum length of 8 basic characters)"
    echo "       -d, --dir      name for the Casio ClassPad folder (maximum length of 8 basic characters)"
    echo ""
    echo "🛈 Detailed constraints for --name and --dir strings:"
    echo "     ◦ Maximum of 8 characters"
    echo "     ◦ Standard/basic characters only (no accents or specific characters i.e. 'ñ', 'ç' or similar)"
    echo "     ◦ The string must not begin with a digit, but digits can be found in the middle or end of the string"
    echo ""
    echo "🛈 Valid string examples:"
    echo "     ◦ test123"
    echo "     ◦ calculus"
    echo "     ◦ Deg2Rad"
    echo ""
    echo "🛈 Invalid string examples:"
    echo "     ◦ 123test"
    echo "     ◦ cálculos"
    echo "     ◦ DegreesToRadians"
    echo ""
    echo "🛈 Parameters --name and --dir are ignored when converting from XCP to TXT."
}

INPUT=""
OUTPUT=""
NAME=""
DIR=""
VERBOSE=""

# Regex to validate -n and -d parameters (1 initial small or capital letter 
# plus up to 7 additional letters/digits, limiting the maximum length to 8)
VALID_REGEXP="^[a-zA-Z][a-zA-Z0-9]{0,7}$"

# Parsing arguments from the command line
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            classpad_converter_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE="-v"
            shift 1
            ;;
        -i|--input)
            if [[ -n "$2" && "$2" != -* ]]; then INPUT="$2"; shift 2; else echo -e "🗶 Parameter --input is missing.\n  Use '$0 -h' for help." >&2; exit 1; fi
            ;;
        -o|--output)
            if [[ -n "$2" && "$2" != -* ]]; then OUTPUT="$2"; shift 2; else echo -e "🗶 Parameter --output is missing.\n  Use '$0 -h' for help." >&2; exit 1; fi
            ;;
        -n|--name)
            if [[ -n "$2" && "$2" != -* ]]; then NAME="$2"; shift 2; else echo -e "🗶 Parameter --name is missing.\n  Use '$0 -h' for help." >&2; exit 1; fi
            ;;
        -d|--dir)
            if [[ -n "$2" && "$2" != -* ]]; then DIR="$2"; shift 2; else echo -e "🗶 Parameter --dir is missing.\n  Use '$0 -h' for help." >&2; exit 1; fi
            ;;
        *)
            echo -e "🗶 Unknown parameter '$1'.\n" >&2
            classpad_converter_help
            exit 1
            ;;
    esac
done

# Validating required global parameters
if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
    echo -e "🗶 Parameters --input and --output are required.\n  Use '$0 -h' for help." >&2
    exit 1
fi

# Identifying the conversion mode depending on the input and output extensions
if [[ "$INPUT" =~ \.txt$ && "$OUTPUT" =~ \.xcp$ ]]; then
    CONVERSION_MODE="TXT_TO_XCP"
elif [[ "$INPUT" =~ \.xcp$ && "$OUTPUT" =~ \.txt$ ]]; then
    CONVERSION_MODE="XCP_TO_TXT"
else
    echo -e "🗶 Mismatching input/output extensions (.txt ←→ .xcp).\n  Use '$0 -h' for help." >&2
    exit 1
fi

# Conditional blocks depending on the conversion mode detected earlier
if [[ "$CONVERSION_MODE" == "TXT_TO_XCP" ]]; then
    
    # Ensuring the name and dir parameters are provided when converting from TXT to XCP
    if [[ -z "$NAME" || -z "$DIR" ]]; then
        echo -e "🗶 Parameters --name and --dir parameters are required to convert TXT to XCP.\n  Use '$0 -h' for help." >&2
        exit 1
    fi

    # Checking if the name string is valid
    if [[ ! "$NAME" =~ $VALID_REGEXP ]]; then
        echo -e "🗶 Parameter --name '$NAME' string format is invalid.\n  Use '$0 -h' for help." >&2
        exit 1
    fi

    # Checking if the dir string is valid
    if [[ ! "$DIR" =~ $VALID_REGEXP ]]; then
        echo -e "🗶 Parameter --dir '$DIR' string format is invalid.\n  Use '$0 -h' for help." >&2
        exit 1
    fi

    echo "⇆ Converting from TXT to XCP..." && \
      echo "✔ Parameters '--name $NAME' and '--dir $DIR' are valid" && \
      ./classpad_encoder.py --fromUTF8 ${INPUT} encoded_${INPUT} && \
      echo "⚠ The file 'encoded_$INPUT' will be removed once conversion to XCP is finished." && \
      ./txt2xcp.py -l ${VERBOSE} -o ${OUTPUT} -n ${NAME} -d ${DIR} encoded_${INPUT} && \
      rm encoded_${INPUT} && \
      echo "⚠ The file 'encoded_$INPUT' is no longer needed and has been removed." && \
      echo "✔ The file '$INPUT' has been converted to '$OUTPUT'."

elif [[ "$CONVERSION_MODE" == "XCP_TO_TXT" ]]; then
    echo "⇆ Converting from XCP to TXT..."

    if [[ -n "$NAME" || -n "$DIR" ]]; then
        echo "🛈 Parameters --name and --dir are ignored when converting from XCP to TXT."
    fi

    echo "🛈 Processing input file: '$INPUT'" && \
      ./txt2xcp.py -l -u ${VERBOSE} -o encoded_${OUTPUT} ${INPUT} && \
      echo "⚠ The file 'encoded_$OUTPUT' will be removed once conversion to TXT is finished." && \
      ./classpad_encoder.py --toUTF8 encoded_${OUTPUT} ${OUTPUT} && \
      rm encoded_${OUTPUT} && \
      echo "⚠ The file 'encoded_$OUTPUT' is no longer needed and has been removed." && \
      echo "✔ The file '$INPUT' has been converted to '$OUTPUT'."
fi

exit 0
