from http.client import HTTP_VERSION_NOT_SUPPORTED
import os
import getopt
import sys
from tracemalloc import DomainFilter

if os.name == 'nt':
    hspath=r'C:\Windows\System32\drivers\etc\hosts'
elif os.name == 'posix':
    hspath=r'etc/hosts'
hspath='hosts'

def hostseditor(domain,*,mode='edit',ip=''):
    global hspath
    hosts=open(hspath,'r')
    hostsfile=hosts.readlines()
    hosts.close()
    hostsdict={}
    ip_=''
    domain_=''
    ip_getted=False
    for line in hostsfile:
        for i in range(0,len(line)):
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
        hostsdict[domain_]=(ip_,hostsfile.index(line))
        ip_=domain_=''
        ip_getted=False
    if mode=='edit':
        if not domain in hostsdict:
            return
        hostsfile[hostsdict[domain][1]]=ip+' '+domain
    elif mode=='remove':
        if not domain in hostsdict:
            return
        del hostsfile[hostsdict[domain][1]]
    elif mode=='new':
        if domain=='' and ip=='':
            return
        if not hostsfile[-1][-1] =='\n':
            ip='\n'+ip
        hostsfile.append(ip+' '+domain)
    elif mode=='get':
        if not domain in hostsdict:
            return
        return hostsdict[domain]
    hostsfile_=''.join(hostsfile)
    with open(hspath,'w') as hosts:
        hosts.write(hostsfile_)

if __name__=='__main__':
    opts,args=getopt.getopt(sys.argv[1:],shortopts='p:ihv',longopts=['ip=','path=','help','version'])
    verb=sys.argv[1]
    domain=sys.argv[2]
    if domain=='':
        sys.exit()
    for opt_name,opt_value in opts:
        pass
    hostseditor(domain,mode=verb,ip='1.1.2')
    