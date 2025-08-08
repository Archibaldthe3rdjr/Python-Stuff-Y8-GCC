import time

NameVERI = "no"

while NameVERI == "no":
    Name = input("what is your name?")
    time.sleep(1)
    print(Name)
    NameVERI = input("Are you sure? (yes or no)")

def Dot():
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)


Dot()
print("morning "+Name+" its time for breakfast!")

