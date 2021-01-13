import random
import os
from os import walk
import shutil
import hashlib

def loadBlacklist(filename):
    try:
        path, fl = os.path.split(os.path.realpath(__file__))
        filename = os.path.join(path, filename)
        with open(filename, 'r') as f:
            blacklist = []
            for line in f:
                blacklist.append(line.rstrip())
            return blacklist
    except:
        return []

def isMatch(s, p):
    sl = len(s)
    pl = len(p)
    dp = [[False for i in range(pl+1)] for j in range(sl+1)]
    s = " "+s
    p = " "+p
    dp[0][0]=True
    for i in range(1,pl+1):
        if p[i] == '*':
            dp[0][i] = dp[0][i-1]
    for i in range(1,sl+1):
        for j in range(1,pl+1):
            if s[i] == p[j] or p[j] == '?':
                dp[i][j] = dp[i-1][j-1]
            elif p[j]=='*':
                dp[i][j] = max(dp[i-1][j],dp[i][j-1])
    return dp[sl][pl]

def getHash(filename):
    BUF_SIZE = 65536  #declare buffer size for chunks sizes
    # md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            # md5.update(data)
            sha1.update(data)
    return sha1.hexdigest()

def getStringHash(string):
    sha1 = hashlib.sha1()
    string = string.encode('utf-8')
    sha1.update(string)
    return sha1.hexdigest()

def createTempDir():
    tmp = str(random.randint(1,99999))+'tmp/';
    path, fl = os.path.split(os.path.realpath(__file__))
    TmpFolder = os.path.join(path, tmp)
    try:
        os.mkdir(TmpFolder)
    except OSError:
        print ("Creation of the directory %s failed" % TmpFolder)
    else:
        print ("Successfully created the directory %s " % TmpFolder)
    return TmpFolder

#Declare tmp folder which is always absolute to the installation path of lighthouseFR, never relative to where it is run.
TmpFolder = '';

def deleteTempDir(path):
    try:
        os.rmdir(path)
    except OSError:
        print ("Deletion of the directory %s failed" % path)
    else:
        print ("Successfully deleted the directory %s" % path)

def deleteFiles():
    for the_file in os.listdir(TmpFolder):
        file_path = os.path.join(TmpFolder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def deleteOneFile(the_file):
    file_path = os.path.join(TmpFolder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)
