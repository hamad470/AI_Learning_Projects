

def addition(name,a,b):  
    print(name)  
    add = a+b
    return add


def multiplication(name,a,b):
    print(name)
    mult = a*b
    return mult


a = int(input("ENTER DIGIT-1 "))
b = int(input("ENTER DIGIT-2 "))


value_add = addition("THIS IS ADDITION",a=a,b=b) 
multi = multiplication("THIS IS MULTIPLICATION ",a,b)

print("Addition : ")
print(value_add)

print("Multiplication : ")
print(multi)












