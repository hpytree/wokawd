#!usr/bin/python3
import os
from multiprocessing import Process,Manager,Lock,Value
import sys

def removenull(allp,welldir):
    while True:
        p=allp
        if len(p)==0 and welldir.value==1:
            return
        for i in p:
            if len(os.listdir(i))==0:
                os.rmdir(i)
                del allp[allp.index(i)]

def removemain(welldone,allpath,l0):
    while True:
        l0.acquire()
        if len(allpath)==0:
            if welldone.value==1:
                l0.release()
                return
            else:
                l0.release()
                continue
        removepath=allpath.pop()
        l0.release()
        os.remove(removepath)

def main(path):
    l_taskget=Lock()
    m=Manager()
    g_allpath=os.walk(path)
    allpro=[]
    allfpath=m.list([])
    allpath=m.list([])
    welldone=Value('i',0)
    welldir=Value('i',0)
    for i in range(20):
        allpro.append(Process(target=removemain,\
            args=(welldone,allfpath,l_taskget)))
        allpro[i].start()
    dirpro=Process(target=removenull,args=(allpath,welldir))
    dirpro.start()
    try:
        while True:
            thispath=next(g_allpath)
            if not thispath[2]==[]:
                for i in thispath[2]:
                    allfpath.append(thispath[0]+os.sep+i)
            if not thispath[1]==[]:
                for i in thispath[1]:
                    allpath.append(thispath[0]+os.sep+i)
    except StopIteration:
        welldone.value=1
        welldir.value=1
        for i in allpro:
            i.join()
        dirpro.join()

if __name__=='__main__':
    main(sys.argv[1])