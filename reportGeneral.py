# coding:utf-8

"""
first run you shuld run testrun.py to download chromium
[W:pyppeteer.chromium_downloader] chromium extracted to: C:\\Users\\Administrator\\AppData\\Local\\pyppeteer\\pyppeteer\\local-chromium\\588429
"""

import asyncio
from pyppeteer import launch
import time

global info
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
html_header_m = """<!DOCTYPE html>
<head>
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
  <link href="../static/css/main.css" rel="stylesheet" type="text/css">
  <title>WebSite Info Report</title>
</head>
<body style="padding-right: 320px;">
  <div class="main-inner">
    <div id="posts" class="posts-expand">
      <header class="post-header">
        <h1 class="post-title" itemprop="name headline">WebSite Info Report</h1>
        <div class="post-meta">
          <span class="post-time">
            <span class="post-meta-item-text">Create by</span>
            <time title="Post created" itemprop="dataCreated datePublished">CreateTimeToReplace</time></span>
        </div>
      </header>
      <div class="post-body" itemprop="articleBody"></div>

"""

htmldir_begin = """
        <aside id="sidebar" class="sidebar sidebar-active" style="display: block; width: 320px;">
          <div class="sidebar-inner">
            <ul class="sidebar-nav motion-element" style="opacity: 1; display: block; transform: translateX(0px);">
              <li class="sidebar-nav-toc sidebar-nav-active" data-target="post-toc-wrap">目录</li></ul>
            <!--noindex-->
            <section class="post-toc-wrap motion-element sidebar-panel sidebar-panel-active" style="opacity: 1; display: block; transform: translateX(0px);">
              <div class="post-toc" style="max-height: 750px; width: calc(100% + 0px);">
                <div class="post-toc-content">
                  <ol class="nav">
  """


htmldir_end = """
                    <li class="nav-item nav-level-1">
                        <a class="nav-link" href="###host##">
                            <span class="nav-number">##number##.</span>  
                            <span class="nav-text">##host##</span></a>
                    </li>
"""

async def screenshot(url):
    browser = await launch({'headless': True,
                            'args': [
                                '--disable-extensions',
                                '--disable-infobars',
                                '--hide-scrollbars',
                                '–disable-dev-shm-usage',
                                '--mute-audio',
                                '–disable-setuid-sandbox',
                                '–no-sandbox',
                                '–no-zygote',
                                '--window-size=1024,768',
                                '--disable-gpu',
                            ],
                            'dumpio': True,
                            'ignoreHTTPSErrors': True,
                            'executablePath': 'C:\\Users\Administrator\\AppData\\Local\\pyppeteer\\pyppeteer\\local-chromium\\588429\\chrome-win32\\chrome.exe'})
    page = await browser.newPage()
    await page.goto(url, timeout=10000)
    await page.setViewport({'width': 1000, 'height': 698})
    await page.waitFor(1000)
    imageName = url.replace("https://", "").replace("http://", "").replace("/", "").replace(":","") + ".png"
    await page.screenshot({'path': './images/' + imageName})
    await browser.close()

    return imageName


def main():

    createtime = str(time.asctime(time.localtime(time.time())))

    html_header = html_header_m.replace("CreateTimeToReplace",createtime)

    reportFile = str(time.strftime("WebSiteReportBy_%Y%m%d_%H%M%S")) + ".html"

    infolist = []

    with open("result.txt","r",encoding="utf-8") as resultfile:
        for infoliststr in resultfile.readlines():
            info = eval(infoliststr.strip())
            infolist.append(info)

    number = 0
    htmlend = ""
    htmlinfo = ""
    for info in infolist:

        host        = info[0]
        ip          = info[1]
        url         = info[2]
        title       = info[3]
        status_code = info[4]
        reason      = info[5]
        server      = info[6]

        server_status_code_reason = "Server : " + server + "&nbsp;Status : " + str(status_code) + reason

        """screen website picture"""

        tmp = """<h1 id="##host##">##title##</h1>
          <a href="##url##" target="_blank">##url##</a></br>
          <a>IP: ##ip##</a></br>
          <a>##server_status_code_reason##</a></br>
          <img src="../images/##xxx.png##">
          </br>
          
          """

        try:
            print("Start deal %s "%url)
            picname = asyncio.get_event_loop().run_until_complete(screenshot(url))

            tmp = tmp.replace("##host##",host).replace("##title##",title).replace("##url##",url)\
                .replace("##ip##",ip).replace("##server_status_code_reason##",server_status_code_reason).\
                replace("##xxx.png##",picname)
            htmlinfo += tmp

            number +=1
            htmlend += htmldir_end.replace("##host##",host).replace("##number##",str(number)) + "\n"
        except Exception as e:
            print(e)

    htmlresult = html_header + htmlinfo + htmldir_begin + htmlend
    with open("./reports/" + reportFile, "a", encoding="utf-8") as f:
        f.write(htmlresult)


if __name__ == '__main__':
    main()