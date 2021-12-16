## Imports
import os
import datetime


## User Variables (userPath is '/home/user/', both paths can be changed)
userPath = os.path.abspath(__file__)[ : os.path.abspath(__file__).find('/', 6)+1]
wallpapersDir           = userPath + 'Pictures/BingWallpaper/' # directory to save wallpapers in
nitrogenConfigFile      = userPath + '.config/nitrogen/bg-saved.cfg'

wgetQuiet               = True # set to true to get no output by wget


## Variable Definitions
fileDir = os.path.abspath(__file__).strip('BingWallpaperSetter.py')
lastWallpaperFilename   = 'lastWallpaper.txt' 

bingStartpage   = 'https://www.bing.com'
htmlTag         = ['<link rel="preload" href="', '" as="image" id="preloadBg"  />']

date            = datetime.datetime.now()

if wgetQuiet:
    wgetOptions = '--quiet '
else:
    wgetOptions = ''


## Main Program
# delete old index.html document of the bing startpage and get the new
os.system('rm ' + fileDir + 'index.html')
os.system('wget ' + wgetOptions + '-O ' + fileDir + 'index.html ' + bingStartpage)

# read index.html
file = open(fileDir + 'index.html', 'r')
line = file.readline()
file.close

# find start and end of wallpaper link
startLink   = line.find(htmlTag[0])+len(htmlTag[0])
endLink     = line.find(htmlTag[1], startLink)

linkWallpaper = bingStartpage + line[startLink:endLink]

# check if lastWallpaper.txt exists, if not create it
if not os.path.isfile(fileDir + lastWallpaperFilename):
    open(fileDir + lastWallpaperFilename, 'w').close()

# check which wallpaper was downloaded last
lastWallpaperFile = open(fileDir + lastWallpaperFilename, 'r')
lastLinkWallpaper = lastWallpaperFile.read() 
lastWallpaperFile.close()

# set name of wallpaper
nameWallpaper = str(date.year) + str(date.month) + str(date.day) + "_"
nameWallpaper += linkWallpaper[linkWallpaper.find('OHR.')+len('OHR.'):linkWallpaper.find('_DE')] + '_1920x1080.jpg'
pathWallpaper = wallpapersDir + nameWallpaper

# if the last wallpaper is not the same as the most recent,
# download it, write to the file and set it as new wallpaper
# set name of wallpaper
if lastLinkWallpaper != linkWallpaper:
    # save wallpaper
    os.system('wget ' + wgetOptions + '-O ' + pathWallpaper + ' ' + linkWallpaper)
    
    # write which wallpaper is the last downloaded
    lastWallpaperFile = open(fileDir + lastWallpaperFilename, 'w')
    lastLinkWallpaper = lastWallpaperFile.write(linkWallpaper)
    lastWallpaperFile.close()


# set wallpaper
nitrogenConfig = open(nitrogenConfigFile, 'r')
nitrogenFile   = nitrogenConfig.readlines()
nitrogenConfig.close()

for i in range(len(nitrogenFile)):
    if nitrogenFile[i][:5] == 'file=':
        nitrogenFile[i] = 'file=' + pathWallpaper + '\n'

nitrogenConfig = open(nitrogenConfigFile, 'w')
nitrogenConfig.writelines(nitrogenFile)
nitrogenConfig.close()

os.system('nitrogen --restore')
os.system('nitrogen --restore') # sometimes it takes two calls to restore the wallpaper
