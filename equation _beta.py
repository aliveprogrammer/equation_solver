# here we use # to express sqrt() ^ to express **
# must have '+' after '='
# only one piece after '/' and '#'
# the piece after / and # must be (...) 
# e.g. 10/(x) #(x)
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
        father_string.expr=self.upper
    def solver(self):
        print(self.origin)
        mul={0:1}
        last={}
        if self.sign == False:
            mul={0:-1}
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
                unit=Math_string(self.__next__()[0][1:-1]).expr.reverse()
            if unit == '#':
                unit={sqrt(self.__next__()[0][1:-1]):1}
            last=unit.copy()
            mul=mul*unit  
        self.upper=self.upper+mul
        print("listen to me",self.upper) 

class sqrt:
    def equal(one,another):
        if one.inner == another.inner and one.outer == another.outer:
            return True
        else:
            return False
    def __repr__(self):
        return str(self.outer)+'#'+str(self.inner)
    def __init__(self,sqrt_string):
        self.inner=Math_string(sqrt_string).expr
        self.outer=0
    def pos_find(pos,area):       
        for index,fvalue in area.items():
            if isinstance(index,sqrt):
                if pos.equal(index):
                   del area[index]
                   return fvalue
        else:
            return 0
    def __add__(add1,add2):
        if isinstance(add2,int):
            return sqrt.__radd__(add1,add2)
        res=sqrt('')
        res.inner=add1.inner*add2.inner
        res.outer=add1.outer+add2.outer
        return res
    def __radd__(add1,number):
        res=sqrt('')
        res.inner=add1.inner
        res.outer=add1.outer+number
        return res
class dict_extension():
    def reverse(self):
        exchange=self.get_deno()
        exchange[-1]=self
        return exchange
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
            res[key]=key.pos_find(res)+value
        return res
    def new_mul(m1,m2):
        res={}
        deno1=m1.get_deno()
        deno2=m2.get_deno()
        if deno1 != {0:1} or deno2 != {0:1}:
            res[-1]=deno1*deno2            
        for index1,v1 in m1.items():
            for index2,v2 in m2.items():
                pos=index1+index2
                res[pos]=pos.pos_find(res)+v1*v2
        return res
class int_extension():
    def pos_find(pos,area):
        return area.get(pos,0)
    

from forbiddenfruit import curse
curse(dict,"__add__",dict_extension.new_add)
curse(dict,"__mul__",dict_extension.new_mul)
curse(dict,"get_deno",dict_extension.get_denominator)
curse(dict,"reverse",dict_extension.reverse)
curse(int,"pos_find",int_extension.pos_find)

x='x'               
test_basic="-9x^2-((x+1)^2-10(5x-9)^3)+32+64+2x-7+(x-1)(x^2+9)=+10x-8+10"
test_fraction="((x+1)/(x+2))/(x-10)=+100"
test_sqrt="2#(x)-(4-x)/(#(x))=+((2-x)#(x))/(4-x)"
instance=Math_string(test_sqrt)
