import csv
import random
import sys

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
        - 0 Administrative, an integer
        - 1 Administrative_Duration, a floating point number
        - 2 Informational, an integer
        - 3 Informational_Duration, a floating point number
        - 4 ProductRelated, an integer
        - 5 ProductRelated_Duration, a floating point number
        - 6 BounceRates, a floating point number
        - 7 ExitRates, a floating point number
        - 8 PageValues, a floating point number
        - 9 SpecialDay, a floating point number
        - 10 Month, an index from 0 (January) to 11 (December)
        - 11 OperatingSystems, an integer
        - 12 Browser, an integer
        - 13 Region, an integer
        - 14 TrafficType, an integer
        - 15 VisitorType, an integer 0 (not returning) or 1 (returning)
        - 16 Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        next(csvreader) # skip first line (header)

        for row in csvreader:
            evidence.append(row)
    
    for i in range(len(evidence)):
        if evidence[i].pop(17) == 'TRUE':
            labels.append(1)
        else:
            labels.append(0)
        
        for j in range(len(evidence[i])): 
            # convert to integer: 0,2,4,11,12,13,14
            if j == 0 or j == 2 or j == 4 or j == 11 or j == 12 or j == 13 or j == 14:
                evidence[i][j] = int(evidence[i][j])
            # convert to float: 1,3,5,6,7,8,9
            elif j == 1 or j == 3 or j == 5 or j == 6 or j == 7 or j == 8 or j == 9:
                evidence[i][j] = float(evidence[i][j])
            # month: 10
            elif j == 10:
                months = ['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec'] # No data with Jan & Apr
                evidence[i][j] = months.index(evidence[i][j])
            # returning visitor: 15
            elif j == 15:
                evidence[i][j] = 1 if evidence[i][j] == 'Returning_Visitor' else 0
            # weekend: 16
            elif j == 16:
                evidence[i][j] = 1 if evidence[i][j] == 'TRUE' else 0

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors = 1)

    # Separate data into training and testing groups
    #holdout = int(0.50 * len(evidence))
    #random.shuffle(evidence)
    #testing = evidence[:holdout]
    #training = evidence[holdout:]

    # Train model on training set
    X_training = evidence
    y_training = labels
    return model.fit(X_training, y_training)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    correct_positives = 0
    correct_negatives = 0
    total_positives = 0
    total_negatives = 0

    for i in range(len(labels)):
        if labels[i] == 1:
            total_positives += 1
            if labels[i] == predictions[i]:
                correct_positives += 1
        else:
            total_negatives += 1
            if labels[i] == predictions[i]:
                correct_negatives += 1
        
    sensitivity = correct_positives / total_positives
    specificity = correct_negatives / total_negatives

    return (sensitivity, specificity)


if __name__ == "__main__":
    load_data("shopping.csv")
    main()
