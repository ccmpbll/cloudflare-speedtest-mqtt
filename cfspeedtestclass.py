"""
Originally written by tevslin.
Modified and repackaged for use in this docker image by ccmpbll.

class object for connection testing with requests to speed.cloudflare.com
runs tests and stores results in dictionary
cloudflare(dict=None,debug=False,print=True,downtests=None,uptests=None,latencyreps=20)
dict: dictionary to store results in
    if not passed in, created here
    if passed in, used and update - allows keeping partial results from previous runs
    each result has a key and the entry is a dict with "time" and "value" items
debug: True turns on io logging for debugging
printit: if true, results are printed as well as added to the dictionary
downtests: tuple of download tests to be performed
    if None, defaultdowntests (see below) is used
    format is ((size, reps, label)......)
        size: size of block to download
        reps: number of times to repeat test
        label: text label for test - also becomes key in the dict
uptests: tuple of upload tests to be performed
    if None, defaultuptests (see below) is used
    format is ((size, reps, label)......)
        size: size of block to upload
        reps: number of times to repeat test
        label: text label for test - also becomes key in the dict
latencyreps: number of repetitions for latency test
"""

class cloudflare:
    #tests changed 1/1/22 to mirror those done by web-based test
    uploadtests=((101000,8,'100kB'),(1001000, 6,'1MB'),(10001000, 4,'10MB'))
    downloadtests=((101000, 10,'100kB'),(1001000, 8,'1MB'),(10001000, 6,'10MB'),(25001000, 4,'25MB'))
    version="1.7.1"
    def __init__(self,dict=None,debug=False,printit=True,downtests=None,uptests=None,latencyreps=20,timeout=(3.05,25)):

        import requests

        if debug:
            import logging
            # Enabling debugging at http.client level (requests->urllib3->http.client)
            # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
            # the only thing missing will be the response.body which is not logged.
            try: # for Python 3
                from http.client import HTTPConnection
            except ImportError:
                from httplib import HTTPConnection
            HTTPConnection.debuglevel = 1
            logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

        self.debug=debug
        self.printit=printit
        self.latencyreps=latencyreps
        self.dict={} if dict is None else dict
        if not downtests is None:
            self.downloadtests=downtests
        if not uptests is None:
            self.uploadtests=uptests
        self.mequests=requests.Session()
        self.timeout=timeout

    def getcolo(self):
    #retrieves cloudflare colo and user ip address
        r=self.mequests.get('http://speed.cloudflare.com/cdn-cgi/trace')
        dicty={}
        for lines in r.text.splitlines():
            words=lines.split("=")
            dicty[words[0]]=words[1]
        return dicty['colo'],dicty['ip']

    def getcolodetails(self,colo):
        #retrieves colocation list for cloudflare
        r=self.mequests.get('http://speed.cloudflare.com/locations')
        for locs in r.json():
            if locs['iata']==colo: #if match found
                return(locs['region'],locs['city'])
        return ("not found","not found")

    def download(self,numbytes,iterations):
        #runs download tests
        import time
        fulltimes=() #list for all successful times
        servertimes=() #times reported by server
        requesttimes=() #rough proxy for ttfb
        for i in range(iterations):
                start=time.time()
                err=False
                try:
                    r=self.mequests.get('http://speed.cloudflare.com/__down?bytes='+str(numbytes),timeout=self.timeout)
                    end=time.time()
                except:
                    err=True
                if not err:
                    fulltimes=fulltimes+(end-start,)
                    servertimes=servertimes+(float(r.headers['Server-Timing'].split('=')[1])/1e3,)
                    requesttimes=requesttimes+(r.elapsed.seconds+r.elapsed.microseconds/1e6,)
        return (fulltimes,servertimes,requesttimes)

    def upload(self,numbytes,iterations):
        #runs upload tests
        servertimes=() #times reported by server
        thedata=bytearray(numbytes)
        for i in range(iterations):
            err=False
            try:
                r=self.mequests.post('http://speed.cloudflare.com/__up',data=thedata,timeout=self.timeout)
            except:
                err=True
            if not err:
                servertimes=servertimes+(float(r.headers['Server-Timing'].split('=')[1])/1e3,)
        return (servertimes)

    def sprint(self,label,value):
        "time stamps entry and adds to dictionary replacing spaces with underscores in key and optionally prints"
        import time
        if self.printit:
            print(label+":",value)
        self.dict[label.replace(' ','_')]={"time":time.time(),"value":value} #add to dictionary

    def runalltests(self):
        #runs full suite of tests
        import numpy as np

        self.sprint('version',self.version)
        colo,ip=self.getcolo()
        self.sprint('your ip',ip)
        self.sprint('test location code',colo)
        region,city=self.getcolodetails(colo)
        self.sprint ('test location city',city)
        self.sprint ('test location region',region)
        fulltimes,servertimes,requesttimes=self.download(1,self.latencyreps) #measure latency and jitter
        latencies=np.subtract(requesttimes,servertimes)*1e3
        jitter=np.median([abs(latencies[i]-latencies[i-1]) for i in range(1,len(latencies))])
        self.sprint ('latency ms',round(np.median(latencies),2))
        self.sprint ('Jitter ms',round(jitter,2))

        alltests=()

        for tests in self.downloadtests:
            fulltimes,servertimes,requesttimes=self.download(tests[0],tests[1])
            downtimes=np.subtract(fulltimes,requesttimes)
            downspeeds=(tests[0]*8/downtimes)/1e6
            self.sprint(tests[2]+' download Mbps',round(np.mean(downspeeds),2))
            for speed in downspeeds:
                alltests=alltests+(speed,)

        self.sprint('90th percentile download speed',round(np.percentile(alltests,90),2))

        alltests=()
        for tests in self.uploadtests:
            servertimes=self.upload(tests[0],tests[1])
            upspeeds=(tests[0]*8/np.asarray(servertimes))/1e6
            self.sprint(tests[2]+' upload Mbps',round(np.mean(upspeeds),2))
            for speed in upspeeds:
                alltests=alltests+(speed,)

        self.sprint('90th percentile upload speed',round(np.percentile(alltests,90),2))
        return(self.dict)
