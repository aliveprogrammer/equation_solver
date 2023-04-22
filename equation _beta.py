# here we use # to express sqrt() ^ to express **
# must have '+' after '='
# only one piece after '/'
# the piece after / must be (...) 
# e.g. 10/(x)
class Math_string_base:
    def __next__(self):        
        i=self.index   #i point to the next
        type=None

        if i > len(self.origin)-1 or self.origin[i] == '!':
            raise StopIteration
        if self.origin[i].isdecimal():
            type="number"
            while self.origin[i+1].isdecimal():
                i+=1

        if self.origin[i] == '(':
            type="bracket"    
            num=0    
            while True:
                tmp=self.origin[i]
                if tmp == '(' or tmp == ')':
                    if tmp == '(':
                        num+=1
                    else:
                        num-=1
                        if num == 0:
                            break
                i+=1        
            
        self.index,i=i+1,self.index
        return self.origin[i:self.index],i,type
    def __iter__(self):
        self.index=0
        return self   
    def __init__(self,originstr):
        self.origin=originstr

class Math_string(Math_string_base):
    def __iter__(self):
        self.index=1
        return self
    def sep(self):
        self.pieces=[]
        pos=0
        for unit,index,unuse in self:
#            print(unit,index,unuse)           
            if unit == '+' or unit == '-':
                m=self.origin[pos] == '+'
                if pos >= self.epos and self.epos > 0:
                    m=not m   
                             
                piece=(self.origin[pos+1:index],m)
                self.pieces.append(Math_string_piece(piece,self))                
                pos=index
    def __init__(self,originstr):
        self.expr={}
        self.origin=originstr
        self.epos=originstr.find('=')
        self.origin=self.origin.replace('=','')+'+'     
        if self.origin[0] != '-' and self.origin[0] != '+':
            self.origin='+'+self.origin
        self.sep()
    
class Math_string_piece(Math_string_base):
    
    def __init__(self,pdata,father_string):
        self.origin=pdata[0]+'!'  # origin is a str
        self.upper=father_string.expr
        self.sign=pdata[1]
        self.solver()
    def solver(self):
        mul={0:1}
        last={}
        print(self.origin)
        for unit,index,type in self:  
#            print(unit)
            if type == 'bracket':
                unit=Math_string(unit[1:-1]).expr                             
            if type == 'number':                   
                unit={0:int(unit)}              
            if unit == x:
                unit={1:1}               
            if unit == '^':
                unit=last
                print('^',unit)
                power=int(self.__next__()[0])-2
                while power > 0:
                    unit=unit*last
                    power-=1
            if unit == '/':
                div=Math_string(self.origin[index+2:-2]).expr
                mul=mul*div.get_deno()
                mul[-1]=div
                break
            if unit == '#':
                pass
            last=unit.copy()
            mul=mul*unit
        if self.sign == False:
            mul=mul*{0:-1}
        self.upper.update(self.upper+mul)
        print("listen to me",self.upper) 

class dict_extension():
    def get_denominator(self):
        deno=self.setdefault(-1,{0:1})
        self.pop(-1)
        return deno
    def new_add(add1,add2):
        deno1=add1.get_deno()
        deno2=add2.get_deno()
        add1=add1*deno2
        add2=add2*deno1
        res=add1
        res[-1]=deno1*deno2    
        for key,value in add2.items():
            res[key]=res.get(key,0)+value
        return res
    def new_mul(m1,m2):
        res={}
        deno1=m1.get_deno()
        deno2=m2.get_deno()
        if deno1 != {0:1} or deno2 != {0:1}:
            res[-1]=deno1*deno2
             
        for index1,v1 in m1.items():
            for index2,v2 in m2.items():
                res[index1+index2]=res.get(index1+index2,0)+v1*v2
        return res
   
            

from forbiddenfruit import curse
curse(dict,"__add__",dict_extension.new_add)
curse(dict,"__mul__",dict_extension.new_mul)
curse(dict,"get_deno",dict_extension.get_denominator)

x='x'               
test_basic="-9x^2-((x+1)^2-10(5x-9)^3)+32+64+2x-7+(x-1)(x^2+9)=+10x-8+10"
test_fraction="(10x-1)^2/(x^2)+(5x/((x+6)/(8x+7))-9)^2=+100"
instance=Math_string(test_fraction)