import csv
import sys
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer 0
        - Administrative_Duration, a floating point number 1
        - Informational, an integer 2
        - Informational_Duration, a floating point number 3
        - ProductRelated, an integer 4
        - ProductRelated_Duration, a floating point number 5
        - BounceRates, a floating point number 6
        - ExitRates, a floating point number 7
        - PageValues, a floating point number 8
        - SpecialDay, a floating point number 9
        - Month, an index from 0 (January) to 11 (December) 10
        - OperatingSystems, an integer 11
        - Browser, an integer 12
        - Region, an integer 13
        - TrafficType, an integer 14
        - VisitorType, an integer 0 (not returning) or 1 (returning) 15
        - Weekend, an integer 0 (if false) or 1 (if true) 16

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Open the file as f
    with open(filename) as f:

        # Create a reader object which will iterate over the lines in f 
        reader = csv.reader(f)

        # Skip the first line (header row)
        next(reader)

        # Create empty list of evidences and labels
        evidences = []
        labels = []

        # Create a dictionary that maps the abbreviations of the months to their respective index
        months = {
            "Jan": 0,
            "Feb": 1,
            "Mar": 2,
            "Apr": 3,
            "May": 4,
            "June": 5,
            "Jul": 6,
            "Aug": 7,
            "Sep": 8,
            "Oct": 9,
            "Nov": 10,
            "Dec": 11
        }

        # Create a list with all indexes that represent a floating point number
        # (Administrative_Duration, Informational_Duration, ProductRelated_Duration, BounceRates, ExitRates, PageValues and SpecialDay)
        floats = [1, 3, 5, 6, 7, 8, 9]

        # For each row in the reader 
        for row in reader:

            # Create empty list of evidence (each row evidence)
            evidence = []

            # Loop through all cells in the row
            for i in range(len(row)):

                # If the index corresponds to an evidence
                if i < 17:

                    # If the index is in the floats list
                    if i in floats:

                        # Append to the evidence list the cell value as a floating point number
                        evidence.append(float(row[i]))
                    
                    # If the index is 10 (Month)
                    elif i == 10:

                        # Append to the evidence list the respective index for the month in the cell value
                        evidence.append(months[row[i]])

                    # If the index is 15 (VisitorType)
                    elif i == 15:

                        # Append to the evidence list: 1 if the visitor is returning, otherwise append 0
                        evidence.append(1 if row[i] == "Returning_Visitor" else 0)

                    # If the index is 16 (Weekend)
                    elif i == 16:

                        # Append to the evidence list: 1 if the user visited in a weekend, otherwise append 0
                        evidence.append(1 if row[i] == "TRUE" else 0)
                    
                    # All the other indexes represent an integer cell value
                    # (Administrative, Informational, ProductRelated, OperatingSystems, Browser, Region, TrafficType)
                    else:

                        # Append to the evidence list the cell value as an integer number
                        evidence.append(int(row[i]))
                
                # Otherwise if the index corresponds to the label 
                else:

                    # Append to the labels list: 1 if the revenue is TRUE, otherwise 0
                    labels.append(1 if row[i] == "TRUE" else 0)  

            # Append the row evidence to the evidences list 
            evidences.append(evidence) 

        #print("EVIDENCE: ", evidences[:2])
        #print("LABELS: ", labels[:2])

        # Returns a tuple where the first element is a list of each row's evidence (evidences) and the second element is a list of all the labels
        return (evidences, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # Create a k-nearest neighbor model (k=1)
    model = KNeighborsClassifier(n_neighbors=1)

    # Fit the model with the evidence and the labels
    model.fit(evidence, labels)

    # Return the trained model
    return model 

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # Create sensitivity and specificity floats
    sensitivity, specificity = float(0), float(0)

    # Create variables for positive and negative count
    positive, negative = 0, 0

    # For each pair where the first element is the i item of labels and the second element is the i item of predictions
    for actual, predicted in zip(labels, predictions):
        
        # If the actual label is positive
        if actual == 1:

            # Increase positive variable by one
            positive += 1
            
            # If the actual label is equal to the predicted label
            if actual == predicted:
                
                # Increase sensitivity variable by one
                sensitivity += 1
        
        # If the actual label is negative
        if actual == 0:
            
            # Increase the negative variable by one
            negative += 1

            # If the actual label is equal to the predicted label
            if actual == predicted:
                
                # Increase specificity variable by one
                specificity += 1
    
    # Divide sensitivity by the positive variable and assign the result to sensitivity
    sensitivity /= positive

    # Divide specificity by the negative variable and assign the result to specificity
    specificity /= negative

    # Return the sensitivity and the specificity 
    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
