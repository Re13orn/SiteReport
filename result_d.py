import sys
import time

def result_d():
    infolist = []
    with open("result.txt", "r", encoding="utf-8") as resultfile:
        for infoliststr in resultfile.readlines():
            info = eval(infoliststr.strip())
            infolist.append(info)
    filename="./reports/txt/" + str(time.strftime("WebSiteReportBy_%Y%m%d_%H%M%S")) + ".txt"
    f = open(filename,"a+",encoding="utf-8")
    for info in infolist:
        resu = "\t".join(str(i) for i in info) + "\n"
        f.write(resu)
        sys.stdout.write(resu)
    print("[*] result is in file {} ".format(filename))
    f.close()

if __name__ == '__main__':
    result_d()