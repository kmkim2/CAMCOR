import codecs
import os
import re
dirName = "17022820"
if not os.path.exists(dirName):
    os.makedirs(dirName)


refPath = "C:/Users/kmkim/PycharmProjects/untitled2/parsed_CRAFT/"+dirName+"/test_with_pos.tsv"
labelPath = "C:/Users/kmkim/Downloads/research/data/biobert_NER_result_GOBP/"+dirName+"/label_test.txt"
tokenPath = "C:/Users/kmkim/Downloads/research/data/biobert_NER_result_GOBP/"+dirName+"/token_test.txt"



output = codecs.open(dirName+"/biobert_NER_result.tsv", "wb", encoding="utf-8")


with codecs.open(refPath,'r',encoding='utf8') as reff:
    ref_lines = reff.readlines()
ref_lines2 = [i for i in ref_lines if i!="\n"]
ref_tokens = []
ref_starts = []
ref_ends = []
for i in ref_lines2:
    iSplit = i.split("\t")
    ref_tokens.append(iSplit[0])
    ref_starts.append(iSplit[2])
    ref_ends.append(iSplit[3])


with codecs.open(labelPath,'r',encoding='utf8') as labelf:
    label_lines = labelf.readlines()

with codecs.open(tokenPath,'r',encoding='utf8') as tokenf:
    token_lines = tokenf.readlines()
    #token_lines2 = [i for i in token_lines if re.search('[a-zA-Z]', i)]

print(len(ref_lines))
print(len(ref_lines2))

print(len(label_lines))
print(len(token_lines))

tokens = []
tokenLabels=[]
subTokens = []
inTheToken = False
token = ""
tokenLabel = ""

startPos = 0
endPos = 0
currentPos = 0


for label_line,token_line in zip(label_lines[:-1],token_lines[:-1]):
    tempLabel = label_line.strip()
    subToken = token_line.strip()
    ##tokenLength = len(subToken.replace('##',''))

    if subToken != '[CLS]' and subToken != '[SEP]':

        if "##" not in subToken: #tempLabel!='X': # start of new Token

            token = ' '.join(subTokens)#.replace('##', '') # print prev. token
            token = token.replace(' ##','')
            #startPos = currentPos
            #tokenLength = 0
            #if token=="." or token==",":
            #    tokenLength =0
            #else:
            #    tokenLength = len(token)
            #endPos = currentPos + tokenLength
            #print(len(token))
            #currentPos = endPos
            if token != "":
                #print(token+"\t"+tokenLabel+"\t"+str(startPos)+"\t" +str(endPos))
                #output.write(token+"\t"+tokenLabel+"\t"+str(startPos)+"\t" +str(endPos)+"\n")
                tokens.append(token)
                tokenLabels.append(tokenLabel)
                token = ""
                subTokens = []
                #currentPos += 1
            subTokens.append(subToken)
            tokenLabel = tempLabel
        else: # in case of 'X'
            subTokens.append(subToken)
        ##currentPos += tokenLength

token = ' '.join(subTokens)#.replace('##', '') # print prev. token
token = token.replace(' ##','')
if token != "":
    tokens.append(token)
    tokenLabels.append(tokenLabel)

#tokens2 = [i for i in tokens if re.search('[a-zA-Z]', i)]

print(len(tokens))
#print(len(tokens2))


output2 = codecs.open(dirName+"/test1.tsv", "wb", encoding="utf-8")
#output3 = codecs.open(dirName+"/test2.tsv", "wb", encoding="utf-8")

current_j = 0

for theToken, theLabel in zip(tokens, tokenLabels):
    if theToken in ref_tokens:
        current_j = ref_tokens.index(theToken)
        ref_tokens[current_j] = ""

        output.write(theToken + "\t" + theLabel +
                      "\t" + ref_starts[current_j] + "\t" + ref_ends[current_j] )
    else:
        output.write(theToken + "\t" + theLabel +
                      "\t" + "0" + "\t" + "0" + "\n" )
output.close()
output2.close()
#for i in tokens2:
 #   output3.write(i+"\n")