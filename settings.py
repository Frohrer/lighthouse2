from dotenv import load_dotenv
import os
load_dotenv()

# The blacklist file must be loaded in the root directory of this script.
BLACKLISTFILE = "blacklist.txt"
USERAGENT = os.getenv("user-agent")
WATSON_API_KEY = os.getenv("watson-api-key")
WATSON_VERSION = os.getenv("watson-version")
WATSON_SERVICE_URL = os.getenv("watson-service-url")
WATSONTHRESHOLD = os.getenv("watson-classifier-threshold")
WATSONCLASSIFIERID = os.getenv("watson-classifier-ids")
VERIFYTLS = os.getenv("verify-tls")
