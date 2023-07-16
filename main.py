def main():
    inputType = input("Encrypt or decrypt (e or d): ").lower()
    while inputType != "e" and inputType != "d":
        inputType = input("Encrypt or decrypt (e or d): ")
    if inputType == "e":
        runEncrypt()
    else:
        runDecrypt()