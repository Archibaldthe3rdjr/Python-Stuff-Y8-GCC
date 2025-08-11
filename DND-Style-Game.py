import time
import sys
NameVERI = "no"
def Dot():
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)

def slow_type(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

while NameVERI == "no":
    Name = input("what is your name?")
    time.sleep(1)
    print(Name)
    NameVERI = input("Are you sure? (yes or no)")

Dot()
slow_type("You awake to your alarm clock beeping", 0.10)
time.sleep(.5)
print("\n")
slow_type("morning "+Name+" its time for breakfast!", 0.07)
time.sleep(.5)
print("\n")
slow_type("You roll out of you bed to see your filthy room", 0.10)
time.sleep(1)
print("\n")
slow_type("What do you wish to do?")
Choice1 = input(slow_type("1.Leave Your Room\n 2.Clean Your Room\n 3.Call Out to Mum", 0.10))

if Choice1 == "1":
    print("You choice was 1")

if Choice1 == "2":
    print("You choice was 2")

if Choice1 == "3":
    print("You choice was 3")
