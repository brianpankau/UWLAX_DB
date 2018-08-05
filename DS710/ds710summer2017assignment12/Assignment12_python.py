# -*- coding: utf-8 -*-

# Author: Brian Pankau
# Class: DS710 Summer 2017
# Assignment: Python 12


# import libraries
import json
import os
import sys
import binascii
import unicodedata
import string

# set working directory
os.chdir('C:\_DS710\Temp12')

# Problem 1a
# --------------------------------------------------------------------
# specify json card data
# change attribute name to artist to support DTK card schema
sen_triplets_card = """{
    "artist" : "Sen Triplets",
    "manaCost" : "{2}{W}{U}{B}",
    "cmc" : 5,
    "colors" : ["White", "Blue", "Black"],

    "type" : "Legendary Artifact Creature — Human Wizard",
    "supertypes" : ["Legendary"],
    "types" : ["Artifact", "Creature"],
    "subtypes" : ["Human", "Wizard"],

    "rarity" : "Mythic Rare",

    "text" : "At the beginning of your upkeep, choose target opponent. This turn, that player can't cast spells or activate abilities and plays with his or her hand revealed. You may play cards from that player's hand this turn.",

    "flavor" : "They are the masters of your mind.",

    "artist" : "Greg Staples",
    "number" : "109",

    "power" : "3",
    "toughness" : "3",

    "layout" : "normal",
    "multiverseid" : 180607,
    "imageName" : "sen triplets",
    "id" : "3129aee7f26a4282ce131db7d417b1bc3338c4d4"
}"""

# test with the first DTK card
card1 = """{
    "artist": "Cliff Childs",
    "cmc": 6,
    "flavor": "For hundreds of years Ugin slept, encased in the cocoon of stone and magic Sarkhan had created using a shard of a Zendikari hedron. As Ugin lay dormant, his spectral guardians kept vigil.",
    "id": "865ee3504233dfecb1cdd716e298913727032fd7",
    "imageName": "scion of ugin",
    "layout": "normal",
    "manaCost": "{6}",
    "mciNumber": "1",
    "multiverseid": 394681,
    "name": "Scion of Ugin",
    "number": "1",
    "power": "4",
    "rarity": "Uncommon",
    "subtypes": ["Dragon","Spirit"],
    "text": "Flying",
    "toughness": "4",
    "type": "Creature — Dragon Spirit",
    "types": ["Creature"]
}"""

# define MagicCard class attributes & methods
# change attribute name to artist to support DTK card schema
class MagicCard(object):
    def __init__(self, artist=None, colors=[], rarity=None):
        self.__artist = artist
        self.__colors = colors
        self.__rarity = rarity
    def set_artist(self, artist):
        self.__artist = artist
    def get_artist(self):
        return self.__artist
    def set_colors(self, colors):
        self.__colors = colors
    def get_colors(self):
        return self.__colors
    def set_rarity(self, rarity):
        self.__rarity = rarity
    def get_rarity(self):
        return self.__rarity

# convert the json data in to a python representation and store in a temporary dictionary
cdict = json.loads(sen_triplets_card)
adict = json.loads(card1)


# create an instance of MagicCard and populate it with dict values for the keys artist, colors, rarity
sen_triplets = MagicCard(cdict.get('artist'), cdict.get('colors'), cdict.get('rarity'))

# verify that DTK cards can be instanced
card_1 = MagicCard(adict.get('artist'), adict.get('colors'), adict.get('rarity'))

# verify the instance's attributes
print("sen triplets artist = ", sen_triplets.get_artist())
print("sen triplets colors = ", sen_triplets.get_colors())
print("sen triplets rarity = ", sen_triplets.get_rarity())
print("")

# verify DTK card instance
print("card_1 artist = ", card_1.get_artist())
print("card_1 colors = ", card_1.get_colors())
print("card_1 rarity = ", card_1.get_rarity())


# Problem 1b
# --------------------------------------------------------------------
'''
# define a small DTK json set for testing
dtk_cards_test = """{
  "name": "Dragons of Tarkir",
  "cards": [
    {
      "artist": "Cliff Childs",
      "cmc": 6,
      "flavor": "For hundreds of years Ugin slept, encased in the cocoon of stone and magic Sarkhan had created using a shard of a Zendikari hedron. As Ugin lay dormant, his spectral guardians kept vigil.",
      "id": "865ee3504233dfecb1cdd716e298913727032fd7",
      "imageName": "scion of ugin",
      "layout": "normal",
      "manaCost": "{6}",
      "mciNumber": "1",
      "multiverseid": 394681,
      "name": "Scion of Ugin",
      "number": "1",
      "power": "4",
      "rarity": "Uncommon",
      "subtypes": ["Dragon","Spirit"],
      "text": "Flying",
      "toughness": "4",
      "type": "Creature — Dragon Spirit",
      "types": ["Creature"]
    },
    {
      "artist": "Ryan Yee",
      "cmc": 2,
      "colorIdentity": ["W"],
      "colors": ["White"],
      "flavor": "Martyred for worshipping her ancestors, she now walks among them.",
      "id": "c79ecbe728fb34a5c11bb46ec2a17d6944032800",
      "imageName": "anafenza, kin-tree spirit",
      "layout": "normal",
      "manaCost": "{W}{W}",
      "mciNumber": "2",
      "multiverseid": 394490,
      "name": "Anafenza, Kin-Tree Spirit",
      "number": "2",
      "power": "2",
      "rarity": "Rare",
      "subtypes": ["Spirit","Soldier"],
      "supertypes": ["Legendary"],
      "text": "Whenever another nontoken creature enters the battlefield under your control, bolster 1. (Choose a creature with the least toughness among creatures you control and put a +1/+1 counter on it.)",
      "toughness": "2",
      "type": "Legendary Creature — Spirit Soldier",
      "types": ["Creature"],
      "watermark": "Dromoka"
    },
    {
      "artist": "David Palumbo",
      "cmc": 3,
      "colorIdentity": ["W"],
      "colors": ["White"],
      "flavor": "I would gladly give my life if it would inspire my clan to victory.",
      "id": "50bb32432fbf5571494fee5a18effcec85b70ece",
      "imageName": "arashin foremost",
      "layout": "normal",
      "manaCost": "{1}{W}{W}",
      "mciNumber": "3",
      "multiverseid": 394494,
      "name": "Arashin Foremost",
      "number": "3",
      "power": "2",
      "rarity": "Rare",
      "subtypes": ["Human","Warrior"],
      "text": "Double strike\\nWhenever Arashin Foremost enters the battlefield or attacks, another target Warrior creature you control gains double strike until end of turn.",
      "toughness": "2",
      "type": "Creature — Human Warrior",
      "types": ["Creature"],
      "watermark": "Dromoka"
    }
    ]
}"""
'''

# set file names
parse_input_fn0    = "DTK.json"
parse_output_fn0   = "DTK_clean.json"

# convert input source from unknown encoding into ascii, remove non-printable characters
# manually replace '\n' with '\\n', delete and occurrance of '\"' from DTK.json source
f2 = open(parse_output_fn0, 'w', encoding='utf-8', errors="ignore")
with open(parse_input_fn0, 'r', encoding="utf-8", errors="ignore") as f1:
    for aline in iter(f1.readline, ""):
        #strip special characters from file
        printable = set(string.printable)
        aline_str = '' .join(filter(lambda x: x in string.printable, aline))
        # write the processed line to a file
        f2.write(aline_str)
f2.close()
f1.close()

# read the DTK json file
with open(parse_output_fn0) as f:
  dtk_data = f.read()
f.close()

# convert the json data in to a python representation and store in a temporary dictionary
cdict = json.loads(dtk_data)
# debug
#cdict = json.loads(dtk_cards_test)

        
# define class to create MTG instances
def cardInstances(cards):
    MCinstanceList = []
    while (len(cards) != 0):
        l = cards.pop()
        MCinstanceList.append(MagicCard(l.get('artist'), l.get('colors'), l.get('rarity')))
    return (MCinstanceList)
    
# define MagicCardSet class attributes & methods
class MagicCardSet(object):
    def __init__(self, name=None, cards=[]):
        self.__name = name
        self.__cards = cardInstances(cards)
    def set_name(self, name):
        self.__name = name
    def get_name(self):
        return self.__name
    def get_cards(self):
        return self.__cards

# create an instance of MagicCardSet and populate it with dict values for the keys name and cards
dtk = MagicCardSet(cdict.get('name'), cdict.get('cards'))

# verify the DTK name attribute
print("dtk name  = ", dtk.get_name())

# print the artist, colors, and rarity values for each card in the DTK set
dtk_card_instance_list = dtk.get_cards()
for acarddict in dtk_card_instance_list:
    print("artist = ", acarddict.get_artist())
    print("colors = ", acarddict.get_colors())
    print("rarity = ", acarddict.get_rarity())
    print("")


# Problem 1c
# --------------------------------------------------------------------
# verify the DTK name attribute
print("dtk name  = ", dtk.get_name())

# determine the rarity levels for 'Common', 'Uncommon', 'Rare', and 'Mythic Rare'
dtk_card_instance_list = dtk.get_cards()
count_rarity_common = 0
count_rarity_uncommon = 0
count_rarity_rare = 0
count_rarity_mythic_rare = 0
for acarddict in dtk_card_instance_list:
    if (acarddict.get_rarity() == "Common"):
        count_rarity_common = count_rarity_common + 1
    elif (acarddict.get_rarity() == "Uncommon"):
        count_rarity_uncommon = count_rarity_uncommon + 1
    elif (acarddict.get_rarity() == "Rare"):
        count_rarity_rare = count_rarity_rare + 1
    elif (acarddict.get_rarity() == "Mythic Rare"):
        count_rarity_mythic_rare = count_rarity_mythic_rare + 1
    else:
        pass

# output the rarity counts
print("count: rarity =  Common      = ", count_rarity_common)
print("count: rarity =  Uncommon    = ", count_rarity_uncommon)
print("count: rarity =  Rare        = ", count_rarity_rare)
print("count: rarity =  Mythic Rare = ", count_rarity_mythic_rare)
print("")

# print the artist, colors, and rarity values for Mythic Rare cards
print("Artist names and colors for cards with 'Mythic Rare' rarity:")
for acarddict in dtk_card_instance_list:
    if (acarddict.get_rarity() == "Mythic Rare"):
        print("  artist = ", acarddict.get_artist())
        print("  colors = ", acarddict.get_colors())
        print("")


# Problem 1d
# --------------------------------------------------------------------
# count the color frequency of Uncommon cards
print("Most representative colors for cards with 'Uncommon' rarity:")
print("")

# compile a list of non-unique colors, exclude occurances where color is None
nonunique_color_list = []
for acarddict in dtk_card_instance_list:
    if (acarddict.get_rarity() == "Uncommon"):
        artist_color_list = acarddict.get_colors()
        if (artist_color_list != None):
            while (len(artist_color_list) != 0):
                color = artist_color_list.pop()
                nonunique_color_list.append(color)

# debug
#print(sorted(nonunique_color_list))

# generate a unique count for each color occurrance
# source:  https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item-in-python
from collections import Counter
print(Counter(nonunique_color_list))

