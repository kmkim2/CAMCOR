
import codecs

mentionPath = "C:/Users/kmkim/PycharmProjects/untitled2/17020410/biobert_NER_result_concept_words.tsv"


with codecs.open(mentionPath,'r',encoding='utf8') as reader1:
    lines = reader1.readlines()

mentions = []
startPoss = []
endPoss = []
GOIDs= []

for line in lines:
    theline = line.split("\t")
    mentions.append(theline[0])
    startPoss.append(theline[1])
    endPoss.append(theline[2].strip())

output = codecs.open("17020410.bionlp", "wb", encoding="utf-8")

for mention, startPos, endPos in zip (mentions, startPoss, endPoss):
    output.write("T3\tGO:0006281 " + startPos + " " + endPos + "\t" + mention+ "\n")
