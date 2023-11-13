from time import sleep
import sys

for i in range(50):
    sys.stdout.write('\r')
    # the exact output you're looking for:
    sys.stdout.write("[%-49s]" % ('='*i))
    sys.stdout.flush()
    sleep(0.1)