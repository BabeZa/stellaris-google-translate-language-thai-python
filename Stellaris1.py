import re
from os import listdir
from os.path import isfile, join

from googletrans import Translator
translator = Translator()

pathIn = 'Stelleris'
pathOut = pathIn + 'Out'
pattern = '([ ]*)([\w\d_.]+)(:)([\d]*)( ")(.*)(")'
fileCurrent = 0
    

def openFolder():

    allfilesList = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    allfilesCount = len(allfilesList)

    # fileCount()

    msg = ""
    i = 0
    for fname in allfilesList:
        filename = ""
        filename = "/" + fname
        if  i >= fileCurrent:
            allLineCount = len(open(pathIn+filename, encoding="utf8").readlines())
            outF = open(pathOut+filename, "w", encoding="utf-8")
            with open(pathIn+filename, encoding="utf8") as file:
                k = 0
                for line in file:
                    text = line.rstrip()
                    regex = re.match(pattern, text)
                    if regex is not None:
                        if regex.group(6).strip() != "":
                            textForTrans = regex.group(6)
                            if translator.detect(textForTrans).lang == "th":
                                outF.write(text)
                                outF.write("\n")
                            else:
                                resulttrans = translator.translate(textForTrans, src='en', dest='th')
                                print( textForTrans + " -> " + resulttrans.text)
                                outF.write(regex.group(1)+regex.group(2)+":"+regex.group(4)+' "'+resulttrans.text+'"')
                                outF.write("\n")
                        else:
                            outF.write(text)
                            outF.write("\n")
                    else:
                        # print(text)
                        outF.write(text)
                        outF.write("\n")
                    k = k + 1
            outF.close()
        i = i + 1
        # print(i,"/",allfilesCount," -> ",fname, end='\r')


def main():
    # call this before the for loop:
    openFolder()


if __name__ == "__main__":
    main()
