import requests
from lxml import etree
def gettiobe(begin,end,*,ranking=True,rantings=True,change=True,foreward=False):
    h={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64\
        ; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}
    htmlfile=requests.get('https://www.tiobe.com/tiobe-index/',headers=h)
    html=etree.HTML(htmlfile.text)
    onetotwenty=html.xpath('/html/body/section/section/section/\
        article/table[1]/tbody/tr')
    twentytofifty=html.xpath('/html/body/section/section/section/\
        article/table[2]/tbody/tr')
    alllist=onetotwenty+twentytofifty
    del onetotwenty
    del twentytofifty
    rankinglist={}
    if not (ranking and rantings and change):
        return None
    for i in range(begin-1,end):
        td=alllist[i].xpath('td')
        if i < 20:
            rankinglist[td[4].text]={}
            if ranking:
                rankinglist[td[4].text]['ranking']=int(td[0].text)
            if rantings:
                rankinglist[td[4].text]['rantings']=float(td[5].text[0:-1])
            if change:
                rankinglist[td[4].text]['change']=float(td[6].text[0:-1])
        else:
            rankinglist[td[1].text]={}
            if ranking:
                rankinglist[td[1].text]['ranking']=int(td[0].text)
            if rantings:
                rankinglist[td[1].text]['rantings']=float(td[2].text[0:-1])
    if foreward:
        forewardp=html.xpath('/html/body/section/section/section/article/p')
        forewarda=[]
        for i in range(0,3):
            forewarda.append(''.join(forewardp[i].itertext()))
        forewarda='\n'.join(forewarda)+'\n'
        return (rankinglist,forewarda)
    return (rankinglist,)

def printtiobe(rankinglist):
    for i,j in rankinglist[0].items():
        print(i,end='\t')
        for ji in j.values():
            print(str(ji),end='\t')
        print('',end='\n')
    print(rankinglist[1])
    

printtiobe(gettiobe(1,50,foreward=True))