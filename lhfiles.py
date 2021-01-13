import urllib.parse
from urllib.parse import urlparse
import mimetypes
import random
import os
import aux_functions

downloadableFileCats = ['application','image']
directFileCats = ['text','font','message']

downloadableFileTypes = ['pdf','xls','xlsx','doc','docx','png','jpg','jpeg','jpe','tif','tiff','ico']

def isScanableFile(url,content_type):
    parsed = urlparse(url)
    realUrl = parsed.scheme+'://'+parsed.netloc+parsed.path
    extension = mimetypes.guess_extension(content_type,True)
    extension2 = mimetypes.guess_type(realUrl,True)
    print(extension2,extension)
    category = extension2[0].split('/')[0] if extension2[0] != None else None
    type = extension.split('.')[1] if extension != None else None
    if category in downloadableFileCats:
        if type in downloadableFileTypes:
            return True
    return False

def likelyScannableURL(url):
    parsed = urlparse(url)
    realUrl = parsed.scheme+'://'+parsed.netloc+parsed.path
    extension2 = mimetypes.guess_type(realUrl,True)
    category = extension2[0].split('/')[0] if extension2[0] != None else None
    if category in downloadableFileCats:
        return True
    return False

def isTextFile(url,content_type):
    parsed = urlparse(url)
    realUrl = parsed.scheme+'://'+parsed.netloc+parsed.path
    extension2 = mimetypes.guess_type(realUrl,True)
    category = extension2[0].split('/')[0] if extension2[0] != None else None
    if category in directFileCats:
        return True
    return False

def download(url,page):
    content_type = page.headers['content-type']
    extension = mimetypes.guess_extension(content_type,True)
    extension2 = mimetypes.guess_type(url,True)
    print(extension,extension2,url)
    if extension == '.jpe':
        extension = '.jpg';
    if extension:
        filename = str(random.randint(1,99999)) + extension;
        saveAs = os.path.join(aux_functions.TmpFolder, filename)
        # print(filename)
        with open(saveAs,'wb') as f:
                #write the contents of the response (r.content)
                # to a new file in binary mode.
                f.write(page.content)
        sha1 = aux_functions.getHash(saveAs)
        file = {
            'name':filename,
            'scanned':False,
            'url':url,
            'sha1':sha1,
            'type':extension,
            'text':''
        }
        return file;

def removeDuplicateFiles(result):
    tempHashes = []
    for file in result['files']:
        if file['sha1'] in tempHashes:
            fileLoc = os.path.join(aux_functions.TmpFolder, file['name'])
            aux_functions.deleteOneFile(fileLoc)
        else:
            tempHashes.append(file['sha1'])
    return result
