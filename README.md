# BIF.py
For those uninitiated, Best Image Format is the greatest image format in the world. I developed it back in 2021 as a simple Visual Basic application, and it became the most popular image format by the end of the year, with about 5 different people using it. It supports 5 different colour modes, so you can fine tune your result to be personal to you. For compression, it uses the BCA which is a lossless, string-based compression "algorithm". It's unique in that it can actually bloat the file by up to 50%, especially if there are loads of unique pixels.

It's had such a legacy, and it's so beautiful that I had to rewrite it, making it easier to maintain and update with new features. Believe it or not, this Python rewrite is actually faster than the Visual Basic version by at least 2x on my computer! Writing it in Python also means that both the BIF and BCA are modular, so can be used in other Python programs (if you'd really want to do that). It's also cross-platform because of this!

The Pillow library is absolutely required for this to work. It also uses Argparse for the command line programs, and TkInter for the GUI.

## Format Pacifics
BIF files are pretty simple. Here's an example file:
```
BIFC:W128:H128:M2:D:0-4150:4-1: etc…
```
It’s comprised of 2 sections: the header, and the uncompressed/compressed image data. The first section of the header is the "format string" and can be either "BIF" or "BIFC", which decide whether the file is compressed or not. Then, "W" and "H" determine the width and height of the image in pixels. "M" determines the colour mode used by the image, which are as follows:
1. Red, green, blue and white
2. Cyan, magenta, yellow, black and white
3. Black and white
4. 8-step greyscale
5. Mode 1 + Mode 2

"D" denotes the start of image data. When a file is being parsed, the kind of data to parse is determined by the format string. So if it was a compressed file, it would expect to look for BCA data. If the format string and image data are mismatched, it will return an error when parsing. The same goes for a mismatched width and height, which also returns an error instead of drawing the incorrect image. A BIF file always ends with a colon.

## Bloated Compression Algorithm (BCA)
This algorithm works by using strings, which results in compression taking an extremely long time. It's basically a very bloated version of run-length encoding that uses plain text instead of bytes, and was programmed before I even knew it existed.

The format of the BCA consists of text that's formatted in a similar way to header data for BIF images. After parsing the BIF header, we reach a pair of numbers: the first number of the pair which represents the colour of the current pixel (depending on the colour format specified upon conversion), followed by a hyphen, then a number which represents the amount of times this pixel appears. 2 different variables are set accordingly.

When parsing a BCA compressed string, it constantly adds the appropriate pixel to an Image stored in memory. As they’re being added, a counter is increased until it reaches the right amount, at which point, the next "byte" is parsed, which is found by searching for a colon, which is also how the file ends. Once the end of the file is reached, the image is then saved or previewed.

An example of a BCA compressed string is as follows:
```
0-40:3-20:
```
This means 40 instances of colour 0, and 20 instances of colour 3.

## Shaht Ahuts
Shout out to my Computer Science teacher for appreciating what a bold move it is to make an image format from scratch, Bayleaf Pacific for loving the BIF aesthetic,  referencing it frequently and creating the BIF.py logo, and RryRry Ryeball for testing it out on his beefy desktop computer and HP laptop (which is similar to mine specs-wise), and encouraging me to keep it at its "slow single-threaded glory". Shout outs to everyone I mentioned and forgot to mention for finding it so funny!
