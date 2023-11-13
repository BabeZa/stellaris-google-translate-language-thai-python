import re
from googletrans import Translator
translator = Translator()
data = ''

def start_reader():
    with open("b/Dust King joins fight.po", encoding="utf8") as f:
        global data 
        data = f.read()

def spit_msg():
    global data
    patten = '(msgid *")(.*)(")[\r\n]*(msgstr *")(.*)(")'
    r=re.findall(patten,data)
    # print(r)
    rawlist = []
    for x in r:
        if(x[1] != ''):
            # print({"id":x[1],"str":x[4]})
            rawlist.append({"id":x[1],"str":x[4]})
    return rawlist

def trans(result):
    for a in result:
        temp = a['id'] 
        tran = translator.translate(temp,dest='th',src='en').text
        print(temp,'->',tran)

start_reader()
result = spit_msg()
trans(result)

