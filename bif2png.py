import argparse
import os
import time
import bif
from PIL import Image

parser = argparse.ArgumentParser(description="Converts a BIF image to PNG.")
parser.add_argument("input_file", type=argparse.FileType("r"), help="The name of the file to be converted.")
parser.add_argument("output_file", type=argparse.FileType("w"), help="The name of the converted file.")
parser.add_argument("--verbose", "-v", action="store_true", help="Shows the conversion process. Conversion will be a lot slower if this is enabled.",default=False)

args=parser.parse_args()

input_extension=".".join(args.input_file.name.split(".")[-1:]).lower()
output_extension=".".join(args.output_file.name.split(".")[-1:]).lower()
if input_extension=="bif":
    if output_extension=="png":
        start_time=time.time()
        if args.verbose:
            print("Conversion started: " + time.strftime("%D %H:%M:%S",time.gmtime(start_time)) + "...")
        with open(args.input_file.name) as file:
            image=bif.decompress_bif(file.readline(),args.verbose)
        image["image"].save(args.output_file.name)
        end_time=time.time()
        if args.verbose:
            print("Conversion completed in " + str(round(end_time-start_time,2)) + " seconds!")
            print("File saved to " + args.output_file.name + ".")
else:
    raise argparse.ArgumentTypeError("Input file not a BIF!")
