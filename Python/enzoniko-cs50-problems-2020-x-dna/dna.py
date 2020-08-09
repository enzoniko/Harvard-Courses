from sys import argv, exit
import pandas as pd


# Checks if the number of files is correct
if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

# Reads the text file
f = open(argv[2], "r")
sequences = f.readline()
f.close()

# Returns the longest sequences in a dictionary


def patterns(a, b, c): #, e, f, g, h):

    STRs = {a: 0, b: 0, c: 0} #, e: 0, f: 0, g: 0, h: 0}
    counter = 0
    text_accumulator = ""

    for idx, char in enumerate(sequences):

        text_accumulator += char

        for key in STRs.keys():

            if idx + 1 + len(key) <= len(sequences) - 1:
                if key in text_accumulator:
                    counter += 1
                    text_accumulator = ""

                    if sequences[idx + 1: idx + 1 + len(key)] == key:
                        continue
                    else:
                        if STRs[key] < counter:
                            STRs[key] = counter
                        counter = 0

    return STRs


# Compares the sequences with the database in the CSV file
DNA_person = patterns("AGATC", "TATC", "AATG") # , "GAAA", "TTTTTTCT", "GATA", "TCTG", "TCTAG"
df = pd.read_csv(argv[1])
df = df.loc[(df["AGATC"] == DNA_person["AGATC"]) & (df["TATC"] == DNA_person["TATC"]) & (df["AATG"] == DNA_person["AATG"])] # & (df["GAAA"] == DNA_person["GAAA"]) & (df["TTTTTTCT"] == DNA_person["TTTTTTCT"]) & (df["GATA"] == DNA_person["GATA"]) & (df["TCTG"] == DNA_person["TCTG"]) & (df["TCTAG"] == DNA_person["TCTAG"])]


# Prints the results
if df.empty:
    print("No match")
for i, row in df.iterrows():
    print(row["name"])