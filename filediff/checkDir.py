__author__ = 'nlfox233'
#coding:utf-8
#Date:2014.6.5
#检测修改过的文件
import os,sys,hashlib,datetime
global_DirOld = "/tmp/website-oringin"
global_DirNew = "/media/nlfox233/Ubuntu 14.04.3 LTS amd64/website"
global_FilesList = []
#输入要比对的文件路径

def InputDirPath():
    global global_DirOld,global_DirNew
    # global_DirOld = unicode(raw_input("请输入备份文件所在目录："),"utf-8")
    while not os.path.exists(global_DirOld):
        print  u"指定的路径不存在，请重新输入"
        # global_DirOld = unicode(raw_input("请输入备份文件所在目录："),"utf-8")
    # global_DirNew = unicode(raw_input("请输入要检测文件的目录："),"utf-8")
    while not os.path.exists(global_DirNew):
        print  u"指定的路径不存在，请重新输入"
        # global_DirNew = unicode(raw_input("请输入要检测文件的目录："),"utf-8")

#将数据保存到文件中
def SaveToFile(filePath,content):
    try:
        f = open(filePath,"a+")
        f.write(content.encode("utf-8") + "\n")
        f.close()
    except Exception,ex:
        print "Error:" + str(ex)

#计算文件的MD5值
def CalcMD5(filepath):
    try:
        #以二进制的形式打开
        with open(filepath,'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            return hash
    except Exception,ex:
        print "Error:" + str(ex)
        return None

#遍历目录下的所有文件
def GetAllSubFiles():
    global global_FilesList
    for dir in os.walk(global_DirNew):
        for file in dir[2]:
            filePath = dir[0] + os.sep + file
            global_FilesList.append(filePath[len(global_DirNew)+1:])

#列出新增文件和变动的文件
def ListChangedFiles():
    global global_DirOld,global_DirNew,global_FilesList
    print u"变动或新增的文件："
    for file in global_FilesList:
        filePathOld = global_DirOld + os.sep + file
        filePathNew = global_DirNew + os.sep + file
        if not os.path.exists(filePathOld) or CalcMD5(filePathOld)!=CalcMD5(filePathNew):
            content = "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ "]" + filePathNew
            print content
            SaveToFile("ChangedFiles.txt",content)

if __name__=="__main__":
    InputDirPath()
    GetAllSubFiles()
    print global_FilesList
    ListChangedFiles()