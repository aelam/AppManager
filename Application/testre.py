#coding=utf-8
#
import zipfile,re


def func():
    print "HELLO:"
    zip = zipfile.ZipFile("/Users/ryan/Desktop/fiveStar/FiveStar.zip",'r')
#    valid = re.compile(r"^payload\/*(\w+).app\/info.plist")
#    valid = re.compile(r"^payload")
#    for name in zip.namelist():
#        if valid.match(name):
#            print "YAY"
       # print name

    l = (
        "Payload/1231231.app/Info.plist",
        "Payload/123 1231.app/Info.plist",
        "Payload/23中33文.app/Info.plist",
        "Payload/23中33文.app/Info.plist",
        "Payload/12 3.app/1231.app/Info.plist",
        "Payload/123.app/1231.app/Info.plist",
        "Payload/app/.app/Info.plist",
    )


    valid = re.compile(r"^Payload\/[^\/]+.app\/Info.plist$",re.IGNORECASE)
    for i in l:
        m = valid.match(i)
        if m:
            print m.group()
        else:
            print "None:" + i

if __name__ == "__main__":
    func()
