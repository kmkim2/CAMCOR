import xml.etree.ElementTree as elemTree
import codecs
import os

hierarchPath = "C:/Users/kmkim/Downloads/research/CRAFT-3.1.3/concept-annotation/GO_BP/GO_BP+extensions/GO_BP_extensions_parsed_hierarchy_2106.txt"

trainPath = "C:/Users/kmkim/PycharmProjects/untitled2/regression/train.tsv"
GOpath = "C:/Users/kmkim/Downloads/research/CRAFT-3.1.3/concept-annotation/GO_BP/GO_BP+extensions/GO_BP_extensions_parsed_no_hierarchy_manual.txt"

outpath = "relatedSet.txt"

GO_dict_ids = []
GO_dict_titles = []
GO_dict_docs = []
hierarchy_dict_ids = []
hierarchy_dict_relatedTitle = []
hierarchy_dict_relatedDoc = []




with codecs.open(GOpath,'r',encoding='utf8') as GOreader:
    lines = GOreader.readlines()
    GOreader.close()
    for i, line in enumerate(lines):
        if(i%4==0):
            GO_dict_ids.append(line.strip())
        elif(i%4==1):
            GO_dict_titles.append(line.strip())
        elif (i % 4 == 3):
            GO_dict_docs.append(line.strip())


#print(GO_dict_ids)
with codecs.open(hierarchPath,'r',encoding='utf8') as reader:
    lines = reader.readlines()
    reader.close()
    for i, line in enumerate(lines):
        if(i%3==0):
            hierarchy_dict_ids.append(line.strip())
        elif (i % 3 == 2):
            relatedIds = line.split("\t")
            relatedTitles = []
            relatedDocs = []
            #print(len(relatedIds))
            for relatedID in relatedIds:
                asdf = relatedID.strip()
                #print(asdf)
                if(asdf!=''):
                    idx = GO_dict_ids.index(asdf)
                    #print(GO_dict_titles[idx])
                    title = GO_dict_titles[idx]
                    relatedTitles.append(title)
                    doc = GO_dict_docs[idx]
                    relatedDocs.append(doc)
                else:
                    title=""
                    doc = ""
                    relatedTitles.append(title)
                    relatedDocs.append(doc)
            hierarchy_dict_relatedTitle.append(relatedTitles)
            hierarchy_dict_relatedDoc.append(relatedDocs)


print(len(hierarchy_dict_ids))
print(len(hierarchy_dict_relatedTitle))

output = codecs.open(outpath, "wb", encoding="utf-8")

with codecs.open(trainPath,'r',encoding='utf8') as trainReader:
    lines = trainReader.readlines()
    trainReader.close()
    for i, line in enumerate(lines):
        splitline = line.split("\t")
        mention = splitline[4]
        ID = splitline[5].strip()
        IDnum = ID.split(":")[1]
        #print(IDnum)
        idx = hierarchy_dict_ids.index(IDnum)
        hierarchyString = '\t'.join(hierarchy_dict_relatedTitle[idx])
        hierarchyString2 ='\t'.join(hierarchy_dict_relatedDoc[idx])

        idx = GO_dict_ids.index(IDnum)
        mentionDoc = GO_dict_docs[idx]

        #idx = GO_dict_ids.index(IDnum)
        # print(GO_dict_titles[idx])
        #doc = GO_dict_docs[idx]

        output.write(mention+"\n")
        output.write(mentionDoc + "\n")
        output.write(hierarchyString+"\n")
        output.write(hierarchyString2+"\n")

output.close()
