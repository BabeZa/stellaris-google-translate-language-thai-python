import re
import os

from time import sleep
from progress.bar import IncrementalBar,ShadyBar
from langdetect import detect



pathIn = 'ORI'
pathRef = 'REF'
pathOut = 'RESULT'

pattern = '([ ]*)([\w\d_.]+)(:)([\d]*)( ")(.*)(")'
fileCurrent = 0


# สร้าง ไดร์ใหม่
def newDir(newpath):
    # ถ้าไม่มีอยู่แล้วให้สร้างใหม่
    if not os.path.exists(newpath):
        os.mkdir(newpath)

def openFolder():
    allfilesList = []
    
    for root, dirs, files in os.walk(pathRef):

        # loop ชื่อไดร์
        for name in dirs:
            pathfiles = os.path.join(root, name)
            # print(pathfiles)
            newpath = pathfiles.replace(pathRef, pathOut)
            # print(newpath)
            # สร้าง ไดร์ใหม่
            newDir(newpath)

        # loop ชื่อไฟล์
        for name in files:
            pathfiles = os.path.join(root, name)
            # เพิ่มชื่อไฟล์ลง allfilesList หลังจากลบ rootpath ออก
            allfilesList.append(pathfiles.replace(pathRef+'\\', ""))

    readWriteFiles(allfilesList)

def fileCount():
    f = open("StellarisNum.txt", "r")
    global fileCurrent
    fileCurrent = int(f.read())

def writefileCount(i):
    f = open("StellarisNum.txt", "w")
    f.write(str(i))
    f.close()

def readWriteFiles(allfilesList):
    allfilesCount = len(allfilesList)

    # fileCount()

    i = 0
    # loop ไฟล์แต่ละไฟล์
    msg = 'Replace : '
    bar = ShadyBar(msg, max=allfilesCount, color='green', suffix=' %(index)d/%(max)d  ')
    for fname in allfilesList:
        filename = ""
        filename = "/" + fname
        # print(filename)
        if  i >= fileCurrent:
            replaceText(filename)                 
            bar.next()
        i = i + 1
        bar.finish()
        writefileCount(i)



def replaceText(filename):
    try:
        f = open(pathIn+filename, "r", encoding="utf8")
        tempORI = f.read()
        f.close()
        # print(tempORI)

        with open(pathRef+filename, encoding="utf8") as file:
            k = 0
            # อ่านทีละบรรทัด
            for line in file:
                text = line.rstrip()
                # print(handleText(text),text)
                status, indexStr = handleText(text)
                if status == 1:
                    # tempORI = tempORI.replace('abcd', 'ram')
                    pattern = '([ ]*)('+indexStr+')( ")(.*)(")'
                    text = text.replace('\\n', "\_n")
                    # print("++",text)
                    tempORI = re.sub(pattern, text, tempORI, flags = re.M)
                
                k = k + 1
        tempORI = tempORI.replace('\_n', "\\n")
        # print(tempORI)
        outF = open(pathOut+filename, "w", encoding="utf-8")
        outF.write(tempORI)
        outF.close()
    except:
        print('ERROR -----> ',pathIn+filename+" --- ")


def handleText(text):
    status, text2, regex = spiltText(text)
    
    if status == 1:
        # เอาไปแปล
        # print("TRAN : ",text2)
        if detectLang(text2) == "th":
            # print("THIS TH : ",text2)
            return 1 ,regex.group(1)+regex.group(2)+":"+regex.group(4)
        else:
            return 2, ""
    elif status == 2:
        # ไม่ต้องแปล
        # print("NO TRAN : ",text)
        return 2, ""
    else:
        print("Error in >>>",text)


def spiltText(text):
    # แยกข้อความเพื่อเอาส่วนที่จะแปล
    # สถานะ 1 คือข้อความนี้มีรูปแบบที่แปลได้
    regex = re.match(pattern, text)
    if regex is not None:
        if regex.group(6).strip() != "":
            textForTrans = regex.group(6)
            # print("-->",textForTrans)
            return 1, textForTrans, regex
        else:
            # print("--/",text)
            return 2, text, regex
    else:
        # print("--|",text)
        return 2, text, regex

def detectLang(text):
    try:
        lang = detect(text) 
    except:
        lang = "xx"
    return lang 



def main():
    openFolder()
    print("######################")


if __name__ == "__main__":
    main()