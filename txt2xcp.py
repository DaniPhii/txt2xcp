#!/usr/bin/env python3

# This program converts text into XCP files used by
# calculators like the Casio fx-CP400 (ClassPad II).
# 
# 
# This is a program originally written in C by Pascal aka SnailMath.
#   Original GitHub repo: https://github.com/SnailMath/txt2xcp
# 
# 
# SnailMath is not afiliated with any company. Neither is DaniPhii.
# 
# 
# This version is a direct translation from C to Python made assisted by 
# Google Gemini 3.5 Flash and includes an unpacking option to extract 
# the text data from XCP files that wasn't included in the original C
# version of this program. Also, this version considers specific character 
# encoding headers used by the calculator to avoid breaking the encoding
# and corrupting the original text written locally on the device. This 
# is very useful when the Python script classpad_encoder.py is used to 
# transcode the text before and after conversions from/to TXT/XCP files.
# 
# 

import sys
import os
import io

# Global state variables
verbose = 0
chgnew = 0
padchar = 0
unpack = 0
checksum = 0x00

# Constants
BIG_ENDIAN = 1
LITTLE_ENDIAN = 0
len2_length = 4
block_zero_length = 9
eof_length = 2

varname = "file"
folname = "main"
varname_len = 5
folname_len = 5

infile = None
outfile = None

def tobin(ch):
    """Convert an ASCII hex nibble character to a binary integer."""
    if '0' <= ch <= '9':
        return ord(ch) - ord('0')
    else:
        return ord(ch.lower()) - ord('a') + 10

def info_log(*args, **kwargs):
    """Print message only if verbose output is enabled."""
    if verbose:
        print(*args, **kwargs, end='')

def update_checksum(val):
    global checksum
    checksum = (checksum - val) & 0xFF

def xcpwrite(ptr: bytes, stream):
    """Writes bytes to the stream and updates the 8-bit checksum."""
    stream.write(ptr)
    for b in ptr:
        update_checksum(b)

def xcpwriteHexByte(number: int, stream):
    """Writes a byte as two hexadecimal ASCII characters and updates the checksum."""
    hex_str = f"{(number & 0xFF):02x}"
    stream.write(hex_str.encode('ascii'))
    update_checksum(number & 0xFF)

def xcpwriteHexLong(number: int, stream):
    """Writes a 32-bit integer as 8 hexadecimal ASCII characters."""
    xcpwriteHexByte((number >> 24) & 0xFF, stream)
    xcpwriteHexByte((number >> 16) & 0xFF, stream)
    xcpwriteHexByte((number >> 8) & 0xFF, stream)
    xcpwriteHexByte(number & 0xFF, stream)

def xcpputc(ch: int, stream):
    """Writes a single byte to the stream and updates the checksum."""
    stream.write(bytes([ch & 0xFF]))
    update_checksum(ch & 0xFF)

def xcpwriteBinLong(number: int, endianness: int, stream):
    """Writes a 32-bit binary integer in the specified endianness format."""
    if endianness == BIG_ENDIAN:
        xcpputc((number >> 24) & 0xFF, stream)
        xcpputc((number >> 16) & 0xFF, stream)
        xcpputc((number >> 8) & 0xFF, stream)
        xcpputc(number & 0xFF, stream)
    else:  # LITTLE_ENDIAN
        xcpputc(number & 0xFF, stream)
        xcpputc((number >> 8) & 0xFF, stream)
        xcpputc((number >> 16) & 0xFF, stream)
        xcpputc((number >> 24) & 0xFF, stream)

def print_usage():
    prog_name = sys.argv[0]
    sys.stderr.write(f"\n"
                     f"Usage: {prog_name} [OPTIONS] SOURCE [DEST]\n\n"
                     f"Converts the file SOURCE to an .xcp file called DEST.\n\n"
                     f"Options:\n"
                     f"  -l       Convert newline Characters from \"\\r\\n\" (Windows) or \"\\n\"\n"
                     f"           (Linux) to \"\\r\" (The newline characters used by the calc). Use\n"
                     f"           this only for text, and don't use it for programs or binary data.\n"
                     f"  -n NAME  Specify the name of the variable\n"
                     f"  -d NAME  Specify the name of the folder\n"
                     f"  -o NAME  Specify the output filename, if not provided at the end\n"
                     f"  -v       Verbose the output\n"
                     f"  -p       Don't use it! Specify character used for padding (default \\x00)\n"
                     f"  -u       Unpack text/binary data from an XCP file\n\n"
                     f"Examples:\n"
                     f"{prog_name} yourfile1.bin newfile1.xcp\n"
                     f"{prog_name} -l yourfile2.txt newfile2.xcp\n"
                     f"{prog_name} -l -o newfile3.xcp -n newfile3 -d main yourfile3.txt\n"
                     f"{prog_name} -u -o newfile4.txt yourfile4.xcp\n\n"
                     f"The xcp file is of the type Casio Program(Text).\n")

# The files on the calculator are called variables (var for short) and they are placed into folders.
# 
# XCP file structure:
#     1 vcp           10 byte - the text "VCP.XDATA" including the 0x00 terminator
#     2 longnumber     8 byte - (hex ascii) the number 0x5f4d4353
#     3 folname_len    2 byte - (hex ascii) length of the folder name + 1
#     4 folname      2-9 byte - name of the folder including 0x00 terminator
#     5 varname_len    2 byte - (hex ascii) length of the name + 1
#     6 varname      2-9 byte - name of the var including 0x00 terminator) (also called "filename")
#     7 block_31       8 byte - the text "00000031"
#     8 folname2      16 byte - name of the folder, padded with 0xff
#     9 varname2      16 byte - name of the var, padded with 0xff
#    10 len1           4 byte - (binary big endian) The length of len2, block_zero, data, eof 
#                               and padding combined, this has to be divisible by 4, see padding
#    11 block_guq     13 byte - the text "GUQ" followed by ten bytes of 0xff
#    12 len1asc        8 byte - (hex ascii) the value of len1 again, but in ascii hex, small letters
#    13 len2           4 byte - (binary little endian) the length of the data + 3
#    14 block_zero     9 byte - nine times 0x00
#    15 data         len byte - the binary data
#    16 eof            2 byte - The file terminator 0x00 0xff
#    17 padding      0-3 byte - pad the data so len1 is a multiple of 4 [pad with (3-((len+2)&~0x03)) bytes] 
#    18 checksum       2 byte - (hex ascii) the checksum (take 0x00 and subtract all byes, except 
#                               hex-ascii values, these are subtracted as hexadecimal numbers.

def main():
    global verbose, chgnew, padchar, unpack, varname, folname, varname_len, folname_len, infile, outfile, checksum

    argc = len(sys.argv)
    if argc < 2:
        print_usage()
        sys.exit(0)

    i = 1
    while i < argc:
        arg = sys.argv[i]
        if arg == '-l':
            chgnew = 1
        elif arg == '-v':
            verbose = 1
        elif arg == '-u':
            unpack = 1
        elif arg == '-p':
            i += 1
            if i == argc:
                sys.stderr.write("🗶 Parameter \"-p\" is specified but no character is given.\n")
                sys.exit(-1)
            p_arg = sys.argv[i]
            padchar = (tobin(p_arg[0]) << 4) + tobin(p_arg[1])
        elif arg == '-n':
            i += 1
            if i == argc:
                sys.stderr.write("🗶 Parameter \"-n\" is specified but no name is given.\n")
                sys.exit(-1)
            varname = sys.argv[i]
            if len(varname) > 8:
                varname = varname[:8]
            varname_len = len(varname) + 1
        elif arg == '-d':
            i += 1
            if i == argc:
                sys.stderr.write("🗶 Parameter \"-d\" is specified but no name is given.\n")
                sys.exit(-1)
            folname = sys.argv[i]
            if len(folname) > 8:
                folname = folname[:8]
            folname_len = len(folname) + 1
        elif arg == '-o':
            i += 1
            if i == argc:
                sys.stderr.write("🗶 Parameter \"-o\" is specified but no name is given.\n")
                sys.exit(-1)
            if outfile is not None:
                sys.stderr.write("🗶 There are too many output filenames given. Please use just one output file.\n")
                sys.exit(-1)
            outfile = sys.argv[i]
        elif arg.startswith('-'):
            sys.stderr.write(f"🗶 Parameter \"{arg}\" is not a recognized argument.\n")
            sys.exit(-1)
        else:
            if infile is None:
                infile = arg
            elif outfile is None:
                outfile = arg
            else:
                sys.stderr.write("🗶 There are too many filenames given. Please use just one input and one output file!\n")
                sys.exit(-1)
        i += 1

    if infile is None:
        sys.stderr.write("🗶 There is no input file given!\n")
        sys.exit(-1)

    if outfile is None:
        base_filename = infile[:59]
        if unpack:
            if base_filename.lower().endswith('.xcp'):
                base_filename = base_filename[:-4]
            outfile = base_filename + ".txt"
        else:
            outfile = base_filename + ".xcp"

    # Open Input File
    try:
        in_file = open(infile, "rb")
    except Exception:
        sys.stderr.write(f"🗶 Cannot open file \"{infile}\" for reading!\n")
        sys.exit(-1)

    if unpack:
        # --- UNPACK MODE ---
        with in_file:
            info_log("🛈 Step 1: Validating VCP header\n")
            vcp_buf = in_file.read(10)
            if len(vcp_buf) != 10:
                sys.stderr.write("🗶 Premature end of file reading VCP header.\n")
                sys.exit(-1)

            info_log("🛈 Step 2-6: Skipping to folder and variable configurations\n")
            in_file.seek(8, os.SEEK_CUR)

            # Step 3 & 4: Read and skip folder name dynamic chunk
            hex_len = in_file.read(2)
            if len(hex_len) != 2:
                sys.stderr.write("🗶 Premature end of file reading folder length.\n")
                sys.exit(-1)
            f_len = (tobin(chr(hex_len[0])) << 4) + tobin(chr(hex_len[1]))
            in_file.seek(f_len, os.SEEK_CUR)

            # Step 5 & 6: Read and skip variable name dynamic chunk
            hex_len = in_file.read(2)
            if len(hex_len) != 2:
                sys.stderr.write("🗶 Premature end of file reading variable length.\n")
                sys.exit(-1)
            v_len = (tobin(chr(hex_len[0])) << 4) + tobin(chr(hex_len[1]))
            in_file.seek(v_len, os.SEEK_CUR)

            info_log("🛈 Step 7-12: Skipping structured internal byte configurations\n")
            in_file.seek(65, os.SEEK_CUR)

            info_log("🛈 Step 13: Processing block data sizes (len2)\n")
            len2_buf = in_file.read(4)
            if len(len2_buf) != 4:
                sys.stderr.write("🗶 Premature end of file reading len2 block structure.\n")
                sys.exit(-1)

            len2_val = len2_buf[0] | (len2_buf[1] << 8) | (len2_buf[2] << 16) | (len2_buf[3] << 24)
            if len2_val < 3:
                sys.stderr.write("🗶 Structural data format integrity error.\n")
                sys.exit(-1)
            d_len = len2_val - 3

            info_log("🛈 Step 14: Passing block_zero structure configuration\n")
            in_file.seek(9, os.SEEK_CUR)

            info_log("🛈 Step 15: Stream extracting contents data payloads\n")
            out_bytes = bytearray()
            k = 0
            while k < d_len:
                ch_b = in_file.read(1)
                if not ch_b:
                    sys.stderr.write("🗶 Sudden loss of data segments while processing stream.\n")
                    break
                ch = ch_b[0]
                if chgnew:
                    if ch in (0xEC, 0xED, 0xEE):
                        out_bytes.append(ch)
                        k += 1
                        if k >= d_len:
                            break
                        next_ch_b = in_file.read(1)
                        if not next_ch_b:
                            sys.stderr.write("🗶 Sudden loss of data segments...\n")
                            break
                        out_bytes.append(next_ch_b[0])
                        k += 1
                        continue
                    if ch == ord('\r'):
                        out_bytes.append(ord('\n'))
                        k += 1
                        continue
                out_bytes.append(ch)
                k += 1

            try:
                with open(outfile, "wb") as f_out:
                    f_out.write(out_bytes)
            except Exception:
                sys.stderr.write(f"🗶 Cannot open file \"{outfile}\" for writing!\n")
                sys.exit(-1)

            print("✔ File unpacked successfully.")
    else:
        # --- PACK / CONVERT MODE ---
        out_stream = io.BytesIO()

        info_log("🛈 Step 1: vcp\n")
        xcpwrite(b"VCP.XDATA\x00", out_stream)

        info_log("🛈 Step 2: longnumber\n")
        xcpwriteHexLong(0x5f4d4353, out_stream)

        info_log("🛈 Step 3: folname_len\n")
        xcpwriteHexByte(folname_len, out_stream)

        info_log("🛈 Step 4: folname\n")
        folname_bytes = folname.encode('ascii') + b'\x00'
        xcpwrite(folname_bytes, out_stream)

        info_log("🛈 Step 5: varname_len\n")
        xcpwriteHexByte(varname_len, out_stream)

        info_log("🛈 Step 6: varname\n")
        varname_bytes = varname.encode('ascii') + b'\x00'
        xcpwrite(varname_bytes, out_stream)

        info_log("🛈 Step 7: block_31\n")
        xcpwriteHexLong(0x00000031, out_stream)

        info_log("🛈 Step 8: folname2\n")
        buf = bytearray(16)
        for idx in range(16):
            buf[idx] = ord(folname[idx]) if idx < (folname_len - 1) else 0xff
        xcpwrite(bytes(buf), out_stream)

        info_log("🛈 Step 9: varname2\n")
        buf = bytearray(16)
        for idx in range(16):
            buf[idx] = ord(varname[idx]) if idx < (varname_len - 1) else 0xff
        xcpwrite(bytes(buf), out_stream)

        info_log("🛈 Step 10: skip len1 (for now)\n")
        addr_len1 = out_stream.tell()
        out_stream.write(b'\x00\x00\x00\x00')

        info_log("🛈 Step 11: block_guq\n")
        guq_buf = b'GUQ' + b'\xff' * 10
        xcpwrite(guq_buf, out_stream)

        info_log("🛈 Step 12: skip len1asc (for now)\n")
        addr_len1asc = out_stream.tell()
        out_stream.write(b'\x00' * 8)

        info_log("🛈 Step 13: skip len2 (for now)\n")
        addr_len2 = out_stream.tell()
        out_stream.write(b'\x00' * len2_length)

        info_log("🛈 Step 14: block_zero\n")
        xcpwrite(b'\x00' * block_zero_length, out_stream)

        info_log("🛈 Step 15: copy the data\n")
        data_length = 0
        while True:
            ch_b = in_file.read(1)
            if not ch_b:
                break
            ch = ch_b[0]

            if chgnew:
                if ch in (0xEC, 0xED, 0xEE):
                    xcpputc(ch, out_stream)
                    data_length += 1

                    next_ch_b = in_file.read(1)
                    if not next_ch_b:
                        break
                    xcpputc(next_ch_b[0], out_stream)
                    data_length += 1
                    continue

                if ch == ord('\r'):
                    xcpputc(ord('\r'), out_stream)
                    data_length += 1
                    next_ch_b = in_file.read(1)
                    if not next_ch_b:
                        break
                    if next_ch_b[0] == ord('\n'):
                        continue
                    ch = next_ch_b[0]

                if ch == ord('\n'):
                    ch = ord('\r')

            xcpputc(ch, out_stream)
            data_length += 1

        info_log(f"🛈 Length of the content: {data_length}\n🛈 Length of input file: {in_file.tell()}\n")

        info_log("🛈 Step 16: eof\n")
        xcpwrite(b'\x00\xff', out_stream)

        info_log("🛈 Step 17: padding ")
        padding_length = (0 - (len2_length + block_zero_length + data_length + eof_length)) & 0x03
        pad_buf = bytes([padchar] * padding_length)
        xcpwrite(pad_buf, out_stream)
        info_log(f"(padding with {padding_length} bytes)\n")

        info_log("🛈 Now step 10: len1 ")
        out_stream.seek(addr_len1)
        len1 = len2_length + block_zero_length + data_length + eof_length + padding_length
        xcpwriteBinLong(len1, BIG_ENDIAN, out_stream)
        info_log(f"len1 is {len1}\n")

        info_log("🛈 Now step 12: len1asc\n")
        out_stream.seek(addr_len1asc)
        xcpwriteHexLong(len1, out_stream)

        info_log("🛈 Now step 13: len2\n")
        out_stream.seek(addr_len2)
        len2_val = data_length + 3
        xcpwriteBinLong(len2_val, LITTLE_ENDIAN, out_stream)

        info_log("🛈 Step 18: checksum\n")
        out_stream.seek(0, os.SEEK_END)
        xcpwriteHexByte(checksum, out_stream)

        info_log("🛈 Closing the files...\n")
        in_file.close()  # Handled safely at the exact lifecycle stage as C's fclose(in)
        try:
            with open(outfile, "wb") as f_out:
                f_out.write(out_stream.getvalue())
        except Exception:
            sys.stderr.write(f"🗶 Cannot open file \"{outfile}\" for writing!\n")
            sys.exit(-1)

        print("✔ File converted successfully.")

    return 0

if __name__ == '__main__':
    main()
