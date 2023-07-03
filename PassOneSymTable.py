

f = open("in.txt","r")
nfile = []
for line in f :
    line = line[3:]
    line = line.replace("\t"," ")
    line = line.strip(" ")
    my_new = []
    if line.startswith("."):
        pass
    else:
        ListOne = line.split()
        ListOne = ListOne[:3]
        try:
            ListOne = ListOne[0]+" "+ListOne[1]+" "+ListOne[2]+"\n"
        except:
            pass
       
        nfile.append(ListOne) ##EXTEND GIVES ARRAY OUT OF BOUND ERROR
nfile.append("END")

#FILE IS FREE FROM NUMBERS DOTS TABS AND COMMENTS AND ALSO HAS AN END 

f = open("intermediate.txt","w")
for element in nfile:
    #print(element)
    f.write(element)

#INTERMEDIATE FILE IS NOW DONE


c=[]
for element in nfile:
    c.append(element.split())
LocZero=int(c[0][2],base=16) 


my_first_pass=["Address"+" "+nfile[0]]
# intialise address
i=0
n=LocZero
for element in nfile:
    my_list=element.split()
    
    if i==0:
        i+=1
        pass
    elif my_list[0].upper() == "END":
        n+=3 
    else:
        s=hex(n)
        new_line=str(s)+" "+element
        my_first_pass.append(new_line)
        if my_list[0].upper() != "END":
            if my_list[1].upper()=="BYTE":
                if my_list[2].upper().startswith("X"):
                    n+=int((len(my_list[2].upper().strip('X'))-2)/2)
                elif my_list[2].upper().startswith("C"):
                    n+=int((len(my_list[2].upper().strip('C'))-2))
            elif my_list[1].upper()=="WORD":
                n+=3
            elif my_list[1].upper()=="RESB":
                n+=int(my_list[2])
            elif my_list[1].upper()=="RESW":
                n+=int(my_list[2])*3
            elif my_list[1].upper() in ['FIX','FLOAT','HIO','NORM','SIO','TIO']:
                n+=1
            else:
                n+=3
        else: n+=3

#UPPER 3ALASHAN AWDA7 MEN LOWER
        
                
f=open("pass1.txt","w")
for line in my_first_pass:
    f.write(line)
#PASS 1 DONE AND OUT !!!

my=[]
for line in my_first_pass:
    my.append(line.split())


symtable=[]
symtable.append("location label\n")
for i in range(1,len(my)):
    if my[i][1]!="-":
        st=my[i][0]+" "+my[i][1]
        symtable.append(st)
f=open("symbtable.txt","w")

for line in symtable:
    f.write("\n"+line)

#SYMBOL TABLE IS DONE