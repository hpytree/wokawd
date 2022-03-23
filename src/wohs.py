import os
import getopt
import sys

if os.name == 'nt':
    hspath=r'C:\Windows\System32\drivers\etc\hosts'
elif os.name == 'posix':
    hspath=r'etc/hosts'
#hspath='..'+os.sep+'test'+os.sep+'hosts'

def getcomm(sent:str):
    vgetted=dgetted=igetted=False
    verb=domain=ip=''
    for i in range(len(sent)):
        if sent[i].isspace():
            if verb:
                vgetted=True
                if domain:
                    dgetted=True
                    if igetted:
                        igetted=True
            if verb and domain and ip:
                break
            continue
        if not vgetted:
            verb+=sent[i]
        elif not dgetted:
            domain+=sent[i]
        elif not igetted:
            ip+=sent[i]
    print(dgetted)
    return verb,domain,ip

class hosts:
    def __init__(self,hspath):
        o_hosts=open(hspath)
        self.hostsfile=o_hosts.readlines()
        o_hosts.close()
        self.hostsdict={}
        ip_getted=False
        domain_=ip_=''
        for line in self.hostsfile:
            for i in range(len(line)):
                if line[i].isspace():
                    if not (ip_ == ''):
                        ip_getted=True
                    continue
                elif line[i] == '#':
                    break
                if not ip_getted:
                    ip_+=line[i]
                else:
                    domain_+=line[i]
            if ip_ == '' and domain_ == '':
                ip_=domain_=''
                ip_getted=False
                continue
            self.hostsdict[domain_]=(ip_,self.hostsfile.index(line))
            ip_=domain_=''
            ip_getted=False

    def set(self,domain,ip):
        if not domain in self.hostsdict:
            return
        self.hostsfile[self.hostsdict[domain][1]]=ip+' '+domain+'\n'

    def remove(self,domain):
        if not domain in self.hostsdict:
            return
        del self.hostsfile[self.hostsdict[domain][1]]

    def new(self,domain,ip):
        if domain=='' or ip=='':
            return
        if not self.hostsfile[-1][-1] =='\n':
            ip='\n'+ip
        self.hostsfile.append(ip+' '+domain+'\n')

    def get(self,domain):
        if not domain in self.hostsdict:
            return
        return self.hostsdict[domain][0]

    def change(self,domain,*,mode='set',ip=''):
        if mode=='set':
            self.set(domain,ip)
        elif mode=='remove':
            self.remove(domain)
        elif mode=='new':
            self.new(domain,ip)
        elif mode=='get':
            return self.get(domain)

    def save(self):
        hostsfile_=''.join(self.hostsfile)
        with open(hspath,'w') as hosts:
            hosts.write(hostsfile_)

if __name__=='__main__':
    opts,args=getopt.getopt(sys.argv[3:],shortopts='?p:i:hv',\
        longopts=['ip=','path=','help','version','shell'])
    shellmode=False
    ip=''
    for name,value in opts:
        if name in ('-h','--h','-?'):
            pass
        elif name in ('-v','--version'):
            pass
        elif name in ('-p','--path'):
            hspath=value
        elif name in ('-i','--ip'):
            ip=value
        elif name=='--shell':
            shellmode=True
    if len(sys.argv)>1:
        domain=sys.argv[2]
        verb=sys.argv[1]
    else:
        domain=verb=''
    hostsmain=hosts(hspath)
    if verb:
        hostsmain.change(domain,mode=verb,ip=ip)
    while shellmode:
        verb,domain,ip=getcomm(input('> '))
        if verb in ('q','quit','exit'):
            break
        backvalue=hostsmain.change(domain,mode=verb,ip=ip)
        if verb == 'get':
            print(backvalue)
    hostsmain.save()
