import getopt
import sys
import requests
from lxml import etree

def main(url:str,savedir='../test',sizes=''):
    h={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64\
; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}
    htmlfile=requests.get(url,headers=h)
    html=etree.HTML(htmlfile.text)
    alliconlink=[]
    for i in html.xpath('//link'):
        if not i.xpath('@rel')[0].find('icon') == -1:
            alliconlink.append(i)
    if alliconlink==[]:
        return
    href=''
    if not sizes=='':
        allsizes={}
        for i in alliconlink:
            s=i.xpath('@sizes')
            if not s == []:
                allsizes[s[0]]=i
        if sizes not in allsizes:
            return
        href=i.xpath('@href')[0]
    else:
        href=alliconlink[0].xpath('@href')[0]
    if not url[-1]=='/':
        url+='/'
    if href[0] == '/' and not href[1] == '/':
        href=href[1:]
    imgurl=''
    if href[0:2]=='//':
        pos=url.find('//')
        imgurl=url[0:pos]+href
    else:
        imgurl=url+href
    img=requests.get(imgurl,headers=h).content
    filename=''
    if savedir=='':
        pass
    elif not savedir[-1] == '/' and not savedir[-1] == '\\':
        savedir+='/'
    filenamepos=imgurl.rfind('/')
    filename=imgurl[filenamepos+1:]
    f=open(savedir+filename,'wb')
    f.write(img)
    f.close()

if __name__=='__main__':
    opts,args=getopt.getopt(sys.argv[1:],shortopts='d:u:s',\
        longopts=['dir=','url=','sizes='])
    dir='../test'
    url='https://www.baidu.com/'
    sizes=''
    for name,value in opts:
        if name in ('-d','--dir'):
            dir=value
        elif name in ('-u','--url'):
            url=value
        elif name in ('-s','--sizes'):
            sizes=value
    main(url,dir,sizes)
