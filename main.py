# coding:utf-8
"""
input file :host.txt
output file :result.txt

result is a list like :
["www.baidu.com","14.215.177.38","http://www.baidu.com","title_baidu","200","OK","Tengine"]

run the main.py script then
you can run result.deal.py to get clear reperot view
or you can run reportGeneral.py to get a screen and html repeort
"""

import socket
import requests
import urllib.parse
import re
from bs4 import BeautifulSoup
import urllib3
import sys
from SiteReport import result_d
import traceback
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_hostIP(host):

    result = socket.getaddrinfo(host, None)
    ip = result[0][4][0]
    return ip


def url_parse(url):

    url_split = urllib.parse.urlsplit(url=url)
    return url_split.netloc


def Check_url_alive_and_GetInfo(url_list):

    resultlist = []
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}
    url_count = len(url_list)
    process = ''
    count = 0

    for url in url_list:

        process = '{:.2%}'.format(count / url_count)
        
        result = ["www.baidu.com","14.215.177.38","http://www.baidu.com","title_baidu","200","OK","Tengine"] # pre format
        try:
            req = requests.get(url=url,headers=header,timeout=2,verify=False)

            host        = str(url_parse(url)).split(":")[0]
            ip          = get_hostIP(host)
            resp        = req.content
            reason      = req.reason
            status_code = req.status_code
            soup        = BeautifulSoup(resp, 'lxml')
            
            if soup.find_all('title'):
                title = soup.find_all('title')[0].string
            else:
                title = "None_title"
            try:
                server = req.headers['Server']
                if server == None:
                    server = "None_server"

            except:
                # sys.stdout.write("Fail %s Http Server is None\n" % url)
                # print("Error %s Http Server is None"%url)
                server = "None_server"

            result[0] = host
            result[1] = ip
            result[2] = url
            result[3] = title.strip()
            result[4] = status_code
            result[5] = reason.strip()
            result[6] = server.strip()

            resultlist.append(result)


            # print("Success %s get info."%url)
            sys.stdout.write("[%s/%s %s] Success %s get info.\n"%(count,url_count,process,url))
        except Exception as e:
            # print("Error   %s : %s" % (url, e))
            sys.stdout.write("[%s/%s %s] Fail %s : cant't connect or connect timeout.\n" % (count,url_count,process,url))
            # debug option
            # traceback.print_exc()
            
            if url.startswith("http://"):
                url = url.replace("http","https")
                url_list.append(url)
        count = count + 1

    with open(r"result.txt", "w", encoding="utf-8") as resultfile:
        for result in resultlist:
            # print(result)
            resultfile.write(str(result) + "\n")

    return resultlist


def Add_http_header():
    """
    host.txt mayby :
    http://www.xx.com
    https://www.xx.com
    1.1.1.1
    89.50.49.1:443

    :return: url_list
    """
    urls = []
    f = open("host.txt", "r", encoding="utf-8")
    for line in f.readlines():
        urlstr = line.strip()
        if not re.search("^http[s]*://", urlstr):
            if ":443" in urlstr:
                urlstr = "https://" + urlstr
            else:
                urlstr = "http://" + urlstr

        urls.append(urlstr)
    urls = list(sorted(set(urls)))

    return urls


def main():

    httpURLlist = Add_http_header()
    Check_url_alive_and_GetInfo(httpURLlist)


if __name__ == '__main__':
    main()
    result_d.result_d()