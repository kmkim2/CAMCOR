import xml.etree.ElementTree as elemTree
import codecs
import os

knowtatorPath = "C:/Users/kmkim/Downloads/research/CRAFT-3.1.3/concept-annotation/GO_BP/GO_BP+extensions/knowtator/"
file_list = os.listdir(knowtatorPath)
outPath = "C:/Users/kmkim/PycharmProjects/untitled2/regression/"
print(len(file_list))

for i, filename in enumerate(file_list):
    #dirName = filename.split(".")[0]
    #if not os.path.exists(outPath+dirName):
    #    os.makedirs(outPath+dirName)
    print(i)
    if i<55:
        print("train")
        outFile=outPath +  "/train.tsv"
    elif i<61:
        print("test")
        #print(filename)
        outFile=outPath +"/test_with_pos.tsv"
    else:
        print("devel")
        outFile=outPath + "/devel.tsv"

    output = codecs.open(outFile, "ab", encoding="utf-8")

    starts = []
    ends = []
    spannedTexts = []

    fullKnowtatorPath = knowtatorPath+filename
    print(fullKnowtatorPath)
    #tree = elemTree.parse(fullKnowtatorPath)

#print("asdf")

    tree = elemTree.parse(fullKnowtatorPath)
    annotations = tree.findall('./annotation')

    mentionIDs = []
    mentionIDs2 = []

    texts1= []
    texts2=[]

    for annotation in annotations:
        #print(annotation.tag)
       # print(annotation.attrib)
        #print(annotation.find('id'))
        mentionID = annotation.find('mention').get('id')
        spanStart = annotation.find('span').get('start')
        spanEnd = annotation.find('span').get('end')
        spanText = annotation.find('spannedText').text

        mentionIDs.append(mentionID)
        texts1.append(spanStart+"\t"+spanEnd+"\t"+spanText+"\t")
    zip_iterator = zip(mentionIDs, texts1)
    dict1 = dict(zip_iterator)
    #print(len(dict1))

    mentions = tree.findall('./classMention')
    for mention in mentions:
        mentionID =  mention.get('id')
        entityName = mention.find('mentionClass').text
        goID = mention.find('mentionClass').get('id')

        mentionIDs2.append(mentionID)
        texts2.append(entityName + "\t" + goID )
    zip_iterator = zip(mentionIDs2, texts2)
    dict2 = dict(zip_iterator)
    #print(len(dict2))

    keys = dict1.viewkeys() | dict2.viewkeys()
    dict3 = {k : dict1.get(k, '') + dict2.get(k, '') for k in keys}
    for key, value in zip(dict3.keys(), dict3.values()):
        output.write(key+"\t"+value+"\n")
        #print(key)
        #print(value)
    output.close()