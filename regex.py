import re


pattern = '([ ]*)([\w\d_.]+)(:)([\d])( ")(.*)(")'
text = ' mem_synthetic_sun.1.name:0 "This is No Moon"'


regex = re.match(pattern, text)
if regex is not None:
    print(regex)
    print(regex.group(6))
else:
    print(text)

