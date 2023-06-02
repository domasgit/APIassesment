def reverse(text):
    return ''.join(text[i] for i in range(len(text) - 1, -1, -1))

text = input("Give text: ")
print("Reversed string:", reverse(text))
