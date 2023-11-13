from progress.bar import IncrementalBar,FillingCirclesBar,ShadyBar
from time import sleep

bar = IncrementalBar('Processingadwdaww', max=100, color='green', suffix=' %(percent)d%%')
for i in range(100):
    sleep(0.005)
    bar.next()
bar.finish()

bar = ShadyBar('Processingadwdaww', max=180, color='blue', suffix=' %(index)d/%(max)d [%(percent)d%%] :')
for i in range(180):
    sleep(0.005)
    bar.next()
bar.finish()

bar = ShadyBar('Processingadwdaww', max=180)
for i in range(180):
    sleep(0.005)
    if i == 100:
        barTime = IncrementalBar('Waiting time', max=180, color='blue', suffix=' %(index)d/%(max)d                                                             ')
        for i in range(180):
            sleep(0.005)
            barTime.next()
        barTime.finish()
    bar.next()
bar.finish()