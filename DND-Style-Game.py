import time

NameVERI = "no"
import sys
import time
def Dot():
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)

def slow_typing(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)  # print each char without newline, flush immediately
        time.sleep(delay)
    print()  # move to next line after the text is done

while NameVERI == "no":
    Name = input("what is your name?")
    time.sleep(1)
    print(Name)
    NameVERI = input("Are you sure? (yes or no)")


Dot()
slow_typing("morning "+Name+" its time for breakfast!", 0.05)

