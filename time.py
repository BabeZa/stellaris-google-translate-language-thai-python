import time

start = time.time()
print("hello")
time.sleep(0.1)
end = time.time()
print(end - start)
x = 60.020082235336304

print("Time {:.0f} min".format( x/60 ))
print("Logs-"+str(int(time.time())))