"""
Originally written by tevslin.
Modified and repackaged for use in this docker image by ccmpbll.

no arguments required:
--debug write trace of io using logger (default does not)
--json  output written to sysout is json rather than formatted text
"""
try:
    from . import cfspeedtestclass
except:
    import cfspeedtestclass
    import json
    import argparse

def main():

    parser=argparse.ArgumentParser(
        description='Runs speed test of net connection using ping and Cloudflare')
    parser.add_argument('--debug',action='store_true',help='log network io')
    parser.add_argument('--json',action='store_true',help='write json to sysout instead of formatted results')
    args=parser.parse_args()

    speedtest=cfspeedtestclass.cloudflare(debug=args.debug,printit=(not args.json)) #reopen with correct params
    dict=speedtest.runalltests()
    if args.json:
        print (json.dumps(dict))

main()
