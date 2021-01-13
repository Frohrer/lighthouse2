import re
import regexLH
import creditcheck

def readAllText(result):
    allOutput = [];
    countTexts = 0;
    index = 0;

    for files in result['files']:
        text = files['file']['text']
        url = files['file']['url']
        result = scanText(result,text,url)
    for page in result['pages']:
        text = page['text']
        url = page['url']
        result = scanText(result,text,url)
    #print(allOutput[1].url)
    return result;

def scanText(result,text,url):
    y = re.split(',|<|>|\"|\'',str(text))
    for value in y:
        email = re.search(regexLH.reEmail,value)
        phone = re.search(regexLH.rePhone,value)
        social = re.search(regexLH.reSSNbetter,value)
        url1 = re.search(regexLH.reUrl,value)
        pdf = re.search(regexLH.rePDF,value)
        png = re.search(regexLH.rePNG,value)
        jpg = re.search(regexLH.reJPG,value)
        excel = re.search(regexLH.reXLSX,value)
        word = re.search(regexLH.reDOCX,value)
        creditcard = re.search(regexLH.reCC,value)
        if email and result['emailList'].count(email.group()) < 1:
            print(email.group(),'Email from file')
            #print(fileOutput.url)
            result['emailList'].append(email.group())
            result['finds'] += 1;
        if phone and result['phoneList'].count(phone.group()) < 1:
            print(phone.group(),'Phone from file')
            #print(fileOutput.url)
            result['phoneList'].append(phone.group())
            result['finds'] += 1;
        if social and result['ssnList'].count(social.group()) < 1:
            print(social.group(),'SSN from file')
            #print(fileOutput.url)
            result['finds'] += 1;
            ssn = {
                'number':social.group(),
                'url':url
            }
            result['ssnList'].append(ssn)
            result['socials'] += 1;
        if creditcard:
            print(creditcard.group(),'Creditcard')
            if creditcheck.check(creditcard.group()):
                card = {
                    'number':creditcard.group(),
                    'url':url
                }
                result['finds'] += 1;
                result['ccList'].append(card)
                textExist.append(creditcard.group())
                result['creditcards'] += 1;
            else:
                print('Not MOD10',creditcard.group())
    return result
