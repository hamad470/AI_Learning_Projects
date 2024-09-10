class A():
    

    def __init__(self):
        print("Constructor is Initialized...")
        attr1 = "ABC"
        pass
    def method(self):

        self.atr2="CDF"
        print("Method access")

    def add(self,a,c):
        
        return a+c
    
obj = A()    
obj.__init__()
# print(A.atr2)
# add = obj.add(3,4)
# print(add)






