from PIL import Image

def convert_to_bif(filename,mode,orig_algorithm,threshold,compressed,prebright,scale,verbose): # returns: image, file string, compression ratio/bloat (if applicable)
    image=Image.open(filename)
    if verbose:
        print("- Image \"" + filename + "\" opened successfully with dimensions " + str(image.size[0]) + "x" + str(image.size[1]) + "!")
    if scale!=1:
        image=image.resize(size=(int(image.size[0]*scale),int(image.size[1]*scale)))
        if verbose:
            print("- Image successfully scaled by " + str(scale) + "x. New resolution is " + str(image.size[0]) + "x" + str(image.size[1]) + ".")
    image_pixels=image.load()
    if verbose:
        print("- Image pixel map generated!")
    
    colours=get_colours(mode)

    if prebright!=0:
        for x in range(0,image.size[0]):
            for y in range(0,image.size[1]):
                orig_pixel=image_pixels[x,y]
                image_pixels[x,y]=(orig_pixel[0]+prebright,orig_pixel[1]+prebright,orig_pixel[2]+prebright)
        if verbose:
            print("- Image prebrighted by " + str(prebright) + "!")

    if verbose:
        if orig_algorithm:
            print("- Conversion started using original algorithm.")
        else:
            print("- Conversion started using euclidean distance algorithm.")
        
    for x in range(0,image.size[0]):
        for y in range(0,image.size[1]):
            orig_pixel=image_pixels[x,y]
            if isinstance(orig_pixel,tuple):
                if verbose:
                    print("- Quantizing pixel " + str(x) + ", " + str(y) + "...  ",end="\r")
                if orig_algorithm:
                    if mode==1:
                        if orig_pixel[0] - threshold > orig_pixel[1] and orig_pixel[0] - threshold > orig_pixel[2] or orig_pixel[0] - threshold < threshold or orig_pixel[1] - threshold < threshold or orig_pixel[2] - threshold < threshold:
                            image_pixels[x,y]=colours[0]
                            
                        elif orig_pixel[1] - threshold > orig_pixel[0] and orig_pixel[1] - threshold > orig_pixel[2]:
                            image_pixels[x,y]=colours[1]
                            
                        elif orig_pixel[2] - threshold > orig_pixel[1] and orig_pixel[2] - threshold > orig_pixel[0]:
                            image_pixels[x,y]=colours[2]
                            
                        else:
                            image_pixels[x,y]=colours[3]
                        
                    elif mode==2:
                        if orig_pixel[0] - threshold > orig_pixel[1] and orig_pixel[0] - threshold > orig_pixel[2]:
                            image_pixels[x,y]=colours[0]
                            
                        elif orig_pixel[1] - threshold > orig_pixel[0] and orig_pixel[1] - threshold > orig_pixel[2]:
                            image_pixels[x,y]=colours[1]
                            
                        elif orig_pixel[2] - threshold > orig_pixel[1] and orig_pixel[2] - threshold > orig_pixel[0]:
                            image_pixels[x,y]=colours[2]
                            
                        elif orig_pixel[0] - threshold < threshold or orig_pixel[1] - threshold < threshold or orig_pixel[2] - threshold < threshold:
                            image_pixels[x,y]=colours[3]
                            
                        else:
                            image_pixels[x,y]=colours[4]
                        
                    elif mode==3:
                        if orig_pixel[0] > threshold or orig_pixel[1] > threshold or orig_pixel[2] > threshold:
                            image_pixels[x,y]=colours[0]
                            
                        else:
                            image_pixels[x,y]=colours[1]
                                                
                else:
                    closest_diff=1000000 # any stupidly high number
                    for colour in colours:
                        red_diff=orig_pixel[0]-colour[0]
                        green_diff=orig_pixel[1]-colour[1]
                        blue_diff=orig_pixel[2]-colour[2]
                        overall_diff=red_diff*red_diff+green_diff*green_diff+blue_diff*blue_diff
                        if closest_diff>overall_diff:
                            closest_diff=overall_diff
                            image_pixels[x,y]=colour

    if verbose:
        print()
        print("- Image quantized!")
        
    original_string=""
    for y in range(0,image.size[1]):
        for x in range(0,image.size[0]):
            if verbose:
                print("- Adding pixel " + str(x) + ", " + str(y) + " to file...  ",end="\r")
            if isinstance(image_pixels[x,y],tuple):  
                orig_pixel=image_pixels[x,y]   
                if mode==1:
                    if orig_pixel[0]==colours[0][0] and orig_pixel[1]==colours[0][1] and orig_pixel[2]==colours[0][2]:
                        original_string+="1"
                    elif orig_pixel[0]==colours[1][0] and orig_pixel[1]==colours[1][1] and orig_pixel[2]==colours[1][2]:
                        original_string+="2"
                    elif orig_pixel[0]==colours[2][0] and orig_pixel[1]==colours[2][1] and orig_pixel[2]==colours[2][2]:
                        original_string+="3"
                    else:
                        original_string+="0"
                elif mode==2:
                    if orig_pixel[0]==colours[0][0] and orig_pixel[1]==colours[0][1] and orig_pixel[2]==colours[0][2]:
                        original_string+="1"
                    elif orig_pixel[0]==colours[1][0] and orig_pixel[1]==colours[1][1] and orig_pixel[2]==colours[1][2]:
                        original_string+="2"
                    elif orig_pixel[0]==colours[2][0] and orig_pixel[1]==colours[2][1] and orig_pixel[2]==colours[2][2]:
                        original_string+="3"
                    elif orig_pixel[0]==colours[3][0] and orig_pixel[1]==colours[3][1] and orig_pixel[2]==colours[3][2]:
                        original_string+="4"
                    else:
                        original_string+="0"
                elif mode==3:
                    if orig_pixel[0]==colours[0][0] and orig_pixel[1]==colours[0][1] and orig_pixel[2]==colours[0][2]:
                        original_string+="1"
                    else:
                        original_string+="0"
                elif mode==4 or mode==5:
                    if orig_pixel[0]==colours[0][0] and orig_pixel[1]==colours[0][1] and orig_pixel[2]==colours[0][2]:
                        original_string+="1"
                    elif orig_pixel[0]==colours[1][0] and orig_pixel[1]==colours[1][1] and orig_pixel[2]==colours[1][2]:
                        original_string+="2"
                    elif orig_pixel[0]==colours[2][0] and orig_pixel[1]==colours[2][1] and orig_pixel[2]==colours[2][2]:
                        original_string+="3"
                    elif orig_pixel[0]==colours[3][0] and orig_pixel[1]==colours[3][1] and orig_pixel[2]==colours[3][2]:
                        original_string+="4"
                    elif orig_pixel[0]==colours[4][0] and orig_pixel[1]==colours[4][1] and orig_pixel[2]==colours[4][2]:
                        original_string+="5"
                    elif orig_pixel[0]==colours[5][0] and orig_pixel[1]==colours[5][1] and orig_pixel[2]==colours[5][2]:
                        original_string+="6"
                    elif orig_pixel[0]==colours[6][0] and orig_pixel[1]==colours[6][1] and orig_pixel[2]==colours[6][2]:
                        original_string+="7"
                    else:
                        original_string+="0"

    if verbose:
        print()
        print("- File created!")

    ratio=0
    bloated=False
    file="BIF"
    if compressed:
        file+="C"
    file+=":W"+str(image.size[0])+":H"+str(image.size[1])+":M"+str(mode)+":D:"
    if compressed:
        if verbose:
            print()
            print("- Compressing file...")
        compressed_string=compress(original_string)
        file+=compressed_string
        if len(compressed_string)<len(original_string):
            ratio=round(100*(len(compressed_string)/len(original_string)),2)
        else:
            ratio=round(100*(len(original_string)/len(compressed_string)),2)
            bloated=True
        if verbose:
            if bloated:
                print("- Compression finished with a " + str(ratio) + "% increase in file size!")
            else:
                print("- Compression finished with a " + str(ratio) + "% reduction in file size!")
    else:
        if verbose:
            print("- Finishing file...")
        file+=original_string

    return {
        "file":file,
        "image":image,
        "ratio":ratio,
        "bloated":bloated
        }

def decompress(sections):
    decompressed_string=""

    for section in sections:
        if len(section)>0:
            data=section.split("-")
            if len(data)==2:
                data_value=data[0]
                data_amount=data[1]
                for a in range(0,int(data_amount)):
                    decompressed_string+=data_value
    return decompressed_string

def decompress_bif(string,verbose):
    sections=string.split(":")

    data_reached=False
    data_position=0
    compressed=False
    width=0
    height=0
    mode=0
    
    if verbose:
        print("- Parsing header...")
        
    for section in sections:
        if len(section)>0:
            if not data_reached:
                if section=="BIFC":
                    compressed=True
                if section[0]=="W":
                    width=int(section[1:])
                if section[0]=="H":
                    height=int(section[1:])
                if section[0]=="M":
                    mode=int(section[1:])
                if section[0]=="D":
                    data_reached=True
                data_position+=1
    
    if verbose:
        print("- Header successfully parsed!")
        print("    Width: " + str(width) + ", Height: " + str(width), "Mode " + str(mode), ", Compressed: " + str(compressed))

    decompressed_string=""
        
    if compressed:
        if verbose:
            print("- Decompressing file...")
        decompressed_string=decompress(sections)
    else:
        decompressed_string=string.split(":")[data_position]
    new_image=Image.new(mode="RGB",size=(width,height))
    colours=get_colours(mode)
    string_position=0
    for y in range(0,height):
        for x in range(0,width):
            colour_value=0
            if string_position<len(decompressed_string) and decompressed_string[string_position].isdigit():
                if verbose:
                    print("- Adding pixel " + str(x) + ", " + str(y) + " to image...  ",end="\r")
                colour_value=int(decompressed_string[string_position])
                colour=None
                if mode==1:
                    if colour_value==0:
                        colour=colours[3]
                    if colour_value==1:
                        colour=colours[0]
                    if colour_value==2:
                        colour=colours[1]
                    elif colour_value==3:
                        colour=colours[2]
                if mode==2:
                    if colour_value==0:
                        colour=colours[4]
                    if colour_value==1:
                        colour=colours[0]
                    if colour_value==2:
                        colour=colours[1]
                    elif colour_value==3:
                        colour=colours[2]
                    elif colour_value==4:
                        colour=colours[3]
                elif mode==3:
                    if colour_value==0:
                        colour=colours[1]
                    if colour_value==1:
                        colour=colours[0]
                elif mode==4 or mode==5:
                    if colour_value==0:
                        colour=colours[7]
                    if colour_value==1:
                        colour=colours[0]
                    if colour_value==2:
                        colour=colours[1]
                    elif colour_value==3:
                        colour=colours[2]
                    elif colour_value==4:
                        colour=colours[3]
                    elif colour_value==5:
                        colour=colours[4]
                    elif colour_value==6:
                        colour=colours[5]
                    elif colour_value==7:
                        colour=colours[6]
                new_image.putpixel((x,y),colour)
                string_position+=1
                
    if verbose:
        print()
        print("- Image created!")

    bloated=False
    ratio=0
    ratio_raw=round(100*(len(string)/len(decompressed_string)),2)
    if compressed:
        if len(string)<len(decompressed_string):
            ratio=round(100*(len(string)/len(decompressed_string)),2)
        else:
            ratio=round(100*(len(decompressed_string)/len(string)),2)
            bloated=True

    # compressed is if the image was previously compressed
    return {
        "image":new_image,
        "compressed":compressed,
        "ratio":ratio,
        "ratio_raw":ratio_raw,
        "bloated":bloated,
        "mode":mode
        }

def compress(string):
    compressed_string=""
    last_char=""
    counter=1
    for a in range(0,len(string)):
        if last_char==string[a]:
            counter+=1
        else:
            if a>0:
                compressed_string+=last_char+"-"+str(counter)+":"
            counter=1
        last_char=string[a]
    compressed_string+=last_char+"-"+str(counter)+":"
    return compressed_string

def get_mode_description(mode):
    if mode==1:
        return "Mode 1 (red, green, blue and white)"
    elif mode==2:
        return "Mode 2 (cyan, magenta, yellow, black and white)"
    elif mode==3:
        return "Mode 3 (black and white)"
    elif mode==4:
        return "Mode 4 (8 step greyscale)"
    elif mode==5:
        return "Mode 5 (Mode 1 + Mode 2)"
    else:
        return "Mode " + str(mode) + " (unknown)"

def get_colours(mode):
    if mode==1:
        return(
            (255,0,0),
            (0,255,0),
            (0,0,255),
            (255,255,255)
            )
    elif mode==2:
        return(
            (255,0,255),
            (255,255,0),
            (0,255,255),
            (0,0,0),
            (255,255,255)
            )
    elif mode==3:
        return(
            (255,255,255),
            (0,0,0)
            )
    elif mode==4:
        return(
            (0,0,0),
            (36,36,36),
            (73,73,73),
            (109,109,109),
            (146,146,146),
            (182,182,182),
            (219,219,219),
            (255,255,255)
            )
    elif mode==5:
        return(
            (255,0,0),
            (0,255,0),
            (0,0,255),
            (255,0,255),
            (255,255,0),
            (0,255,255),
            (0,0,0),
            (255,255,255)
            )
    else:
        return None
