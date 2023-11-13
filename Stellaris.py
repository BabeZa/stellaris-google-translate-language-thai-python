import re
from os import listdir
from os.path import isfile, join

from googletrans import Translator
translator = Translator()

pathIn = 'Stelleris'
pathOut = pathIn + 'Out'
pattern = '([ ]*)([\w\d_.]+)(:)([\d]*)( ")(.*)(")'
fileCurrent = 0

def status(filename, fileNum, allFile, process, allLine):
    percent = int((process/allLine)*50)
    bar = "#" * percent + '-' * (50 - percent)
    print("\033[F"*4)
    print(
        f'Current file : {filename}                                                                   ',
        f'file: {fileNum} / {allFile}                                                                 ',
        f'{process}/{allLine} : [{bar}] {(process/allLine):2.1%}',
        sep="\n"
    )

def fileCount():
    f = open("StellarisNum.txt", "r")
    global fileCurrent
    fileCurrent = int(f.read())
    

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
            print("\033[F"*4)
            print(msg,"\n\n\n")
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
                                # print(" -> " +resulttrans.text)
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
                    status(fname, i, allfilesCount, k, allLineCount)
            outF.close()
            msg = "file Done: "+ str(allLineCount) +" : "+ fname + " "*50
        i = i + 1
        f = open("StellarisNum.txt", "w")
        f.write(str(i))
        f.close()
        # print(i,"/",allfilesCount," -> ",fname, end='\r')


def main():
    # call this before the for loop:
    print("\n"*4, end="")
    openFolder()


if __name__ == "__main__":
    main()
