import codecs
import os


dirName = "17022820"
Path = "C:/Users/kmkim/PycharmProjects/untitled2/"+dirName+"/biobert_NER_result.tsv"

output = codecs.open(dirName + "/biobert_NER_result_concept_words.tsv", "wb", encoding="utf-8")

currentMentions = []

isMention = False

currentStartPos = 0
currentEndPos = 0

with codecs.open(Path,'r',encoding='utf8') as f:
    lines = f.readlines()
    for line in lines:
        line_split = line.split()
        token = line_split[0]
        tag = line_split[1]
        if tag=='B':
            if currentMentions:
                print(' '.join(currentMentions))
                output.write(' '.join(currentMentions)+"\t" + currentStartPos + "\t" + currentEndPos + '\n')
            currentMentions = []
            currentMentions.append(token)
            currentStartPos = line_split[2]
            currentEndPos = line_split[3]
            isMention = True
        elif tag=='I' and isMention ==True:
            currentMentions.append(token)
            currentEndPos = line_split[3]
        elif tag=='O':
            isMention=False