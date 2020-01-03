import morsecode as morse

msg = input("Enter a message to translate into morse code:")
morse_msg = morse.translate(msg)
print(morse_msg)