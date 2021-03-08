# baseline algorithm:
# take two input sentences and check if they are full string match
# if the two input sentences are full string matched, I consider they are paraphrase
# this algorithm also do a simple check for the similarty of the sentence pair
# if the similarity large than a threshold, this algorithm will consider the two input sentences are paraphrase
from difflib import SequenceMatcher
threshold = 0.0

def similar(a, b): # calculate the similarity between two sentences
    return SequenceMatcher(None, a, b).ratio()

# below is the example of how this algorithm work---------------------------------------------
inputSent1 = "I have a brown cat"
inputSent2 = "my cat is brown"
inputSent3 = "A brown cat is sitting here"
similarity1and2 = similar(inputSent1,inputSent2)
similarity1and3 = similar(inputSent1,inputSent3)

# in this case I set the threshold to 0.5
threshold = 0.5

# check if sentence 1 and 2 are paraphrase
print('Similarty:', similarity1and2)
if similarity1and2 > threshold:
    print("sentence 1 and 2 are paraphrase: Yes")
else:
    print("sentence 1 and 2 are paraphrase: No")

# check if sentence 1 and 3 are paraphrase
print('Similarty:', similarity1and3)
if similarity1and3 > threshold:
    print("sentence 1 and 3 are paraphrase: Yes")
else:
    print("sentence 1 and 3 are paraphrase: No")
# example end---------------------------------------------------------------------------------

# to evalute this algorithm, the first step is to load the data file
# in this case I use pandas package:
import pandas as pd

# .data file is tab delimited
# the format for data in the provided file is like:
# Topic_is | Topic_Name | Sent_1 | Sent_2 | Label | Sent_1_tag | Sent_2_tag
# this algorithm only need Sent_1 and Sent_2 for the paraphrase detection 
# note that column start from 0
# so the algorithm needed columns should be [2,3]
# the algorithm also need the Label column to define the votes for the paraphrase detection
# so the algorithm needed columns should be [4] 
# copy the Sent_1 and Sent_2 and Label columens from the data file
dev_data = pd.read_csv('dev.data', delimiter='\t', usecols=[2, 3, 4], names=['Sent1', 'Sent2', 'Label'])
# print(dev_data)

# after got the DataFrame, it is time to check the paraphrase for each row
# first add a new column for saving the paraphrase detection result: Yes or No
dev_data['Paraphrase'] = 'Yes/No'

# since the data come from twitter and has a huge amount, I set the threshold for this case to 0.8
threshold = 0.8
for index, row in dev_data.iterrows():
    # calculate the similarty between two sentences
    similarty = similar(row['Sent1'],row['Sent2'])
    # use the baseline algorithm to determine whether this pair of sentences is paraphrase or not
    # also save the result to Paraphrase column
    if similarty > threshold:
        row['Paraphrase'] = 'Yes'
    else:
        row['Paraphrase'] = 'No'
# print(dev_data)

# save the result to .csv file
dev_data.to_csv('dev_data_paraphrase_result.csv')

# Evaluation-------------------------------------------------------------------------------------
# to calculate the precision
# set up values for calculateGoldStandardYes = 0
GoldStandardYes = 0
GoldStandardNo = 0
SystemYes = 0
SystemNo = 0
TruePositiveYes = 0
TruePositiveNo = 0

# define a function for get the gold standard
def checkExpection(cell): # take in the contents from the "Label" column
    a = int(cell[1]) # save postive votes
    b = int(cell[4]) # save negative votes
    expection = 'No' # set default the paraphrase classification to No
    if a > b: # if positive votes is more than the negative votes
        expection = 'Yes' # change the paraphrase classification to Yes
    return expection

# loop through all row and check
for index, row in dev_data.iterrows():
    # calculate the similarty between two sentences
    expect = checkExpection(row['Label'])
    # gold standard is Yes
    if expect == 'Yes':
        GoldStandardYes += 1
        if row['Paraphrase'] == 'Yes':
            SystemYes += 1
            TruePositiveYes += 1
        else:
            SystemNo += 1
    # gold standard is No
    else: 
        GoldStandardNo += 1
        if row['Paraphrase'] == 'Yes':
            SystemYes += 1
        else:
            SystemNo += 1
            TruePositiveNo += 1

# calculate precision
Precision = (TruePositiveYes / SystemYes + TruePositiveNo / SystemNo) * 0.5
print('Precision:', Precision)
# calculate recall
Recall = (TruePositiveYes / GoldStandardYes + TruePositiveNo / GoldStandardNo) * 0.5
print('Recall:', Recall)
print('F1:', 2*((Precision*Recall)/(Precision+Recall)))
#------------------------------------------------------------------------------------------------