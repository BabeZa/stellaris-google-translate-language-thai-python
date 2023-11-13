from langdetect import detect, detect_langs


text1 = 'To establish a §SSector§!, first select a planet in §SFrontier space§! and press the Create Sector button. This will make the planet the §SCapital§! of a new Sector and all frontier space systems within six hyperjumps will be added to it. Sectors may automate the construction of planetary buildings on planets within them if this option is enabled and they are given resources, greatly reducing the need for micromanagement.'
text2 = '$REASON$$SUBJECT|Y$ ตอนนี้คือ $NEW_TYPE|Y$ ภายใต้ $OVERLORD|Y$'
text3 = 'ข้อตกลงการค้าสิ้นสุดลง พวกเขากลายเป็นวิชา'
text4 = 'Defensive Platform max capacity reached หมาดำวิ่งตัดหน้ารถ'
text5 = '01000111 01110010 01100101 01100101 01110100 01101001 01101110 01100111 01110011 00100000 01100110 01100101 01101100 01101100 01101111 01110111 00100000 01110011 01111001 01101110 01110100 01101000 01100101 01110100 01101001 01100011 01110011'

print(detect(text5))
print(detect_langs(text5))