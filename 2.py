from googletrans import Translator
translator = Translator()

text = 'Class W Star : These giant stars are also known as Wolf-Rayet stars, for which a very high luminosity and temperature are characteristic. These stars are most often found in nebulae, that resulted from the dumping of the envelope of red supergiants - the previous stage of the evolution of these stars. Constant electromagnetic emissions of the unstable star disrupt the operation of protective systems of both ships and stations, making them more vulnerable.!'

result = translator.translate(text, src='en', dest='th')
lng = translator.detect(text)

print(result.text)
print(lng)