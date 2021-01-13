# lighthouseFR
-- A sophisticated data-leak scanner --
Lighthouse 2 can crawl websites for Social Security Numbers and other stuff. It can read HTML, PDFs, xlsx, docx, doc and images (using Tesseract OCR) and can find images that you trained it for, for example using IBM Watson Positive/Negative image neural net.

## Features
- Scan recursively based on depth, or scan a whole website.
- Blocklist feature allows you to disregard pages based on a wildcard filter.
- Speedy crawler using multithreading
- Scan files' content using Tesseract
- IBM Image recognition, for example: detect Driver's Licenses, Passports, Social Security Cards using IBM Visual Recognition (Visual deprecated while I was writing this README :( )


## Usage

Download and install dependencies:
```
git clone [link to this]
pip3 install [all packages you need but don't have]
```

Run as unprivileged user
```
python3 lh2.py
```

```
usage: lh2.py [-h] [-d] [-o O] url depth

Scan websites for leaked data.

positional arguments:
  url         The url of the website (including http/s)
  depth       Declare a scanning depth, -1 for infinite scan (Only use without
              flag -d).

optional arguments:
  -h, --help  show this help message and exit
  -d          Scan URLs outside the original domain.
  -o O        Output as JSON file with name specified.
```

## Example .env file
```
#API KEYS
watson-api-key=
watson-classifier-threshold=0.4
watson-classifier-ids=
watson-version=2018-03-19
watson-service-url=https://api.us-south.visual-recognition.watson.cloud.ibm.com

#MISC
user-agent=Lighthouse/2.0.1
exception=site.example.com
verify-tls=False
```

## Example Result

```
{
    "allUrls": [
        {list of urls scanned}
    ],
    "badUrls": [],
    "blacklist": [
        "http://example.com*"
    ],
    "ccList": [],
    "cost": 0.0, //Explains the dollar cost of using Watson API
    "creditcards": 0,
    "documents": {
        "license": [],
        "passport": [],
        "ssn": []
    },
    "emailList": [
        "[redacted]@gmail.com",
        "[redacted]@gmail.com",
        "[redacted]@camahospitalar.med.br",
        "[redacted]@comcast.net"
    ],
    "fileSHAs": [],
    "files": [],
    "finds": 1,
    "fourOhFourUrls": [],
    "pages": [],
    "phoneList": [],
    "scope": "",
    "socials": 1,
    "ssnList": [
        {
            "number": "[redacted]",
            "url": "http://[redacted].blogspot.com/"
        }
    ],
    "startTime": "2021-01-13 00:50:57.455043",
    "stopTime": "2021-01-13 00:51:01.232433",
    "urlAlreadyFollowed": [
        {list of urls}
    ],
    "urlFollowList": [],
    "urlInit": "",
    "urls": 40
}
```
