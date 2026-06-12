import random;import os
## 按位读
def read_w(filename,wnum):
    '''
    需要传入已打开文件的文件名和按几位取为一个单位
    '''
    a=filename.read()
    a_=[];bg=0
    while (bg+wnum)<=len(a):
        try:
            A=a[bg:bg+wnum]
            a_.append(A)
            bg+=wnum
        except:
            A=a[bg:]
            a_.append(A)
            bg+=wnum
            print("学号名单不完整或有出错噢~")
        # 考虑不整除的情况
    return [i for i in a_]

## 按行读
def read_h(filename):
    '''
    仅需要传入文件名
    '''
    z=[]
    z=filename.readlines()
    return [i[:-1] for i in z]
#______________________________________________________
#读文件函数
import os
Address_py=str(os.path.abspath( '.'))#获取当前文件目录路径
Address_py=Address_py+"//"
def readfile(filename,readmethod,lenth=10):
    address="".join([Address_py,filename,".txt"])
    with open(address,"r",encoding="utf-8") as filename:
        if readmethod=="h":
            fnlist=read_h(filename)
        if readmethod=="w":
            fnlist=read_w(filename,lenth)
    return fnlist
#______________________________________________________

A=readfile("方剂","h");
#根据文件内容简历程序内题库
answer="";ques=""
AN=[];QU=[]
for i in range(len(A)):
    while len([x for x in A[i]])>=3:
        if A[i][0]=="%":
            ques=A[i];p=i
            for z in range(len(A)):
                if p+2>len(A):
                    break
                elif  len(A[p+1])<=3:
                    answer=answer+A[p+1]
                    p=p+1
                elif A[p+1][0]!="%":
                    answer=answer+A[p+1]+"\n"
                    p=p+1
                elif A[p+1][0]=="%":
                    AN.append(answer);QU.append(ques)
                    ques="";answer=""
                    break
        break
#print(QU,AN)
print("按下回车就会跳出来一个问题，在输入回车会输出相应答案，输入中文“停下”可以退出程序")
k=0
while input()!="停下":
    if k==0:
        b=random.uniform(1,1000)
        B=int(b%len(QU))
        print(QU[B],end="")
        k=1
    elif k==1:
       print(AN[B])
       k=0
k=0;


 