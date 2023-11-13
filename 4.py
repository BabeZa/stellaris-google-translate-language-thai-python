import time

all_nums = 100
counter = 0


def status(num, counter):
    print("\033[F"*4)
    print(
        f'Current number {num}',
        f'Numbers done: {counter}, all nums: {all_nums}',
        f'{(num/all_nums):0.0%}',
        sep="\n"
    )

# call this before the for loop:
print("\n"*4, end="")

for x in range(all_nums):
    counter += 1
    status(x, counter)
    time.sleep(0.01)