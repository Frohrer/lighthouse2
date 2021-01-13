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
from urllib.parse import urlparse
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
import lhfiles

# moduleReturn = {
#     'allUrlsInModule':[],
#     'fourOhFourUrlsInModule':[]
# }

def getDomainScope(url):
    try:
        res = get_tld(url, as_object=True,fix_protocol=True)
        return res.fld
    except:
        return False

def isSameDomain(url,domain):
    if (not url or not domain):
        return False
    if (url == None or domain == None):
        return False
    if getDomainScope(url) == getDomainScope(domain):
        return True
    return False

def validateUrl(url,href,domain):
    pass

def blacklisted(url,blacklist):
    for entry in blacklist:
        if aux_functions.isMatch(url,entry):
            return True
        else:
            continue
    return False

def removeDuplicatePages(result):
    duplicatePages = {}
    for i,page in enumerate(result['pages']):
        try:
            if duplicatePages[page['sha1']] == page['url']:
                del result['pages'][i]
                print('deleted',i)
            else:
                duplicatePages[page['sha1']] = page['url']
        except KeyError:
            duplicatePages[page['sha1']] = page['url']
        print(duplicatePages)
    return result

def removeDuplicateUrls(result):
    result['allUrls'] = list(dict.fromkeys(result['allUrls']))
    # for entry in allUrls:
    #     # href = entry.replace("/","")
    #     # if href in result['urlAlreadyFollowed']:
    #     #     result['allUrls'].remove(entry)
    #     # el
    #     if entry in result['urlAlreadyFollowed']:
    #         print('removing', entry)
    #         result['allUrls'].remove(entry)
    #     # else:
    #     #     result['urlAlreadyFollowed'].append(entry)
    return result

# bing = [{'href':'http://lagottobreeders.org/'},{'href':'http://lagottobreeders.org'}]
# print(removeDuplicateUrls(bing))

def savePageOrDocument(returnpage,page,url):
    if 'text/html' in page.headers['Content-Type']:
        returnpage['page'] = page
    elif lhfiles.isScanableFile(url,page.headers['Content-Type']):
        # download the file
        returnpage['file'] = lhfiles.download(url,page)
        returnpage['scanableFile'] = True
    elif lhfiles.isTextFile(url,page.headers['Content-Type']):
        returnpage['page'] = page
    returnpage['statuscode'] = page.status_code
    return returnpage

def connectToUrl(url,domain):
    headers = {'user-agent': settings.USERAGENT}
    timeout = 8
    returnpage = {
        'statuscode':'',
        'file':'',
        'scanableFile':False,
        'error':False,
        'errorDesc':'',
        'page':''
    }
    try:
        page = requests.get(url,headers=headers,timeout=timeout,verify=False)
    except requests.ConnectionError:
        returnpage['error'] = True
        returnpage['errorDesc'] = 'ConnectionError'
        return returnpage
    except requests.TooManyRedirects:
        returnpage['error'] = True
        returnpage['errorDesc'] = 'TooManyRedirects'
        return returnpage
    except requests.ReadTimeout:
        returnpage['error'] = True
        returnpage['errorDesc'] = 'ReadTimeout'
        return returnpage
    if page.status_code != requests.codes.ok:
        returnpage['error'] = True
        returnpage['errorDesc'] = 'BadStatusCode'
        return returnpage

    if len(page.history) > 1 and len(page.history) < 30:
        print('Page history > 1')
        if isSameDomain(page.history[len(page.history)-1].url,domain):
            print('Redirect to same domain, keeping page')
            page = page.history[len(page.history)-1]
            returnpage = savePageOrDocument(returnpage,page,url)
            return returnpage
    elif len(page.history) > 30:
        returnpage['error'] = True
        returnpage['errorDesc'] = 'TooManyRedirects'
        return returnpage
    else:
        returnpage = savePageOrDocument(returnpage,page,url)
        return returnpage


def getUrlsandText(url,domain,blacklist):
    returnpage = connectToUrl(url,domain)
    page = returnpage['page']
    returnpage['page'] = '';
    links = []
    hrefs = []
    contents = {
        'status' : 'Unavailable',
        'error' : True,
        'isFile' : False,
        'text' : '',
        'title' : '',
        'sha1' : '',
        'url' : '',
        'parsedurl':'',
        'links':links,
        'request':returnpage
    }
    if returnpage == False or not returnpage:
        contentJSON = json.dumps(contents)
        return contentJSON

    if returnpage['error'] == True:
        contentJSON = json.dumps(contents)
        return contentJSON

    if returnpage['scanableFile'] == True:
        file = returnpage['file']
        returnpage['file'] = '';
        contents = {
            'status' : returnpage['statuscode'],
            'error' : False,
            'isFile' : True,
            'text' : '',
            'title' : '',
            'sha1' : file['sha1'],
            'url' : url,
            'parsedurl':urlparse(url),
            'request':returnpage,
            'file':file
        }
        contentJSON = json.dumps(contents)
        return contentJSON

    try:
        soup = BeautifulSoup(page.text, 'html.parser')
        for link in soup.find_all('a',href=True):
            hrefs.append(link.get('href'))
        for link in soup.find_all('img',src=True):
            hrefs.append(link.get('src'))
        for href in hrefs:
            if (href == None) or (not href):
                continue;
            if (href.startswith('#') == True):
                continue;
            if blacklisted(href,blacklist):
                continue;
            if (href.startswith('/') == True):
                href = urljoin(url, href)
            if (getDomainScope(href) == False):
                href = urljoin(url, href)
            if isSameDomain(href,domain):
                links.append(href)

        contents.update({
            'status' : returnpage['statuscode'],
            'error' : False,
            # 'htmlAll' : soup.find_all(),
            'text' : soup.get_text(),
            'title' : soup.title.string if soup.title else 'NO TITLE',
            'sha1' : aux_functions.getStringHash(soup.get_text()),
            'parsedurl':urlparse(url),
            'url' : url,
            'request':returnpage,
            'links':links
        })
    except Exception as e:
        print('[getUrlsandText]',e)

    contentJSON = json.dumps(contents)
    return contentJSON

def getAllUrlsOnce(result,domain): #Collect pages and files without adding new links
    processesAmount = 4
    crawlPool = mp.Pool(processes=processesAmount)
    for entry in result['allUrls']:
        if entry in result['urlAlreadyFollowed']:
            continue;
        if blacklisted(entry,result['blacklist']):
            print('This url is blacklisted')
            continue;
        # crawlPool.apply_async(thread_function, (entry['href'],domain,), callback = getNewUrls)
        result['urlAlreadyFollowed'].append(entry)
        print('Now scanning',entry)
        newContentJSON = crawlPool.apply(getUrlsandText, (entry,domain,result['blacklist'],))
        newContent = json.loads(newContentJSON)
        if newContent['isFile']:
            result['files'].append(newContent)
        else:
            result['pages'].append(newContent)
    crawlPool.close()
    crawlPool.join()
    return result

def getOnlyDownloads(result,domain):
    processesAmount = 4
    crawlPool = mp.Pool(processes=processesAmount)
    for entry in result['allUrls']:
        if entry in result['urlAlreadyFollowed']:
            continue;
        if blacklisted(entry,result['blacklist']):
            print('This url is blacklisted')
            continue;
        if not lhfiles.likelyScannableURL(entry):
            continue;
        # crawlPool.apply_async(thread_function, (entry['href'],domain,), callback = getNewUrls)
        result['urlAlreadyFollowed'].append(entry)
        print('Now scanning',entry)
        newContentJSON = crawlPool.apply(getUrlsandText, (entry,domain,result['blacklist'],))
        newContent = json.loads(newContentJSON)
        if newContent['isFile']:
            result['files'].append(newContent)
        else:
            result['pages'].append(newContent)
    crawlPool.close()
    crawlPool.join()
    return result

def getAllUrlsAsync(result,domain):
    processesAmount = 4
    crawlPool = mp.Pool(processes=processesAmount)
    # crawlPool = Pool(processes=processesAmount)
    for entry in result['allUrls']:
        if entry in result['urlAlreadyFollowed']:
            continue;
        if blacklisted(entry,result['blacklist']):
            print('This url is blacklisted')
            continue;
        # crawlPool.apply_async(thread_function, (entry['href'],domain,), callback = getNewUrls)
        result['urlAlreadyFollowed'].append(entry)
        newContentJSON = crawlPool.apply(getUrlsandText, (entry,domain,result['blacklist'],))
        newContent = json.loads(newContentJSON)
        if newContent['isFile']:
            result['files'].append(newContent)
        else:
            result['allUrls'].extend(newContent['links'])
            result['pages'].append(newContent)
    crawlPool.close()
    crawlPool.join()
    return result
