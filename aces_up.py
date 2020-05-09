import io
import sys
import time
import hashlib
import pyautogui

def is_club(md5):
    return md5 in ['73ddb26f3bf3084464469233028d42aa', '81664e4a36265a68b61bfd213f34c450', '746a0f4698be801d47a6b0ecc385c4e6', '3cc4c384e370056c26efa19a6f13c929', '3fc30ef2beefc5caa8c8a00fe86f4ef6', 'bafde2a70a90961f34588c0763bf01cb', '00865b5590e9acb97e80cf06b28223d0', 'ffe05dbe65dcd08b5d68d6cc802efc1c', 'f6bd3e708c347ed4ae0be2ce392ec025', 'ee563fb4ae0b999007c831afd3d406c9', '5c9b36ad3b09261b766e0290a5e7c2e6', '59cd97f90cc20beed594696194238cab', 'f48c00cbc1b5480066b2f461d333adef']

def is_diamond(md5):
    return md5 in ['43f7b83888e8fe4c2cbbfcca86004acb', '2975f74592d5502c095942169ac85d2b', '1fe84917f77dd55bbb215e91727c7721', '223d84c90cb5c41bcfeedbafc3793622', '55bf37ac5a9efd4e4a561ad35531ad2a', 'e724a03f682486f946cd28bb212c958e', '72eacee39bae683c73b92820f168c168', '71a11735e7603ae43eacc925d561f08c', 'f435a357b2c0e1aa4f6974c9dc637c94', '56439a614fef0c8af51e674de4f3b439', '1dc33cfb4857b6cac06292e0b152d43a', 'ec014e12a5cdb8050e668837c2788b95', 'f011c3ced7f0725175f26e0a22cc17fd']

def is_heart(md5):
    return md5 in ['119fb77b0371b51c62fd9eeb7d73abae', 'ccaa4d730a2790bd0251f930f03884a1', '900b2b234b2dfe8e7923509c9bc44ccf', '4de27bc44ffe388c4b67d8de6ce3705b', '2e62fc946c8644442fef7aea0cf287a7', '91996d19532ec2dd463d62282c3996d6', '0b594e8e752c60d97e8cccafe874121a', '504279c6dd149a324170b8d10dec140f', 'fa844dcdb88f9f53502ea4ed9bfd00e7', '76f0ddd2ca1f6bfb8385bc50526014be', 'd2087ff22cb66bf6e88f773936fab27e', 'f3d4b30e65a927b0a6b4e1d0d3a01536', '63403e0ede2aa0eb89a7125781c802c2', '4d5e664fc4c1cc1f8d477cee8e846ac9']

def is_spade(md5):
    return md5 in ['fbe784e82919eac059bf3e2d00e81cfb', '8929932e7a61316633407856170a8eaf', '37311e012c399b932cdb487b64552d26', '07987aec7bb1f33fac5754f0eb4b5893', '94ed7584f4dbca9f45ec838dd26ae7e5', '1c169f7aad05af8f9e4e947ce26cbb6d', '7ff23c6887ab08b6c5a96ccdbf3662a7', '1a5458309be4504314d1a04b1d239639', '53bf38ba1292e4096f4cd8d737721fe1', '97d056bc70b142ccc5ff7433d459a43c', '6cbe312a44441cab30c34f5be680657a', '2d54e60d7d28ddff3fd16c4b7ad1c197', 'e3066dc447d0180cb6453f052408b5f1']

def suit(md5):
    if is_club(md5):
        return 0
    if is_diamond(md5):
        return 1
    if is_heart(md5):
        return 2
    return 3

def count_aces(md5sums):
    return len(md5sums & {'56439a614fef0c8af51e674de4f3b439', '76f0ddd2ca1f6bfb8385bc50526014be', '97d056bc70b142ccc5ff7433d459a43c', 'ee563fb4ae0b999007c831afd3d406c9'})

time.sleep(2) # wait 2s before executing the script to allow opening KPatience

aces = 3 # how many aces should there be in a deal
same_suit = False # all cards in a deal are in the same suit
interval = 1.6 # interval between deals

for arg in sys.argv:
    if arg.startswith('aces'):
        if arg[-1:].isdigit():
            aces = ord(arg[-1:])-48 if ord(arg[-1:])-48 < 4 else 4
    if "suit" in arg:
        same_suit = True
    if "interval" in arg:
        try:
            interval = float(arg[1+arg.rfind('='):])
        except:
            pass

while True:
    pyautogui.click(200, 90) # click "New Deal" button
    time.sleep(interval) # wait for the cards to show and for the solver to calculate the outcome
    screenshot = pyautogui.screenshot()
    pixels = screenshot.load()
    
    # check pixel with coordinates (123,1051); marked red in solver_texts.png
    # if green from RGB value is not high enough it means that the text is not "Solver: This game is winnable."
    # in that case skip further checks and go to the next deal
    if pixels[123,1051][2] < 210:
        continue

    # get fragments of each card and save them as byte objects
    card1, card2, card3, card4 = io.BytesIO(), io.BytesIO(), io.BytesIO(), io.BytesIO()
    screenshot.crop((550,165,710,230)).save(card1, 'png')
    screenshot.crop((770,165,930,230)).save(card2, 'png')
    screenshot.crop((990,165,1150,230)).save(card3, 'png')
    screenshot.crop((1210,165,1370,230)).save(card4, 'png')

    # calculate MD5 sums of each fragment
    md5_1 = hashlib.md5(card1.getvalue()).hexdigest()
    md5_2 = hashlib.md5(card2.getvalue()).hexdigest()
    md5_3 = hashlib.md5(card3.getvalue()).hexdigest()
    md5_4 = hashlib.md5(card4.getvalue()).hexdigest()

    # check if all suits are the same
    if same_suit and suit(md5_1) == suit(md5_2) and suit(md5_1) == suit(md5_3) and suit(md5_1) == suit(md5_4):
        break
    # check in there are enough aces
    if count_aces({md5_1, md5_2, md5_3, md5_4}) >= aces:
        break

pyautogui.moveTo(500,500) # move cursor to avoid accidentally clicking on "New Deal"