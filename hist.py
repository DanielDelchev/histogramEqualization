from PIL import Image
from matplotlib import pyplot
import argparse

if __name__ == '__main__':

    default_input_filename = 'gray.jpg'
    default_output_filename = 'result.jpg'
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str, help="The name of the JPEG file to manipulate", nargs='?')
    parser.add_argument('output_filename', type=str, help="The name of the result JPEG file to create", nargs='?')
    args = parser.parse_args()
    
    if (args.input_filename != None):
        image = Image.open(args.input_filename)
    else:
        image = Image.open(default_input_filename)
        
    pixels = list(image.getdata()) 
    
    frequency = [0]*256
    CDF = [0]*256
    
    '''grayscale image R=G=B'''
    for RGB_triple in pixels:
        frequency[RGB_triple[0]] += 1
    
    CDF[0] = frequency[0]
    for i in range(1,255):
        CDF[i] = CDF[i-1] + frequency[i]   
    
    M = len(pixels) - 1
    L = 256
    CDFmin = min([x for x in CDF if x > 0])
    
    new_pixels = []
    for RGB_triple in pixels:
        hv = round((CDF[RGB_triple[0]]-CDFmin)*(L-1)/M)
        new_pixels.append(tuple([hv]*3))
        
    new_image = Image.new('RGB', (image.size[0], image.size[1]))
    new_image.putdata(new_pixels)
    
    if (args.input_filename != None):
        new_image.save(args.output_filename, 'JPEG')
    else:
        new_image.save(default_output_filename, 'JPEG')