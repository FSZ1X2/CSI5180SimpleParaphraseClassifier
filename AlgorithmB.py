# advance algorithm:
# this algorithm give different weight to different POS
# it also calculate for a same POS the edit distance between two words
# this algorithm sum up all edit distance with respect to the POS weight to get the final result
# if the final result doesn't pass the threshold, it considered this pair of sentences are paraphrase

# define the function for edit distance calculation
import numpy as np
def editDistance(word1, word2):
    # if first word is empty, the edit distance will be the length of second word
    # if second word is empty, the edit distance will be the length of first word
    if len(word1) == 0:
        return len(word2)
    if len(word2) == 0:
        return len(word1)

    # based on the source: https://web.stanford.edu/class/cs124/lec/med.pdf Page:14
    # build matrix for calculate the edit distance
    matrix = np.zeros((len(word1)+1,len(word2)+1), dtype=np.int)
    for i in range(len(word1)+1): 
        for j in range(len(word2)+1):
            # three situation need to be compared:
            a = matrix[i][j-1] + 1
            b = matrix[i-1][j] + 1
            c = matrix[i-1][j-1] + 2
            if word1[i-1] == word2[j-1]:
                c = matrix[i-1][j-1] + 0
            matrix[i][j] = min(a, b, c)
    return matrix[len(word1)][len(word2)]
 
# test code-------------------------------------------------------
# word1 = "levenshtein"
# word2 = "levels"
# result should be 7
# print(editDistance(word1, word2))
#-----------------------------------------------------------------

# set up weithgt for different POS:
# based on https://corenlp.run/ and https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
CC = 1
CD = 1
DT = 2
EX = 1
FW = 1
IN = 1
JJ = 4
JJR = 4
JJS = 4
LS = 1
MD = 1
NN = 2
NNS = 2
NNP = 3
NNPS = 3
PDT = 1
POS = 1
PRP = 3
PRP4 = 4
RB = 3
RBR = 3
RBS = 3
RP = 2
SYM = 1
TO = 1
UH = 1
VB = 5
VBD = 5
VBG = 5
VBN = 5
VBP = 5
VBZ = 5
WDT = 2
WP = 2
WP4 = 2
WRB = 2
Others = 1

# set up threshold
threshold = (CC + CD + DT + EX + FW + IN + JJ + JJR + JJS + LS + MD + NN + NNS + NNP + NNPS + PDT + POS + PRP + PRP4 + RB + RBR + RBS + RP + SYM + TO + UH + VB + VBD + VBG + VBN + VBP + VBZ + WDT + WP + WP4 + WRB + Others) / 37
print(threshold)

# the main idea for this algorithm is to calculate the average edit distance for each words in a pair of sentences
# use pandas package for dataframe
import pandas as pd

# this algorithm need a function to define the POS for each words from the tags
import io
def BuildPOSTable(sent):
    # split the string
    rawString = sent.split()
    # set up two list to store the POS and the word
    POS_list = list()
    word_list = list()
    # loop through the string and get POS/word pairs from it
    for i in range(0, len(rawString)):
        WordwithPOS = rawString[i].split('/')
        POS_list.append(WordwithPOS[2])      
        word_list.append(WordwithPOS[0])
    # build a POS table for this sentence
    d = {'POS':POS_list,'Word':word_list}
    POSTable = pd.DataFrame(d)
    # print(POSTable)
    return POSTable

# this algorithm need a function to generate a weight list for input list
def Weight(input_list):
    # set weight for others POS as default
    weight_list = [Others]*len(input_list)

    # set weight for different POS
    for i in range(0, len(input_list)):
        if input_list[i] == 'CC':
            weight_list[i] = CC
        if input_list[i] == 'CD':
            weight_list[i] = CD
        if input_list[i] == 'DT':
            weight_list[i] = DT
        if input_list[i] == 'EX':
            weight_list[i] = EX
        if input_list[i] == 'FW':
            weight_list[i] = FW
        if input_list[i] == 'IN':
            weight_list[i] = IN
        if input_list[i] == 'JJ':
            weight_list[i] = JJ
        if input_list[i] == 'JJR':
            weight_list[i] = JJR
        if input_list[i] == 'JJS':
            weight_list[i] = JJS
        if input_list[i] == 'LS':
            weight_list[i] = LS
        if input_list[i] == 'MD':
            weight_list[i] = MD
        if input_list[i] == 'NN':
            weight_list[i] = NN
        if input_list[i] == 'NNS':
            weight_list[i] = NNS
        if input_list[i] == 'NNP':
            weight_list[i] = NNP
        if input_list[i] == 'NNPS':
            weight_list[i] = NNPS
        if input_list[i] == 'PDT':
            weight_list[i] = PDT
        if input_list[i] == 'POS':
            weight_list[i] = POS
        if input_list[i] == 'PRP':
            weight_list[i] = PRP
        if input_list[i] == 'PRP$':
            weight_list[i] = PRP4
        if input_list[i] == 'RB':
            weight_list[i] = RB
        if input_list[i] == 'RBR':
            weight_list[i] = RBR
        if input_list[i] == 'RBS':
            weight_list[i] = RBS
        if input_list[i] == 'RP':
            weight_list[i] = RP
        if input_list[i] == 'SYM':
            weight_list[i] = SYM
        if input_list[i] == 'TO':
            weight_list[i] = TO
        if input_list[i] == 'UH':
            weight_list[i] = UH
        if input_list[i] == 'VB':
            weight_list[i] = VBD
        if input_list[i] == 'VBG':
            weight_list[i] = VBG
        if input_list[i] == 'VBN':
            weight_list[i] = VBN
        if input_list[i] == 'VBP':
            weight_list[i] = VBP
        if input_list[i] == 'VBZ':
            weight_list[i] = VBZ
        if input_list[i] == 'WDT':
            weight_list[i] = WDT
        if input_list[i] == 'WP':
            weight_list[i] = WP
        if input_list[i] == 'WP$':
            weight_list[i] = WP4
        if input_list[i] == 'WRB':
            weight_list[i] = WRB

    return weight_list

# this algorithm need a function to calculate the average edit distance after get POS tables for each sentence
def CompareTables(t1, t2):
    T1POS = t1['POS'].tolist()
    T2POS = t2['POS'].tolist()
    T1word = t1['Word'].tolist()
    T2word = t2['Word'].tolist()

    # create a list that combined two POS list
    ComparePOS = list(set(T1POS+T2POS))
    # print(ComparePOS)

    # fill words into related POS
    T1wordList = [""]*len(ComparePOS)
    for i in range(0, len(T1POS)):
        for j in range(0,len(ComparePOS)):
            if T1POS[i] == ComparePOS[j]:
                T1wordList[j] = T1word[i]
    # print(T1wordList)
    T2wordList = [""]*len(ComparePOS)
    for i in range(0, len(T2POS)):
        for j in range(0,len(ComparePOS)):
            if T2POS[i] == ComparePOS[j]:
                T2wordList[j] = T2word[i]
    # print(T2wordList)  

    # set up weight list for this comparison
    weightList = Weight(ComparePOS)
    # print(weightList)

    # calculte edit distance with weight
    distance = 0
    for w in range(0, len(ComparePOS)):
        # calculate edit distance
        distance += editDistance(T1wordList[w],T2wordList[w]) * weightList[w]
    distance = distance/len(ComparePOS) #distance/average
    # print(distance)
    return distance

# example ---------------------------------------------------------------------------------------------------
# threshold = 1.5
Sent1 = "ZBo/O/IN/B-PP/O playing/O/VBG/B-VP/B-EVENT no/O/DT/B-NP/O games/O/NNS/I-NP/O"	# Sent1: ZBo playing no games
Sent2 = "Gasol/O/NNP/B-NP/O and/O/CC/I-NP/O ZBo/B-person/NNP/I-NP/O are/O/VBP/B-VP/O bullies/O/NNS/B-ADJP/O" # Sent2: Gasol and ZBo are bullies
Sent1POSTable = BuildPOSTable(Sent1) # build a POS table for sentence 1
Sent2POSTable = BuildPOSTable(Sent2) # build a POS table for sentence 1
# calculate average edit distance based on POS tables and weight for each POS
distance = CompareTables(Sent1POSTable, Sent2POSTable) 
print(distance)
# check paraphrase
if distance < threshold: print("Paraphrase: Yes")
else: print("Paraphrase: No")
# example end ------------------------------------------------------------------------------------------------

# load the data file
# .data file is tab delimited
# the format for data in the provided file is like:
# Topic_is | Topic_Name | Sent_1 | Sent_2 | Label | Sent_1_tag | Sent_2_tag
# this algorithm needs Sent_1_tag and Sent_2_tag for the paraphrase detection 
# note that column start from 0
# so the needed columns should be [5,6]
# the algorithm also need the Label column to define the votes for the paraphrase detection
# so the algorithm needed columns should be [4] 
# copy the needed columens from the data file
dev_data = pd.read_csv('dev.data', delimiter='\t', usecols=[4, 5, 6], names=['Label', 'Sent1Tag', 'Sent2Tag'])

# after got the DataFrame, it is time to check the paraphrase for each row
# first add a new column for saving the paraphrase detection result: Yes or No
dev_data['Paraphrase'] = 'Yes/No'

# paraphrase detection
# threshold = 1.5
for index, row in dev_data.iterrows():
    data_string1 = row['Sent1Tag']
    data_string2 = row['Sent2Tag']
    Sent1POSTable = BuildPOSTable(data_string1)
    Sent2POSTable = BuildPOSTable(data_string2)

    # calculate edit distance based on POS
    DistanceForEdit = CompareTables(Sent1POSTable, Sent2POSTable)

    # check paraphrase
    if DistanceForEdit < threshold:
        row['Paraphrase'] = 'Yes'
    else: 
        row['Paraphrase'] = 'No'

# save the result to .csv file
dev_data.to_csv('dev_data_paraphrase_result_AlgoB.csv')

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
def checkExpection(cell):
    a = int(cell[1])
    b = int(cell[4])
    expection = 'No'
    if a > b:
        expection = 'Yes'
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

