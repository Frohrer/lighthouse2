import aux_functions
import os,traceback
import re
import argparse
import json
import signal
import sys
import pprint
import regexLH
import creditcheck
import urllib.parse
from urllib.parse import urlsplit
from urllib.parse import urljoin
import allowedExtensions
import datetime
from tld import get_tld
import settings
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()
import logging
# from multiprocessing.pool import ThreadPool
# from multiprocessing import Process
import multiprocessing as mp
import time
import crawler2 as cr
import lhui
import lhfiles
import fileScanner
import textScanner
# import lhparser

result = {
    'urlInit' : '',
    'blacklist' : [],
    'stopTime' : '',
    'startTime' : datetime.datetime.now(),
    'finds' : 0,
    'scope' : '',
    'urls' : 0,
    'pages' : [],
    'allUrls' : [],
    'fourOhFourUrls' : [],
    'urlFollowList' : [],
    'badUrls' : [],
    'urlAlreadyFollowed' : [],
    'socials' : 0,
    'ssnList' : [],
    'ccList' : [],
    'creditcards' : 0,
    'phoneList' : [],
    'emailList' : [],
    'files' : [],
    'fileSHAs' : [],
    'cost' : 0.0,
    'documents' : {
        'ssn':[],
        'passport':[],
        'license':[]
    }
}

def mainLoop(args):
    global result
    startUrl = args.url[0]
    aux_functions.TmpFolder = aux_functions.createTempDir()
    result['blacklist'] = aux_functions.loadBlacklist(settings.BLACKLISTFILE)
    if not cr.getDomainScope(startUrl):
        exit()
    domain = cr.getDomainScope(startUrl)
    # get the first set of URLs from the initial site
    newContentJSON = cr.getUrlsandText(startUrl,domain,result['blacklist'])
    newContent = json.loads(newContentJSON)
    if newContent['isFile']:
        result['files'].append(newContent)
    else:
        result['allUrls'].extend(newContent['links'])
        result['pages'].append(newContent)
    print('Done with initial URL collection')
    print(len(result['allUrls']))
    # result = cr.removeDuplicateUrls(result)
    # print(len(result['allUrls']))
    # result['allUrls'] = getAllUrlsAsync(result['allUrls'],domain)
    previousAmountOfUrls = 0;
    # Main program execution
    if args.depth == -1:
        print('Doing endless scan until all resources have been found.')
        while len(result['allUrls']) != previousAmountOfUrls:
            print(len(result['allUrls']),previousAmountOfUrls)
            result = cr.getAllUrlsAsync(result,domain)
            result = cr.removeDuplicateUrls(result)
            result = lhfiles.removeDuplicateFiles(result)
            result = fileScanner.readAllFiles(result)
            result = textScanner.readAllText(result)
            previousAmountOfUrls = len(result['allUrls'])
            print(previousAmountOfUrls,'previousAmountOfUrls')
    elif args.depth == 0:
        print('Doing one scan, zero depth.')
        result = cr.getOnlyDownloads(result,domain)
        result = cr.removeDuplicatePages(result)
        result = lhfiles.removeDuplicateFiles(result)
        result = fileScanner.readAllFiles(result)
        result = textScanner.readAllText(result)
    elif args.depth >= 1:
        print('Doing more than one scan.')
        for x in range(args.depth):
            result = cr.getAllUrlsAsync(result,domain)
            result = cr.removeDuplicateUrls(result)
            result = lhfiles.removeDuplicateFiles(result)
            result = fileScanner.readAllFiles(result)
            result = textScanner.readAllText(result)

    # result = cr.removeDuplicateUrls(result)

    # for value in result['allUrls']:
    #     print(value['href'])
    print(len(result['allUrls']),'URLs found')
    print(len(result['fourOhFourUrls']),'404 Urls found')
    if args.o:
        lhui.results(result,args)

if __name__ == '__main__':
    try:
        # update_tld_names()
        argParser = argparse.ArgumentParser(description='Scan websites for leaked data.')
        argParser.add_argument('url', nargs=1, help='The url of the website (including http/s)')
        argParser.add_argument('depth', type=int, default=0, help='Declare a scanning depth, -1 for infinite scan (Only use without flag -d).')
        argParser.add_argument('-d', dest='d', action='store_true', help='Scan URLs outside the original domain.')
        argParser.add_argument('-o', dest='o', nargs=1, help='Output as JSON file with name specified.')

        args = argParser.parse_args()

        def signal_handler(sig, frame):
                print('\n\nCTRL+C detected, aborting scan and cleaning up.\n\n')
                # result['stopTime'] = datetime.datetime.now()
                aux_functions.deleteFiles()
                aux_functions.deleteTempDir(aux_functions.TmpFolder)
                aux_functions.TmpFolder = ''
                sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        mainLoop(args)
    except Exception as e:
        print('[main]',e)
        traceback.print_exc(file=sys.stdout)
    finally:
        print('Cleaning up.')
        if aux_functions.TmpFolder:
            aux_functions.deleteFiles()
            aux_functions.deleteTempDir(aux_functions.TmpFolder)
        exit()
