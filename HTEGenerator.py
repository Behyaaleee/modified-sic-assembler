from PassTwo import my_second

# x =hex(int(bin(int(my_second[len(my_second)-1][0])[2:])))
# y = hex(int(bin(int(my_second[0][1])[2:])))
# z = x-y
# print (z)


x = int(my_second[len(my_second)-1][0],16)
y = int(my_second[1][0],16)
z = hex(x-y) #TO GET DIFFERENCE BETWEEN FIRST AND LAST ADDRESS
h_rec=["H",".",my_second[0][1],".",my_second[1][0],".",z] #H REC

e_rec=["E",".",my_second[1][0]] #E REC

t_rec=[] #ARRAY TO STORE THE T VALUES
start=my_second[1][0]
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
for element in h_rec:
    f.write(element)
f.write("\n")
f.write("T")

for i in range(0,len(t_rec)-1):
    if t_rec[i]=="T":
        t_rec[i]="\n"+t_rec[i]
    
for element in t_rec:
    f.write(element+".")

f.write("\n")  
for element in e_rec:
    f.write(element)
