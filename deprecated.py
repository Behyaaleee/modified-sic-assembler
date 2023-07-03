from InstSet import Instructions 

# Pass 1
#--------

#file opens here

f = open("in.txt","r")
nfile = []
for line in f :
    line = line[3:]
    line = line.replace("\t"," ")
    line = line.strip(" ")
    my_new = []
    if line.startswith("."):
        continue
    else:
        mylist = line.split()
        mylist = mylist[:3]
        try:
            mylist = mylist[0]+" "+mylist[1]+" "+mylist[2]+"\n"
        except:
            pass
       
        nfile.append(mylist)
nfile.append("End")
f = open("intermediate.txt","w")
for line in nfile:
    f.write(line)
c=[]
for element in nfile:
    c.append(element.split())
starting_address=int(c[0][2],base=16)
 #first pass

my_first_pass=["Address"+" "+nfile[0]]
i=0
n=starting_address
for line in nfile:
    my_list=line.split()
    
    if i==0:
        i+=1
        continue
    elif my_list[0].lower() == "end":
        n+=3
    else:
        s=hex(n)
        new_line=str(s)+" "+line
        my_first_pass.append(new_line)
        if my_list[0].lower() != "end":
            if my_list[1].lower()=="byte":
                if my_list[2].lower().startswith("x"):
                    n+=int((len(my_list[2].lower().strip('x'))-2)/2)
                elif my_list[2].lower().startswith("c"):
                    n+=int((len(my_list[2].lower().strip('c'))-2))
            elif my_list[1]=="word":
                n+=3
            elif my_list[1].lower()=="resb":
                n+=int(my_list[2])
            elif my_list[1].lower()=="resw":
                n+=int(my_list[2])*3
            elif my_list[1].lower() in ['fix','float','hio','norm','sio','tio']:
                n+=1
            else:
                n+=3
        else: n+=3
        
                
f=open("pass1.txt","w")
for line in my_first_pass:
    f.write(line)
my=[]
for line in my_first_pass:
    my.append(line.split())
symtable=[]
symtable.append("loc  label\n")
for i in range(1,len(my)):
    if my[i][1]!="-":
        st=my[i][0]+" "+my[i][1]
        symtable.append(st)
f=open("symbtable.txt","w")
for line in symtable:
    f.write(line+"\n")

#------------------------------------------------------------------------------------------------------------


my_second_pass=[]
for i in range (0,len(my_first_pass)):
    my_second_pass.append(my_first_pass[i].split())
symbol_table=[]
for i in range(0,len(symtable)):
    symbol_table.append(symtable[i].split())    
#print(my_second_pass)
#print(symbol_table)
my_second=[]
for line in my_second_pass:
    if line[2].lower()=='byte':
        if line[3].lower().startswith("x"):
            line.append(line[3].strip("X").strip("'"))
            my_second.append(line)
        else:
            s=line[3].strip("C").strip("'")
            l=""
            for letter in s:
                l+=format(ord(letter),"x")
            line.append(l)
            my_second.append(line)
    elif line[2].lower()=='word':
        objectcode=hex(int(line[3]))
        objectcode=str(objectcode)[2:]
        while len(objectcode) !=6:
            objectcode="0"+objectcode
        else:
            line.append(objectcode)
            my_second.append(line)

    elif line[2].lower() in ['resb','resw']:
        line.append("No-Object code")
        my_second.append(line)
    elif line[0].lower()=='address':
        my_second.append(line)
    elif line[2].lower()=="rsub":
        line.append(Instructions['RSUB']+"0000")
        my_second.append(line)
    elif line[3].lower().endswith(",x"):
        opcode=Instructions[line[2]]
        for i in range(1,len(symbol_table)):
            if symbol_table[i][1].lower()==line[3].lower().rstrip(",x"):
                address=symbol_table[i][0]
                address=str(int(address[2:])+8000)
        object_code=opcode+address
        line.append(object_code)
        my_second.append(line)
    elif line[3].lower().startswith("#"):
        opcode=Instructions[line[2]]
        opcode=hex(int(bin(int(opcode,16))[2:].zfill(8)[:7]+"1",2))
        address=line[3].lower().strip("#")
        if(len(address)!=4):
            address="0"+address
            object_code=opcode+address
            line.append(object_code)
            my_second.append(line)        
    else:
        opcode=Instructions[line[2]]
        for i in range(1,len(symbol_table)):
            if symbol_table[i][1].lower()==line[3].lower():
                address=symbol_table[i][0]
        object_code=opcode+address[2:]
        line.append(object_code)
        my_second.append(line)
the_objectcode_table=[]
for line in my_second:
    l=""
    for ins in line :
        l+=ins+"\t"
    the_objectcode_table.append(l)
f=open("objectcode.txt","w")
for line in the_objectcode_table:
    f.write(line+"\n")

# HTE Record
#------------
#for line in my_second:
#    print(line)
h_record=["H",".",my_second[0][1],".",my_second[1][0],".",my_second[len(my_second)-1][0]]
e_record=["E",".",my_second[1][0]]
t_rec=[]
start=my_second[1][0]
print(hex(int(start,16)-int("0x101e",16)))
i=1
rsub_inst=[]
for j in range(1,len(my_second)):
    if j-i==10:
        t_rec.append(start)
        length=hex(int(my_second[j][0],16)-int(start,16))
        t_rec.append(length)
        while i<j:
            if my_second[i][4]=="No-Object code":
                t_rec.reverse()
                index=t_rec.index("T")
                add=len(t_rec)-index-1+2
                t_rec.reverse()
                print(t_rec[add])
                rsub_inst.append(my_second[i][0])
                i+=1
                continue
            else:
                t_rec.append(my_second[i][4])
                i+=1
        t_rec.append("T")
        i=j
        start=my_second[i][0]
    if j==len(my_second)-1:
        length=hex(int(my_second[j][0],16)-int(start,16))
        t_rec.append(length)
        while i<=j:
            
            t_rec.append(my_second[i][4])
            i+=1
        break
t_rec[add]=hex(int(rsub_inst[0],16)-int(t_rec[add],16))  


f=open("HTERecord.txt","w")
for element in h_record:
    f.write(element)
f.write("\n")
f.write("T")

for i in range(0,len(t_rec)-1):
    if t_rec[i]=="T":
        t_rec[i]="\n"+t_rec[i]
    
print(t_rec)
for element in t_rec:
    f.write(element+".")

f.write("\n")  
for element in e_record:
    f.write(element)
