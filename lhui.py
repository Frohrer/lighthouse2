import datetime
import json

def results(result,args):
    result['stopTime'] = datetime.datetime.now()
    with open(args.o[0], 'w') as dumpfile:
        json.dump(result, dumpfile, indent=4, sort_keys=True, default=str)
    # if result['finds'] <= 0 and result['urls'] <= 0:
    #     print('Nothing found.')
    # else:
    #     print('Found '+str(result['finds'])+' uncommon objects and '+str(result['urls'])+' urls on '+result['urlInit'])
    #     #print(result['phoneList'],result['emailList'],result['ssnList'],result['documents'])
    #     if result['socials'] > 0:
    #         print('--- Social Security Number(s) found ---')
    #         print('The following might be one or more valid SSNs:')
    #         for social in result['ssnList']:
    #             print(social['number'],social['url'])
    #         print(result['documents'])
    #
    # if args.o:
    #     fileData = {}
    #     fileData['startTime'] = str(result['startTime']);
    #     fileData['stopTime'] = str(datetime.datetime.now());
    #     fileData['socials'] = result['ssnList'];
    #     fileData['creditcards'] = result['ccList'];
    #     fileData['phones'] = result['phoneList'];
    #     fileData['emails'] = result['emailList'];
    #     fileData['documents'] = result['documents'];
    #     fileData['badUrls'] = result['badUrls'];
    #     fileData['numberofUrls'] = result['urls'];
    #     fileData['numberofUrlsFollowed'] = int(len(result['urlAlreadyFollowed']));
    #
    #     with open(args.o[0], 'a') as outfile:
    #         json.dump(fileData, outfile)
