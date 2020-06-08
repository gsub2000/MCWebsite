from flask import Flask, request, send_file, render_template
from mcpi.minecraft import Minecraft
from mcpi import block
from PIL import Image
import math
import urllib.request
import pyautogui
import autopy
import time

app = Flask(__name__, static_url_path='', static_folder="static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#this is the function that gets the home page
@app.route('/')
def root():
    return app.send_static_file("index.html")

#clears saved images
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

#takes screenshot
@app.route('/', methods=['POST'])
def handle_data():
    test = request.form['url']
    plyr = request.form['player']
    # checkImage(test, plyr)
    screenshot = pyautogui.screenshot()
    width, height = screenshot.size
    new_size = 800, math.floor(height * (800 / width))
    screenshot = screenshot.resize(new_size, Image.ANTIALIAS)
    screenshot.save('static/test.png')
    return send_file('static/index2.html', cache_timeout=0)


minecraftBlocks = (
    ("Air", 0, ((0, 136, 255),), 0),
    ("Smooth Stone", 1, ((125, 125, 125),), 0),
    ("Dirt", 3, ((133, 96, 66),), 0),
    ("Cobblestone", 4, ((117, 117, 117),), 0),
    ("Wooden Plank", 5, ((156, 127, 78),), 0),
    ("Bedrock", 7, ((83, 83, 83),), 0),
    ("Sand", 12, ((217, 210, 158),), 0),
    ("Gravel", 13, ((136, 126, 125),), 0),
    ("Gold Ore", 14, ((143, 139, 124),), 0),
    ("Iron Ore", 15, ((135, 130, 126),), 0),
    ("Coal Ore", 16, ((115, 115, 115),), 0),
    ("Wood", 17, ((154, 125, 77),), 0),
    ("Sponge", 19, ((182, 182, 57),), 0),
    ("White Wool", 35, ((221, 221, 221),), 0),
    ("Orange Wool", 35, ((233, 126, 55),), 1),
    ("Magenta Wool", 35, ((179, 75, 200),), 2),
    ("Light Blue Wool", 35, ((103, 137, 211),), 3),
    ("Yellow Wool", 35, ((192, 179, 28),), 4),
    ("Light Green Wool", 35, ((59, 187, 47),), 5),
    ("Pink Wool", 35, ((217, 132, 153),), 6),
    ("Dark Gray Wool", 35, ((66, 67, 67),), 7),
    ("Gray Wool", 35, ((157, 164, 165),), 8),
    ("Cyan Wool", 35, ((39, 116, 148),), 9),
    ("Purple Wool", 35, ((128, 53, 195),), 10),
    ("Blue Wool", 35, ((39, 51, 153),), 11),
    ("Brown Wool", 35, ((85, 51, 27),), 12),
    ("Dark Green Wool", 35, ((55, 76, 24),), 13),
    ("Red Wool", 35, ((162, 44, 42),), 14),
    ("Black Wool", 35, ((26, 23, 23),), 15),
    ("Gold", 41, ((249, 236, 77),), 0),
    ("Iron", 42, ((230, 230, 230),), 0),
    ("TwoHalves", 43, ((159, 159, 159),), 0),
    ("Brick", 45, ((155, 110, 97),), 0),
    ("Mossy Cobblestone", 48, ((90, 108, 90),), 0),
    ("Obsidian", 49, ((20, 18, 29),), 0),
    ("Diamond Ore", 56, ((129, 140, 143),), 0),
    ("Diamond Block", 57, ((99, 219, 213),), 0),
    ("Workbench", 58, ((107, 71, 42),), 0),
    ("Redstone Ore", 73, ((132, 107, 107),), 0),
    ("Snow Block", 80, ((239, 251, 251),), 0),
    ("Clay", 82, ((158, 164, 176),), 0),
    ("Jukebox", 84, ((107, 73, 55),), 0),
    ("Pumpkin", 86, ((192, 118, 21),), 0),
    ("Netherrack", 87, ((110, 53, 51),), 0),
    ("Soul Sand", 88, ((84, 64, 51),), 0),
    ("Glowstone", 89, ((137, 112, 64),), 0)
)


def checkColor(colorRGB, blockRGB):
    return math.sqrt(math.pow(colorRGB[0] - blockRGB[0], 2) + math.pow(colorRGB[1] - blockRGB[1], 2) + math.pow(
        colorRGB[2] - blockRGB[2], 2))


def getBlockFromColor(colorRGB):
    smallestIndex = -1
    smallestColorDiff = 50000
    currentIndex = 0
    for block in minecraftBlocks:
        for blockcolor in block[2]:
            temp = checkColor(colorRGB, blockcolor)

            if (temp < smallestColorDiff):
                smallestColorDiff = temp
                smallestIndex = currentIndex

        currentIndex = currentIndex + 1

    return minecraftBlocks[smallestIndex]


def checkImage(imgUrl, player):
    if imageColor(imgUrl):
        mc = Minecraft.create("13.57.251.20", 4711)
        playerId = mc.getPlayerEntityId(player)
        time.sleep(5)
        img = Image.open(urllib.request.urlopen(imgUrl))
        width, height = img.size
        new_size = 75, math.floor(height * (75 / width))
        img = img.resize(new_size, Image.ANTIALIAS)
        pos = mc.entity.getPos(playerId)
        for r in range(new_size[0]):
            for c in range(new_size[1]):
                cord = (r, c)
                try:
                    pixelColor = img.getpixel(cord)
                    mc_block = getBlockFromColor(pixelColor)
                    mc.setBlock(pos.x + r, pos.y+30 - c, pos.z + 50, mc_block[1], mc_block[3])
                except:
                    continue

        # mc.entity.setPos(playerId, (pos.x + 10, pos.y - 10, pos.z - 20))
        for i in range(15, 1, -1):
            time.sleep(1)
            print("Time left before screenshot: " + str(i))
        # screenshot = pyautogui.screenshot()
        # width, height = screenshot.size
        # new_size = 800, math.floor(height * (800 / width))
        # screenshot = screenshot.resize(new_size, Image.ANTIALIAS)
        # screenshot.save('static/test.png')




def imageColor(imgUrl):
    try:
        img = Image.open(urllib.request.urlopen(imgUrl))
        return len(img.getpixel((20, 20))) == 3
    except:
        return False


app.run(host="127.0.0.1", port="80")
