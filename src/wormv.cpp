#include<thread>
#include<mutex>
#include<dirent.h>
#include<stdio.h>
#include<locale.h>
#include<queue>
#include<string>
#include<vector>
#include<list>
#include<iostream>
#ifdef WIN32
#include<windows.h>
#define rmdir RemoveDirectoryA
#else
#include<unistd.h>
#endif
//共享变量
static std::queue<std::string> allfilepath;
static std::list<std::string> alldirpath;       //任务池
static std::mutex taskgetlock;                  //任务池访问锁
static std::mutex dirgetlock;
static bool welldone = false;

void walk(const std::string& dirpath);
bool isdirempty(const std::string& dirpath);
//线程函数
void rmfilethread();
void rmdirthread();

int main(int argc,char** argv) {
    if (argc < 2) {
        return 1;
    }
    setlocale(LC_ALL, "zh_cn.UTF8");
    std::vector<std::thread> allthread(20);
    int i;
    for (i = 0;i < 20;i++) {
        allthread[i] = std::thread(rmfilethread);
    }
    std::thread dirthread(rmdirthread);
    std::string path(argv[1]);
    if (path.at(path.size() - 1) == '/')
        path = path.assign(0,path.size() - 1);
    walk(path);
    welldone = true;
    for (i = 0;i < 20;i++) {
        allthread[i].join();
    }
    dirthread.join();
    return 0;
}

void walk(const std::string& dirpath) {
    dirgetlock.lock();
    alldirpath.push_back(dirpath);
    dirgetlock.unlock();
    std::size_t pathsize = dirpath.size();
    char* c_dirpath = new char [pathsize+1];
    dirpath.copy(c_dirpath,pathsize);
    c_dirpath[pathsize] ='\0';                      //string对象转c-字符串
    DIR* dirmain = opendir(c_dirpath);
    while(dirent* afile = readdir(dirmain)) {
        if (afile -> d_name[0] == '.' && (afile -> d_name[1] == '\0' || afile -> d_name[1] == '.'))
            continue;
        std::string dname(afile -> d_name);
        std::string sep("/");
        if (afile -> d_type == DT_DIR) {
            if (afile -> d_name)
            walk(dirpath + sep + dname);
        }
        else {
            std::string filepath = dirpath + sep + dname;
            taskgetlock.lock();
            allfilepath.push(filepath);
            taskgetlock.unlock();
        }
    }
    closedir(dirmain);
    delete [] c_dirpath;
}

bool isdirempty(const std::string& dirpath) {
    std::size_t pathsize = dirpath.size();
    char* c_dirpath = new char [pathsize+1];
    dirpath.copy(c_dirpath,pathsize);
    c_dirpath[pathsize] ='\0';
    DIR* dirmain = opendir(c_dirpath);
    for (int i = 0;i < 2;i++)
        readdir(dirmain);
    bool isempty = (bool) readdir(dirmain);
    closedir(dirmain);
    delete [] c_dirpath;
    return !isempty;
}

void rmfilethread() {
    while (true) {
        taskgetlock.lock();
        if (allfilepath.empty())
            if (welldone) {
                taskgetlock.unlock();
                return;
            }
            else {
                taskgetlock.unlock();
                continue;
            }
        std::string thispath = allfilepath.front();
        allfilepath.pop();
        taskgetlock.unlock();
        std::size_t pathsize = thispath.size();
        char* c_path = new char [pathsize+1];
        thispath.copy(c_path,pathsize);
        c_path[pathsize]='\0';
        remove(c_path);
        delete [] c_path;
    }
}

void rmdirthread() {
    while (true) {
        if (welldone && alldirpath.empty())
            return;
        dirgetlock.lock();
        std::list<std::string>::iterator it = alldirpath.begin();
        dirgetlock.unlock();
        while (it != alldirpath.end()) {
            dirgetlock.lock();
            std::string thispath = *it;
            dirgetlock.unlock();
            if (isdirempty(thispath)) {
                std::size_t pathsize = thispath.size();
                char* c_path = new char [pathsize+1];
                thispath.copy(c_path,pathsize);
                c_path[pathsize]='\0';
                rmdir(c_path);
                delete [] c_path;
                dirgetlock.lock();
                it = alldirpath.erase(it);
                dirgetlock.unlock();
            }
            else
                it++;
        }
    }
}