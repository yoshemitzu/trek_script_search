import urllib2,BeautifulSoup,pickle

trekdict = {}
trekseries = ['ds9','voyager','NextGen',
              'StarTrek','Enterprise',"movies"]

for _series in trekseries:
    trekdict[_series] = {}

def EpGet(series):
    global trekdict
    """ Valid series arguments: 'ds9','NextGen','StarTrek','Enterprise','voyager' """
    
    parenturl = "http://www.chakoteya.net/"+series+"/"

    if series == "movies":
        transmain = parenturl+"index.htm"
    elif series != 'voyager':
        transmain = parenturl+"episodes.htm"
    else:
        transmain = parenturl+"episode_listing.htm"
##    print transmain
    transpage = urllib2.urlopen(transmain)

    soup = BeautifulSoup.BeautifulSoup(transpage.read())
    
    links = []

##    _links = soup.findAll("a")
##    print _links

    for link in soup.findAll("a"):
        eplink = link.get("href")
        epname = str(link.string)
        if epname != "None" and epname != None and epname != "Andromeda" and "Index" not in epname:

            trekdict[series][epname] = {}
            if eplink != None:
                linkcheck = len(eplink)
                print eplink
                if "movie" in eplink:
                    
    ##            if linkcheck < 10 and "To be continued" not in eplink and "index" not in eplink:
    ##                # these episodes are posted twice in the links,
    ##                # but direct to different sections of the same page
                    links.append((eplink,epname))

    errorfile = open("trektext\\"+series+"fail.txt","w")

    epgot = 0
    epnot = 0

    for _eps in links:
        eplink = _eps[0]
        epname = _eps[1]
        epurl = parenturl + str(eplink)

        # this is to indicate progress
        print epurl

        eppage = urllib2.urlopen(epurl)
        soup = BeautifulSoup.BeautifulSoup(eppage.read())

        body = soup.findAll("div")[0]

        try:
            if epname != "None" and epname != "Andromeda" and "Index" not in epname:
                trekdict[series][epname]["transcript"] = body.text
##            trekfile.write(body.text)
            epgot += 1
        except:
##            errorfile.write(str(epurl)+"\n")
            epnot += 1

    errorfile.close()

    print "Transcript download complete."
    print str(epgot)+" episodes successfully retrieved."
    print str(epnot)+" episodes presented errors."

if __name__ == "__main__":
    picklefile = open("trektext\\trekdict1.txt","w")

    EpGet("movies")    

##    for _series in trekseries:
##        EpGet(_series)

    pickle.dump(trekdict,picklefile)
    picklefile.close()



__all__ = ["EpGet"]
