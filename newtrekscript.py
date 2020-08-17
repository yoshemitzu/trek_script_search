import urllib2,time

site = "http://www.chakoteya.net/"

def MovieCheck(text):
    if "movie" in text:
        return True
    return False

def TOSCheck(text):
    if ".htm" in text:
        return True
    return False

def VOYCheck(text):
    if "continue" in text or "Continue" in text:
        return False
    return True

def NullCheck(text=""):
    return True

def GetLinks(pagetext,Check=NullCheck):
    linkdict = {}
    starttext = "<a href="
    endtext = ">"
    startpos = 0
    while True:
        startlink = pagetext.find(starttext,startpos,len(pagetext))
        startpos = startlink + 1
        if startpos == 0:
            break
        endlink =pagetext.find(endtext,startlink)
        link = site+pagetext[startlink+len(starttext)+1:endlink-1]

        if Check(link):

            fontstart = pagetext.find("<font",endlink)
            textstart = pagetext.find(">",fontstart)
            fontend = pagetext.find("</font",textstart)

            name = pagetext[textstart+1:fontend]
            if len(name) < 200:
                name = " ".join(name.split())
                linkdict[name] = link
##                print link,name
    return linkdict

trekurls =  [("http://www.chakoteya.net/movies/index.htm",MovieCheck,"movies"),
          ("http://www.chakoteya.net/StarTrek/episodes.htm",TOSCheck,"StarTrek"),
          ("http://www.chakoteya.net/NextGen/episodes.htm",NullCheck,"NextGen"),
          ("http://www.chakoteya.net/DS9/episodes.htm",NullCheck,"DS9"),
          ("http://www.chakoteya.net/Voyager/episode_listing.htm",VOYCheck,"Voyager"),
          ("http://www.chakoteya.net/Enterprise/episodes.htm",NullCheck,"Enterprise")]

for _trektuple in trekurls:
    _url = _trektuple[0]
    _checkmethod = _trektuple[1]
    page = urllib2.urlopen(_url)
    text = page.read()
    a = GetLinks(text,_checkmethod)
    trekfile = open("trekfile.txt","w")
    trekstring = ""
    for link in a:
        a[link] = a[link].replace(".net/",".net/"+_trektuple[2]+"/")
        print a[link]
        eppage = urllib2.urlopen(a[link])
        trekstring += eppage.read()
        print "epstring appended"
        time.sleep(1)
    trekfile.write(trekstring)
    
