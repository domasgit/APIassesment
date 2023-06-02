text = input("Provide text: ")
result = ''.join([char for char in text if char.lower() not in 'aeiou'])
print("String without vowels:", result)
