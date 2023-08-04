def convertToString(binString):
    powers = [128, 64, 32, 16, 8, 4, 2, 1]
    total = 0
    for i in range(8):
        total += int(binString[i]) * powers[i]
    return chr(total)

def progressBar(current, total, bar_length = 20):
    printVal = current + 1
    denomFactor = 100 / total
    percent = int(printVal * denomFactor)
    arrow   = '-' * int(percent/100 * bar_length - 1) + '>'
    spaces  = ' ' * (bar_length - len(arrow))

    print(f'Progress: [{arrow}{spaces}] {percent}%')