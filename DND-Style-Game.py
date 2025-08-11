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
slow_type("You awake to your alarm clock beeping")
time.sleep(.5)
print("\n")
slow_type("morning "+Name+" its time for breakfast!")
time.sleep(.5)
print("\n")
slow_type("You roll out of your bed to see your filthy room")
time.sleep(1)
print("\n")

slow_type("What do you wish to do?")
Choice1 = input(slow_type("1.Leave Your Room\n2.Clean Your Room\n3.Call Out to Mum"))

if Choice1 == "1":
    slow_type("\n\nYou left your room")
    
    slow_type("Where do you go now?")
    Choice2 = input(slow_type("1. Walk to kitchen\n2. Go to lounge room"))
    if Choice2 == "1":
        slow_type("\nYou enter the kitchen to see your mother cooking pancakes")
    
    if Choice2 == "2":
        slow_type("You see your younger brother up watching cocomelon on the TV")

if Choice1 == "2":
    print("You choice was 2")

if Choice1 == "3":
    print("You choice was 3")
