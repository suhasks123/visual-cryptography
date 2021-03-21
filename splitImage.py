from PIL import Image

import random
import sys


# img = Image.open(sys.argv[1])
img = Image.open("./testImages/pigtrial.png")
img = image.convert('1')

split1 = Image.new("1", [dimension * 2 for dimension in img.size])

split2 = Image.new("1", [dimension * 2 for dimension in img.size])

for x in range(0, img.size[0], 2):
    for y in range(0, img.size[1], 2):
        sourcepixel = img.getpixel((x, y))
        assert sourcepixel in (0, 255)
        coinflip = random.random()
        if sourcepixel == 0:
            if coinflip < .5:
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
        elif sourcepixel == 255:
            if coinflip < .5:
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

split1.save('testImages/part1.jpg')
split2.save('testImages/part2.jpg')