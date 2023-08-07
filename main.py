from helpers import convertToString, progressBar
from PIL import Image
import numpy as np
import os

def main():
    inputType = input("Encrypt or decrypt (e or d): ").lower()
    while inputType != "e" and inputType != "d":
        inputType = input("Encrypt or decrypt (e or d): ")
    if inputType == "e":
        runEncrypt()
    else:
        runDecrypt()

# Each character in the text is converted to its ascii value, and represented in binary
# The pixels in the image are grouped into 3s
# The rgb values in each pixel are changed to be even to represent a 0, or odd to represent a 1

def runEncrypt():
    # r before string tells python to treat string as raw data so backslashes are preserved
    inputImage = input(r"Please enter the absolute path to the image you want to encrypt the message into: ")
    if not inputImage.isascii():
        print("Please enter a valid path")
        runEncrypt()
    image = Image.open(inputImage)
    imageArray = np.array(image)
    arrayShape = imageArray.shape
    length = imageArray.shape[0]
    height = imageArray.shape[1]
    channels = imageArray.shape[2]
    totalPixels = length * height
    inputText = input(r"Please enter the text you want to encrypt: ")
    while not inputImage.isascii():
        inputText = input(r"Please enter the text you want to encrypt: ")
    # Each character takes three pixels to encode
    if len(inputText) > totalPixels / 3:
        print("Text too long to be encrypted in image")
        runEncrypt()
    # Flattens image into 1D array for easier processing
    imageArray = imageArray.reshape(totalPixels, 1, channels)
    for i in range(len(inputText)):
        progressBar(i, len(inputText))
        # Converts the corresponding letter into a binary number
        unformattedStrToBin = str(bin(ord(inputText[i])))
        # Converts the binary number into an easier-to-process form
        if i < len(inputText) - 1:
            strToBin = unformattedStrToBin[0] + unformattedStrToBin[2: len(unformattedStrToBin)] + "0"
        else:
            strToBin = unformattedStrToBin[0] + unformattedStrToBin[2: len(unformattedStrToBin)] + "1"
        if len(strToBin) < 9:
            strToBin = "0" + strToBin
        for j in range(9):
            digit = strToBin[j]
            value = imageArray[i * 3 + (j // 3)][0][j % 3]
            if value % 2 != int(digit):
                multiplier = 1 if value < 255 else -1
                imageArray[i * 3 + (j // 3)][0][j % 3] += multiplier
    reshapedImageArray = np.reshape(imageArray, arrayShape, "C")
    newImage = Image.fromarray(reshapedImageArray)
    splitPath = os.path.splitext(inputImage)
    newPath = splitPath[0] + "_encrypted" + splitPath[1]
    newImage.save(newPath)
    print('Done!')
    print(f"Your encoded image has been saved at path: {newPath}")
    restart = input("Would you like to encode/decode another image? (y / n): ")
    if restart.lower() == "y":
        main()


def runDecrypt():
    # r before string tells python to treat string as raw data so backslashes are preserved
    inputImage = input(r"Please enter the absolute path to the image you want to extract the message from: ")
    if not inputImage.isascii():
        runDecrypt()
    image = Image.open(inputImage)
    imageArray = np.array(image)
    arrayShape = imageArray.shape
    length = imageArray.shape[0]
    height = imageArray.shape[1]
    channels = imageArray.shape[2]
    totalPixels = length * height
    # flattens image array into 1d array to help with processing
    imageArray = imageArray.reshape(totalPixels, 1, channels)
    text = ""
    count = 0
    flag = True
    # Reads every group of three pixels and extracts the data until the end of the message is reached
    while flag:
        value = ""
        for i in range(3):
            for j in range(3):
                pixelVal = imageArray[count + i][0][j]
                if i == 2 and j == 2 and pixelVal % 2 == 1:
                    flag = False
                    break
                value += str(pixelVal % 2)
        text += convertToString(value)
        count += 3
    print(f'The encoded message was: {text}')
    restart = input("Would you like to encode/decode another image? (y / n): ")
    if restart.lower() == "y":
        main()

main()