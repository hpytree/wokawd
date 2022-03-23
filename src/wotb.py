import getopt
import sys
import requests
from lxml import etree

class tblist:
    def __init__(self,begin,end,*,ranking=True,rantings=True,\
        change=True,foreward=False):
        self.begin=begin
        self.end=end
        self.ranking=ranking
        self.rantings=rantings
        self.change=change
        self.foreward=foreward
        self.rankinglist={}
        self.forewarda=''

    def getlist(self):
        h={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64\
; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}
        htmlfile=\
            requests.get('https://www.tiobe.com/tiobe-index/',headers=h)
        html=etree.HTML(htmlfile.text)
        onetotwenty=html.xpath('/html/body/section/section/section/\
article/table[1]/tbody/tr')
        twentytofifty=html.xpath('/html/body/section/section/section/\
article/table[2]/tbody/tr')
        alllist=onetotwenty+twentytofifty
        del onetotwenty
        del twentytofifty
        for i in range(self.begin-1,self.end):
            td=alllist[i].xpath('td')
            if i < 20:
                self.rankinglist[td[4].text]={}
                if self.ranking:
                    self.rankinglist[td[4].text]['ranking']=int(td[0].text)
                if self.rantings:
                    self.rankinglist[td[4].text]\
                        ['rantings']=float(td[5].text[0:-1])
                if self.change:
                    self.rankinglist[td[4].text]\
                        ['change']=float(td[6].text[0:-1])
            else:
                self.rankinglist[td[1].text]={}
                if self.ranking:
                    self.rankinglist[td[1].text]['ranking']=int(td[0].text)
                if self.rantings:
                    self.rankinglist[td[1].text]\
                        ['rantings']=float(td[2].text[0:-1])
        if self.foreward:
            forewardp=\
                html.xpath('/html/body/section/section/section/article/p')
            forewarda=[]
            for i in range(0,3):
                forewarda.append(''.join(forewardp[i].itertext()))
            self.forewarda='\n'.join(forewarda)+'\n'

    def show(self):
        if self.foreward:
            print(self.forewarda)
        if self.ranking:
            print('ranking',end='\t')
        print('name',end='\t\t\t')
        if self.rantings:
            print('rantings',end='\t')
        if self.change:
            print('change',end='\t')
        print('')
        for name,details in self.rankinglist.items():
            if self.ranking:
                print(details['ranking'],end='\t')
            if len(name) < 8:
                end='\t\t\t'
            elif len(name) < 16:
                end='\t\t'
            else:
                end='\t'
            print(name,end=end)
            if self.rantings:
                print(str(details['rantings'])+'%',end='\t\t')
            if self.change and 'change' in details:
                print(str(details['change'])+'%',end='\t')
            print('')

if __name__=='__main__':
    opts,args=getopt.getopt(sys.argv[1:],\
        shortopts='hvb:e:urcf',longopts=['help','version','begin=','end=','unranking',\
        'rantings','change'])
    begin,end=1,50
    ranking=True
    rantings,change,foreward=False,False,False
    for name,value in opts:
        if name in ('-h','--help'):
            pass
        elif name in ('-v','--version'):
            pass
        elif name in ('-b','--begin'):
            if not value=='':
                begin=int(value)
        elif name in ('-e','--end'):
            if not value=='':
                end=int(value)
        elif name in ('-u','--unranking'):
            ranking=False
        elif name in ('-r','--rantings'):
            rantings=True
        elif name in ('-c','--change'):
            change=True
        elif name in ('-f','--foreward'):
            foreward=True
    mainindex=tblist(begin,end,ranking=ranking,rantings=rantings,\
        change=change,foreward=foreward)
    mainindex.getlist()
    mainindex.show()
