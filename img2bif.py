import argparse
import os
import time
import bif

parser = argparse.ArgumentParser(description="Converts an image to BIF.")
parser.add_argument("input_file", type=argparse.FileType("r"), help="The name of the file to be converted.")
parser.add_argument("output_file", type=argparse.FileType("w"), help="The name of the converted file.")
parser.add_argument("mode", type=int, help="The graphics mode to use. 1 = red, green, blue and white, 2 = cyan, magenta, yellow, black and white, 3 = black and white, 4 = 8 stage greyscale",choices=[1,2,3,4,5])
parser.add_argument("--compressed", "-c", action="store_true", help="Compresses the file using the BCA.",default=False)
parser.add_argument("--prebright", "-b", type=int, help="Brightens or darkens the image before conversion.",default=0)
parser.add_argument("--original", "-o", action="store_true", help="Uses the original colour reduction algorithm.",default=False)
parser.add_argument("--threshold", "-t", type=int, help="Sets the threshold when using the original algorithm. If not using the original algorithm, this will be ignored.",default=0)
parser.add_argument("--scale", "-s", type=float, help="Makes the image bigger or smaller before conversion. 1 is the original size, 2 is double the size, and 0.5 is half the size.",default=1.0)
parser.add_argument("--verbose", "-v", action="store_true", help="Shows the conversion process. Conversion will be a lot slower if this is enabled.",default=False)

args=parser.parse_args()
output_extension=".".join(args.output_file.name.split(".")[-1:]).lower()

if output_extension=="bif":
    if args.scale>=0.125 and args.scale<=1:
        start_time=time.time()
        if args.verbose:
            print("Conversion started: " + time.strftime("%D %H:%M:%S",time.gmtime(start_time)) + "...")
        bif_file=bif.convert_to_bif(args.input_file.name,args.mode,args.original,args.threshold,args.compressed,args.prebright,args.scale,args.verbose)
        with open(args.output_file.name, "w") as file:
            file.write(bif_file["file"])
        end_time=time.time()
        if args.verbose:
            print("Conversion completed in " + str(round(end_time-start_time,2)) + " seconds!")
            print("File saved to " + args.output_file.name + ".")
    else:
            raise argparse.ArgumentTypeError("Scale must be between 0.125 and 1")
else:
    raise argparse.ArgumentTypeError("Output file not a BIF!")
