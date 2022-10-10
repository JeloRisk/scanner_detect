# Import Module
from PIL import Image
import cv2
import turtle
import colorsys
def most_common_used_color(img):
    # Get width and height of Image
    width, height = img.size
 
    # Initialize Variable
    r_total = 0
    g_total = 0
    b_total = 0
 
    count = 0
 
    # Iterate through each pixel
    for x in range(0, width):
        for y in range(0, height):
            # r,g,b value of pixel
            r, g, b = img.getpixel((x, y))
 
            r_total += r
            g_total += g
            b_total += b
            count += 1
 
    return (r_total/count, g_total/count, b_total/count)
 
# Read Image
img_ce = r"scanner_detect/output/document.jpg"
img = Image.open(img_ce)
img2 = cv2.imread(img_ce)
# Convert Image into RGB
img = img.convert('RGB')
 
# call function
common_color = most_common_used_color(img)


# cv2.imshow("2",img2)
print("Intial Result: "+str(common_color))
print("RGB: " + str(tuple(int(x) for x in common_color)))
hex ='#%02x%02x%02x' % tuple(int(x) for x in common_color)
print("HEX: " + str(hex))
(r,g,b) = (190, 154, 88)
(h, s, v) = colorsys.rgb_to_hsv(r, g, b)
print('HSV : ', h, s, v)


img22 = Image.new("RGB", (100,100), hex)

from math import sqrt

# COLORS = (
#     (164, 147, 98), #rock
#     (115, 163, 176) #blue
# )
COLORS =[
    {'type': 'fire',
     'color': (198, 142, 96)},
    {'type': 'water',
     'color': (115, 163, 176)},
    {'type': 'grass',
     'color': (157, 172, 93)},
    {'type': 'electric',
     'color': (208, 205, 116)},
    {'type': 'psychic',
     'color': (192, 176, 177)},
]

def closest_color(type,rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color['color']
        color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        
        color_diffs.append((color_diff, color['color']))
        m = min(color_diffs)[1] 
        # print((color_diffs)) 
    for color in COLORS:
        if color["color"] == m:
            if type == "t":
                return color["type"]
            elif type == "rgb":
                return color["color"]

type = closest_color("t",common_color)
print("Prefer Type: "  +str(type))
color = closest_color("rgb",common_color)
print("Closest Color: "  +str(color))
# => (99, 23, 153)



# img22.show()


cv2.waitKey(0)
# Output is (R, G, B)