# woka
## 警告
这是一个测试版，所有功能都不太稳定的。
## 介绍
一个实用的工具集
## 模块介绍
### wohs.py
一个方便的hosts编辑器
### wormv.cpp
快速删除工具，中文文件夹可能被跳过
### wormv.py
旧版的wormv.cpp，现在已被废弃（太慢了）
### wotb.py
爬取tiobe语言排行榜（最没用的的一个功能）
### wocr.py
sRGB颜色混合器
### womon.py
纯色图生成器
### wowbcn.py
爬取网页图标
## 平台兼容问题
windows下没有dirent.h,可以通过[这个项目](https://github.com/tronkko/dirent)解决
## 安装
### Windows:
```
git clone https://github.com/hpytrail/wokawd
cd wokawd
.\install-windows.ps1
```
### Linux:
```
git clone https://github.com/hpytrail/wokawd
cd wokawd
./install-linux.sh
```
安装后所有文件到安装到了build文件夹下，可以复制这些文件到任何文件夹（也可以包含到path路径)。
## 卸载
只要删除build下的文件和path路径就行（如果有的话）。