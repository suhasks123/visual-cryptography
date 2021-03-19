from PIL import Image
import sys
import account

def combine2Images(f1, f2):

    # Two input images
    infile1 = Image.open(f1)
    infile2 = Image.open(f2)

    outfile = Image.new('1', infile1.size)

    # Combine images
    for x in range(infile1.size[0]):
        for y in range(infile1.size[1]):
            outfile.putpixel((x, y), min(infile1.getpixel((x, y)), infile2.getpixel((x, y))))

    # Return / Save outfile
    outfile.save("testImages/combined.png")
    return outfile

if __name__=="__main__": 

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]

    combine2Images(filename1, filename2)

    print("Combining done")
