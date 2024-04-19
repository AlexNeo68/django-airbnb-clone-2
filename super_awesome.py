class Dog:
    def __init__(self):
        print("Dog init called")

    def bark(self):
        print("Dog bark called")

    def eat(self):
        print("Dog eat called")


class Puppy(Dog):
    def __init__(self):
        print("Puppy init called")
        super().__init__()

    def eat(self):
        print("Puppy eat called")
        super().eat()


p = Puppy()
p.eat()