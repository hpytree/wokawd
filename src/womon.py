from PIL import Image
import sys
import getopt

def main(mode,w,h,clr,t,savepath):
    im=Image.new(mode,(w,h),tuple(clr))
    if t == '':
        period=savepath.rfind('.')
        if period==0:
            return 1
        t=savepath[period+1:]
    im.save(savepath,t)

if __name__=='__main__':
    opts,args=getopt.getopt(sys.argv[1:],'m:p:t:',\
        ['width=','height=','mode=','value=','path=','type='])
    w=h=400
    mode='RGB'
    clr=[255,255,255]
    savepath='../test/240.png'
    t=''
    for name,value in opts:
        if name == '--width':
            w=int(value)
        elif name == '--height':
            h=int(value)
        elif name in ('-m','--mode'):
            mode=value
        elif name == '--value':
            clr=[int(i) for i in value.split(',')]
        elif name in ('-p','--path'):
            savepath=value
        elif name in ('-t','--type'):
            t=value
    main(mode,w,h,clr,t,savepath)