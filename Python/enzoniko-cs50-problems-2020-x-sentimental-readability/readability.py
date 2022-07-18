from cs50 import get_string


text = get_string("Text: ")
letterscount = 0
wordcount = 1
sentencecount = 0
for i in range(len(text)):
    if (text[i] >= 'a' and text[i] <= 'z') or (text[i] >= 'A' and text[i] <= 'Z'):
        letterscount += 1
    elif (text[i] == " "):
        wordcount += 1
    elif text[i] in [".", "!", "?"]:
        sentencecount += 1
letterscount = 1.0 * letterscount
wordcount = 1.0 * wordcount
sentencecount = 1.0 * sentencecount
g = 0.0588 * ( 100 * (letterscount / wordcount)) - 0.296 * ( 100 * (sentencecount / wordcount)) - 15.8

grade = (round(g))
if (g < 16 and g >= 0):
    print("Grade: ", grade)
elif (g >= 16):
    print("Grade 16+")
else:
    print("Before Grade 1")

