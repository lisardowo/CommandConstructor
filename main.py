from Mamushi.program import Program
from constructModel import constructorModel

if __name__ == "__main__":
    model = constructorModel()
    Program(model).run()