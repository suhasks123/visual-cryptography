from PIL import Image

import random
import sys

img = Image.open(sys.argv[1])
# img = Image.open("./testImages/pigtrial.png")
img = image.convert('1') # Convert to 1 bit pixel

# Expand both images to 4 times the input image size, doubling each dimension
split1 = Image.new("1", [dims * 2 for dims in img.size]) 

split2 = Image.new("1", [dims * 2 for dims in img.size])

# Iterate through input pixels and split as diagonal shares
for x in range(0, img.size[0], 2):
    for y in range(0, img.size[1], 2):
        input_pix = img.getpixel((x, y))
        assert input_pix in (0, 255)
        random_val = random.random()
        if input_pix == 0: # Black pixel, both splits have complimentary diagonal subpixel pattern
            if random_val < .5:
                split1.putpixel((x * 2, y * 2), 255)
                split1.putpixel((x * 2 + 1, y * 2), 0)
                split1.putpixel((x * 2, y * 2 + 1), 0)
                split1.putpixel((x * 2 + 1, y * 2 + 1), 255)
                
                split2.putpixel((x * 2, y * 2), 0)
                split2.putpixel((x * 2 + 1, y * 2), 255)
                split2.putpixel((x * 2, y * 2 + 1), 255)
                split2.putpixel((x * 2 + 1, y * 2 + 1), 0)
            else:
                split1.putpixel((x * 2, y * 2), 0)
                split1.putpixel((x * 2 + 1, y * 2), 255)
                split1.putpixel((x * 2, y * 2 + 1), 255)
                split1.putpixel((x * 2 + 1, y * 2 + 1), 0)
                
                split2.putpixel((x * 2, y * 2), 255)
                split2.putpixel((x * 2 + 1, y * 2), 0)
                split2.putpixel((x * 2, y * 2 + 1), 0)
                split2.putpixel((x * 2 + 1, y * 2 + 1), 255)
        elif input_pix == 255: # White pixel, both splits have same diagonal subpixel pattern
            if random_val < .5:
                split1.putpixel((x * 2, y * 2), 255)
                split1.putpixel((x * 2 + 1, y * 2), 0)
                split1.putpixel((x * 2, y * 2 + 1), 0)
                split1.putpixel((x * 2 + 1, y * 2 + 1), 255)
                
                split2.putpixel((x * 2, y * 2), 255)
                split2.putpixel((x * 2 + 1, y * 2), 0)
                split2.putpixel((x * 2, y * 2 + 1), 0)
                split2.putpixel((x * 2 + 1, y * 2 + 1), 255)
            else:
                split1.putpixel((x * 2, y * 2), 0)
                split1.putpixel((x * 2 + 1, y * 2), 255)
                split1.putpixel((x * 2, y * 2 + 1), 255)
                split1.putpixel((x * 2 + 1, y * 2 + 1), 0)
                
                split2.putpixel((x * 2, y * 2), 0)
                split2.putpixel((x * 2 + 1, y * 2), 255)
                split2.putpixel((x * 2, y * 2 + 1), 255)
                split2.putpixel((x * 2 + 1, y * 2 + 1), 0)

# Save output images
split1.save('testImages/part1.jpg')
split2.save('testImages/part2.jpg')