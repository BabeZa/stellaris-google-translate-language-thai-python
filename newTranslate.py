import re
import os
import time
import csv

from progress.bar import IncrementalBar,ShadyBar
from langdetect import detect
from googletrans import Translator
translator = Translator()


pathIn = 'ORI'
pathOut = 'TRAN'
lang = 'th'

pattern = '([ ]*)([\w\d_.]+)(:)([\d]*)( ")(.*)(")'
fileCurrent = 0
allLineCounts = 0
tranCount = 0
errorCount = 0
thaiCount = 0


VAR1 = re.compile(r'((\$)([\=\+\-\%\*\[\]\.\|\w]+)(\$))')
VAR2 = re.compile(r'((\[)([\.\|\w]+)(\]))')
VAR3 = re.compile(r'((\£)([\w]+)(\£))')
VAR4 = re.compile(r'((\§)([\w]))')
VAR5 = re.compile(r'((\§)([\!]))')
REPL = re.compile(r'__([ ]{0,1})(\d+)([ ]{0,1})__')
REPL2 = re.compile(r'(__([ ]{0,1})/([ ]{0,1})(\d+)([ ]{0,1})__([ ]{0,1}))')
REPL3 = re.compile(r'(([ ]{0,1})__([ ]{0,1})&([ ]{0,1})(\d+)([ ]{0,1})__)')


varlist = []

def replace(matchobj):
  varlist.append(matchobj.group())
  return "__%d__" %(len(varlist)-1)

def replace2(matchobj):
  varlist.append(matchobj.group())
  return "__/%d__ " %(len(varlist)-1)

def replace3(matchobj):
  varlist.append(matchobj.group())
  return " __&%d__" %(len(varlist)-1)


def restore(matchobj):
  return varlist[int(matchobj.group(2))]

def restore2(matchobj):
  return varlist[int(matchobj.group(4))]

def restore3(matchobj):
  return varlist[int(matchobj.group(5))]

def reset_varlist():
    global varlist
    varlist = []

# สร้าง ไดร์ใหม่
def newDir(newpath):
    # ถ้าไม่มีอยู่แล้วให้สร้างใหม่
    if not os.path.exists(newpath):
        os.mkdir(newpath)

def openFolder():
    allfilesList = []
    

    for root, dirs, files in os.walk(pathIn):

        # loop ชื่อไดร์
        for name in dirs:
            pathfiles = os.path.join(root, name)
            # print(pathfiles)
            newpath = pathfiles.replace(pathIn, pathOut)
            # print(newpath)
            # สร้าง ไดร์ใหม่
            newDir(newpath)

        # loop ชื่อไฟล์
        for name in files:
            pathfiles = os.path.join(root, name)
            # เพิ่มชื่อไฟล์ลง allfilesList หลังจากลบ rootpath ออก
            allfilesList.append(pathfiles.replace(pathIn+'\\', ""))

    # print(allfilesList)
    readWriteFiles(allfilesList)

def fileCount():
    f = open("StellarisNum.txt", "r")
    global fileCurrent
    fileCurrent = int(f.read())

def fileCountEnd(i):
    f = open("StellarisNum.txt", "w")
    f.write(str(i))
    f.close()

def readWriteFiles(allfilesList):
    global allLineCounts, errorCount
    allfilesCount = len(allfilesList)

    fileCount()

    csvfile = open("Logs/Logs-"+pathIn+"-"+str(int(time.time()))+'.csv', 'w', encoding='utf-8', newline='')
    logCSV = csv.writer(csvfile)

    i = 0
    # loop ไฟล์แต่ละไฟล์
    for fname in allfilesList:
        filename = ""
        filename = "/" + fname
        # print(filename)
        if  i >= fileCurrent:
            
            allLineCount = len(open(pathIn+filename, encoding="utf8").readlines())
            outF = open(pathOut+filename, "w", encoding="utf-8")
            # print(pathIn+filename)
            msg = 'Translate : '+str(i+1)+'/'+str(allfilesCount)
            bar = ShadyBar(msg, max=allLineCount, color='green', suffix=' %(index)d/%(max)d : '+fname)
            with open(pathIn+filename, encoding="utf8") as file:
                k = 0
                # อ่านทีละบรรทัด
                for line in file:
                    allLineCounts = allLineCounts + 1
                    text = line.rstrip()
                    textFinal, list1 = handleText(text)
                    # print("--",textFinal)
                    outF.write(textFinal)
                    outF.write("\n")
                    k = k + 1
                    bar.next()

                    if list1:
                        data = []
                        data.extend((filename,k))
                        data.extend(list1)
                        logCSV.writerow(data)
                        errorCount = errorCount + 1

            bar.finish()
            outF.close()        
            
        i = i + 1
        fileCountEnd(i)
    csvfile.close()

def handleText(text):
    global thaiCount
    status, text2, regex = spiltText(text)
    
    if status == 1:
        # เอาไปแปล
        # print("TRAN : ",text2)
        if detectLang(text2) == lang:
            # print("THIS TH : ",text2)
            thaiCount = thaiCount + 1
            return text, []
        elif detectLang(text2) == "err":
            return text, []
        else:
            reset_varlist()
            text3 = ingoneTranslate(text2)
            text3 = text3.replace("Pops", "population")
            text3 = text3.replace("pops ", "population")
            # print(text3)
            # print(varlist)
            text4 = translateText(text3)
            # print(text4)
            # text4 = re.sub(r'(\d)\s+(\d)', r'\1\2', text4)
            try:
                text4 = restoreRegex(text4)
                # print(text4)
                text4 = restoreRegex(text4)
                # print(text4)
                text4 = restoreRegex(text4)
                # print(text4)
            except:
                text4 = text2
            text4 = text4.replace("\ n", "\\n")
            text6 = regex.group(1)+regex.group(2)+":"+regex.group(4)+' "'+text4+'"'
            # print(text4)
            # print(varlist)
            if text6.find('__') != -1:
                return text6, [regex.group(1)+regex.group(2)+":"+regex.group(4),text2,text4,varlist,text3]
            else:
                return text6, []
    elif status == 2:
        # ไม่ต้องแปล
        # print("NO TRAN : ",text)
        return text, []
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
        lang = "err"
    return lang 

def ingoneTranslate(txt):
    txt = VAR1.sub(replace, txt)
    txt = VAR2.sub(replace, txt)
    txt = VAR3.sub(replace, txt)
    txt = VAR4.sub(replace2, txt)
    txt = VAR5.sub(replace3, txt)
    return txt

def restoreRegex(text):
    text = REPL3.sub(restore3, text)
    text = REPL2.sub(restore2, text)
    text = REPL.sub(restore, text)
    # text = REPL2.sub(restore2, text)
    # text = REPL3.sub(restore3, text)
    return text

def translateText(textForTrans):
    global tranCount
    # แปลจาก eng เป็น thai
    while(True):
        try:
            textFinal = translator.translate(textForTrans, src='en', dest=lang).text
            tranCount = tranCount + 1
            break
        except Exception as e: 
            barTime = IncrementalBar('Waiting time', max=180, color='blue', suffix=' %(index)d/%(max)d                                                             ')
            for i in range(180):
                time.sleep(1)
                barTime.next()
            barTime.finish()
    return textFinal

def main():
    global allLineCounts, tranCount, errorCount, thaiCount
    start = time.time()
    openFolder()
    end = time.time()
    print("######################")
    print("Time         {:.0f}  min".format( (end - start)/60 ))
    print("All line   :",allLineCounts)
    print("Translate  :",tranCount)
    print("Thai       :",thaiCount)
    print("Error Tran :",errorCount)
    print("######################")


if __name__ == "__main__":
    main()