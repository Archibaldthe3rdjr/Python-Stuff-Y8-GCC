import time
import os


def slow_type(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.08)
    print()

slow_type("Welcome To Rooms Of Deception\n")

NameV = "no"
time.sleep(1)
while NameV != "yes":
    Name = input("What Shall We Call You?")
    Name = Name.capitalize()
    print("\n"+Name+"\n")
    NameV = input("Are You Sure?\n")
    NameV = NameV.lower()
slow_type("You awake to your alarm clock\n")
slow_type("\nMorning "+Name+" time for breakfast")
slow_type("\nWhat do you wish to do?")
slow_type("\n1.Exit Your Room\n2.Go Back to Sleep\n3.Clean Your Room")
Choice1 = input()

if Choice1 == "1":
    slow_type("You walked out of your room")

if Choice1 == "2":
    slow_type("")