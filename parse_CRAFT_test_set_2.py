import io
import codecs
import re
import nltk
import All_files

import os

knowtatorPath = "C:/Users/kmkim/Downloads/research/CRAFT-3.1.3/concept-annotation/GO_BP/GO_BP+extensions/knowtator/"
articlePath = "C:/Users/kmkim/Downloads/research/CRAFT-3.1.3/articles/txt/articles_only/"

outPath = "C:/Users/kmkim/PycharmProjects/untitled2/parsed_CRAFT/"


file_list = os.listdir(articlePath)
print(len(file_list))

#nltk.download('all')
#pathList = All_files.allfiles("C:/Users/kmkim/Downloads/research/CRAFT-3.1.3/articles/txt/articles_only")


outFile=""


for i, filename in enumerate(file_list):
    dirName = filename.split(".")[0]
    if not os.path.exists(outPath+dirName):
        os.makedirs(outPath+dirName)
    print(i)
    if i<55:
        print("train")
        outFile=outPath + dirName+ "/train.tsv"
    elif i<61:
        print("test")
        print(filename)
        outFile=outPath + dirName +"/test_with_pos.tsv"
    else:
        print("devel")
        outFile=outPath + dirName+"/devel.tsv"

    output = codecs.open(outFile, "wb", encoding="utf-8")

    starts = []
    ends = []
    spannedTexts = []

    fullKnowtatorPath = knowtatorPath+filename+".knowtator.xml"
    #print(fullKnowtatorPath)
    with codecs.open(fullKnowtatorPath,'r',encoding='utf8') as annotatef:
        annotate_txt_lines =annotatef.readlines()

    line_iter = iter(annotate_txt_lines)

    for annotate_txt_line in line_iter:
        if "span start" in annotate_txt_line:

            arr=annotate_txt_line.split('\"')
            start=arr[1]
            end=arr[3]

            nextline = next(line_iter)
            while "span start" in nextline:
                arr = nextline.split('\"')
                end=arr[3]
                nextline = next(line_iter)

            starts.append(start)
            ends.append(end)

            if "spannedText" in nextline:
                spannedText=nextline.replace('<spannedText>','').replace('</spannedText>','').strip()
                spannedTexts.append(spannedText)
        #elif "mentionClass" in annotate_txt_line:

    annotatef.close()

    startlen = len(starts)
    #print(startlen)
    endlen = len(ends)
    #print(endlen)
    spannedTextlen = len(ends)
    #print(spannedTextlen)

    fullArticlePath = articlePath+filename
    #print(fullArticlePath)




    with codecs.open(fullArticlePath, 'r',encoding='utf8') as txtf:
        txt = txtf.read()
        txtLines = nltk.tokenize.sent_tokenize(txt)

        #for txtLine in txtLines:
        span_generator = nltk.tokenize.WordPunctTokenizer().span_tokenize(txt)
        spans = [span for span in span_generator]
        #print(spans[0][1])
        token_generator = nltk.tokenize.WordPunctTokenizer().tokenize(txt)
        tokens = [token for token in token_generator]
        #print(tokens)

        #wordspans = re.finditer(r'\d+|(?:[^\w\s]|_)+|[^\W_]+', txtLine)
        currentWordStatus='O'
        currentWordMatches=False

        lastSpanEnd = 0
        currentSpanStart = 0

        for span,token in zip(spans,tokens):
            for i in range(0, startlen - 1):
                if span[0]>=int(starts[i]) and span[1]<=int(ends[i]):

                    currentWordMatches=True
            if currentWordMatches==True:
                if currentWordStatus=='O':
                    currentWordStatus='B'
                else:
                    currentWordStatus='I'
                currentWordMatches=False
            else:
                currentWordStatus='O'
            #print(token+"\t"+currentWordStatus)
            currentSpanStart = span[0]

            if int(lastSpanEnd +2) == int(currentSpanStart):
                #if "17020410" in filename:
                #print(token)
                #output.write(".\tX\n")
                output.write(".\tX\t"+str(lastSpanEnd)+ "\t" + str(lastSpanEnd+1) + "\n\n")

            #output.write(token + "\t" + currentWordStatus + "\n")
            output.write(token+"\t"+currentWordStatus+"\t"+str(span[0])+"\t"+str(span[1])+"\n")
            #"\t"+str(span)+
            lastSpanEnd = span[1]

            if token.endswith('.'):
                output.write("\n")
    txtf.close()

    output.close()


# for i in range(0,startlen-1):
#     print (starts[i]+"\t"+ends[i]+"\t"+txt[int(starts[i]):int(ends[i])])
#     print(spannedTexts[i])

