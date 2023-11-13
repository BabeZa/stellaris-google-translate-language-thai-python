from tqdm import tqdm
from time import sleep
from random import random, randint


pbar = tqdm(total=100)
pbar.set_description("Processing ")
pbar.set_postfix(file="----------------------")
for i in range(100):
    sleep(0.01)
    pbar.update(1)
pbar.close()

pbar = tqdm(total=100,ascii ="         #")
pbar.set_description("Processing ")
pbar.set_postfix(file="----------------------")
for i in range(100):
    sleep(0.01)
    pbar.update(1)
pbar.close()