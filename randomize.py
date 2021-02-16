import os
import pathlib
import random
import shutil
import argparse
import datetime

def touchFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)


parser = argparse.ArgumentParser(description='Randomise the model of a Minecraft resource folder.')
parser.add_argument('-s', '--seed', default=int(datetime.datetime.timestamp(datetime.datetime.now())), type=int, dest='seed', help='specifies a random seed')
args = parser.parse_args()
randomseed = args.seed

random.seed(randomseed)

itempool = []
blockpool = []

itempoollist = ""
blockpoollist = ""

for path, folders, files in os.walk("assets"):
    #print(path,folders,files)
    for file in files:
        if str(file).endswith('.json'):
            if str(path).endswith('item'):
                itempool.append(file)
            if str(path).endswith('block'):
                blockpool.append(file)

itempoolwork = itempool.copy()
blockpoolwork = blockpool.copy()

random.shuffle(itempoolwork)
random.shuffle(blockpoolwork)

print("Item Model Pool :",len(itempool))
print("Block Model Pool :",len(blockpool))

shufflefolder = 'shuffled_' + str(randomseed) +'/'

touchFolder(shufflefolder)
touchFolder(shufflefolder+'assets/minecraft/')
pathlib.Path(shufflefolder+'assets/.mcassetsroot').touch()
touchFolder(shufflefolder+'assets/minecraft/')
touchFolder(shufflefolder+'assets/minecraft/models/')
touchFolder(shufflefolder+'assets/minecraft/models/item')
touchFolder(shufflefolder+'assets/minecraft/models/block')

for index,itemshuffle in enumerate(itempoolwork):
    shutil.copyfile("assets/minecraft/models/item/"+itempool[index], shufflefolder+'assets/minecraft/models/item/'+itemshuffle)
    shiftstr = itempool[index]+" -> "+itemshuffle
    print(shiftstr)
    itempoollist+=shiftstr+"\n"
for index,blockshuffle in enumerate(blockpoolwork):
    shutil.copyfile("assets/minecraft/models/block/"+blockpool[index], shufflefolder+'assets/minecraft/models/block/'+blockshuffle)
    shiftstr = blockpool[index]+" -> "+blockshuffle
    print(shiftstr)
    blockpoollist+=shiftstr+"\n"

with open(shufflefolder+'shuffledlist.txt','w') as fileopen:
    fileopen.write("\n\n\n-------------------------------------------------------------\nItem List : \n")
    fileopen.write(itempoollist)
    fileopen.write("\n\n\n-------------------------------------------------------------\nBlock List : \n")
    fileopen.write(blockpoollist)

with open(shufflefolder+'pack.mcmeta', "w") as descfile:
    descfile.write('{"pack":{"pack_format": 7,"description": "MC Resource Randomizer, Seed: '+str(randomseed)+'"}}')
try:
    shutil.make_archive('random_model_'+str(randomseed),'zip',shufflefolder)
    shutil.rmtree(shufflefolder)
except Exception as e:
    print("Comprecc Failed")
