from InstSet import Instructions as inst
from PassOneSymTable import my_first_pass as mfp
from PassOneSymTable import symtable as st

my_second_pass=[]
for i in range (0,len(mfp)):
    my_second_pass.append(mfp[i].split())
symbol_table=[]
for i in range(0,len(st)):
    symbol_table.append(st[i].split())    

my_second=[]
for line in my_second_pass:
    if line[2].upper()=='BYTE':
        if line[3].upper().startswith("X"):
            line.append(line[3].strip("X").strip("'"))
            my_second.append(line)
        else:
            s=line[3].strip("C").strip("'")
            l=""
            for letter in s:
                l+=format(ord(letter),"X")
            line.append(l)
            my_second.append(line)

#BYTE HANDLED

    elif line[2].upper()=='WORD':
        objectcode=hex(int(line[3]))
        objectcode=str(objectcode)[2:] #NESHEEL EL 0x....
        while len(objectcode) !=6: #LAW WORD FEEHA 5 BAS 
            objectcode="0"+objectcode #CONCAT STRING
        else:
            line.append(objectcode)
            my_second.append(line)

#WORD HANDLED

    elif line[2].upper() in ['RESB','RESW']: #FOR HANDLING RESERVED BYTES AND WORDS 
        line.append("No-Object code")
        my_second.append(line)
    elif line[0].upper()=='ADDRESS': #TO PARSE AFTER THE INITIAL ADDRESS/LOCATION ZERO
        my_second.append(line)
    elif line[2].upper()=="RSUB": #RSUB HANDLED
        line.append(inst['RSUB']+"0000")
        my_second.append(line)
    elif line[3].upper().endswith(",X"): #IF X -> 1 ELSE 0
        opcode=inst[line[2]]
        for i in range(1,len(symbol_table)):
            if symbol_table[i][1].upper()==line[3].upper().rstrip(",X"):
                address=symbol_table[i][0]
                address=str(int(address[2:])+8000)
        object_code=opcode+address
        line.append(object_code)
        my_second.append(line)
    elif line[3].upper().startswith("#"):
        opcode=inst[line[2]]
        y_int=int(opcode ,16)
        y_bin= bin(y_int)
        y_bin = y_bin[2:-1]
        y_bin=y_bin+"1"
        #opcode=hex(int(bin(opcode)[2:]))
        address=line[3].upper().strip("#")
        address_hex = hex(int(address))[2:]
        while(len(address_hex)<4):
            address_hex="0"+address_hex
        object_code=hex(int(y_bin))[2:]+address_hex
        while len(object_code)<6:
            object_code="0"+object_code
        line.append(object_code)
        my_second.append(line)        
    else:
        opcode=inst[line[2]]
        for i in range(1,len(symbol_table)):
            if symbol_table[i][1].upper()==line[3].upper():
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