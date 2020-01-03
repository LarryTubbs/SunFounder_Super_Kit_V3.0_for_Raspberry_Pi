translation_table = {"A":".-"}
translation_table["B"] = "-..."
translation_table["C"] = "-.-."
translation_table["D"] = "-.."
translation_table["E"] = "."
translation_table["F"] = "..-."
translation_table["G"] = "--."
translation_table["H"] = "...."
translation_table["I"] = ".."
translation_table["J"] = ".---"
translation_table["K"] = "-.-"
translation_table["L"] = ".-.."
translation_table["M"] = "--"
translation_table["N"] = "-."
translation_table["O"] = "---"
translation_table["P"] = ".--."
translation_table["Q"] = "--.-"
translation_table["R"] = ".-."
translation_table["S"] = "..."
translation_table["T"] = "-"
translation_table["U"] = "..-"
translation_table["V"] = "...-"
translation_table["W"] = ".--"
translation_table["X"] = "-..-"
translation_table["Y"] = "-.--"
translation_table["Z"] = "--.."
translation_table["1"] = ".----"
translation_table["2"] = "..---"
translation_table["3"] = "...--"
translation_table["4"] = "....-	"
translation_table["5"] = "....."
translation_table["6"] = "-....	"
translation_table["7"] = "--..."
translation_table["8"] = "---.."
translation_table["9"] = "----."
translation_table["0"] = "-----"
translation_table["."] = ".-.-.-"
translation_table[","] = "--..--"
translation_table["?"] = "..--.."
translation_table["="] = "-...-"

def translate(input):
    morse_out = ""
    for l in input.upper():
        try:
            if l != ' ':
                morse_out += translation_table[l]
                morse_out += "|"
            elif l == ' ':
                morse_out += ' '
        except Exception:
            pass
    return morse_out

# If run this script directly, do:
if __name__ == '__main__':
    while True:
        s = input("Enter text to translate: ")
        print(translate(s))
