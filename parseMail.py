import uuid
import datetime
import base64
import quopri
from email.header import decode_header
import pprint
#from utils import timestamp_dict


import logging
from logging.handlers import RotatingFileHandler

h = RotatingFileHandler('/home/developer/newdev/logs/mailIn.log',maxBytes=100000000, backupCount=12)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(h)
def mail_parse(text):

    words = ['Message-ID', 'From', 'Subject', 'Date', 'subject','date', 'from']
    result ={'origTextLen':len(text) }
    body=[]

    lines = text.splitlines()
    currentLine = 0
    for line in lines:
        if(len(line.strip()) == 0):
            print(".....")
        else:
            line = line.strip()
            for word in words:
                if(line.startswith(word)):
                    result[word] = line[(len(word)+1):].strip()

            if 'boundary' not in result:
                b = parse_boundary(line)
                if b is not None:
                    result['boundary'] = b

            elif('boundary'  in result and result['boundary'] is not None and line == "--{}".format(result['boundary'])):
                encoding, body_ = parse_body(currentLine, line, lines, result['boundary'])
                if body_ is not None:
                    result["Body"] = body_
                    result["Content-Transfer-Encoding"] = encoding

        currentLine = currentLine + 1

    if 'Message-ID' not in result:
 result['Message-ID'] = uuid.uuid4().hex

    #update result with date and time parts
    result.update(timestamp_dict())

    try:
        fix_subject(result)
        fix_from(result)
    except Exception as subex:
        print(subex)

    return result




def parse_body(currentLine, line, lines, boundary):
    offset=1
    nextFirstLine = lines[currentLine+1]
#    if nextFirstLine.startswith("Content-Type"):
    encoding = None
    indexPlainText = nextFirstLine.find("text/plain")
    if indexPlainText == -1:
        return encoding, None
    else:
        offset = offset + 1

    nextOfNextLine = lines[currentLine+2]
    if nextOfNextLine.startswith("Content-Transfer-Encoding"):
        encoding = nextOfNextLine.split(':')[1].strip()
        offset = offset + 1
    textLines=lines[currentLine + offset:]
    actualText=[]
    for txtLine in textLines:
        if txtLine == "--{}".format(boundary) or txtLine == "--{}--".format(boundary):
            break
        else:
            actualText.append(txtLine)
    text = "\r\n".join(actualText)
    logger.info("text found")
    logger.info(text)
    logger.info("~"*8)
    #deal with encoding
    if encoding == "base64":
        text = base64.b64decode(text)
    #elif encoding == "7bit" or encoding == "8bit":
    #    text = quopri.decodestring(text)
    elif encoding == "quoted-printable":
        try:
            text = quopri.decode(text)
        except:
            pass
    elif encoding == "uuencode" or encoding == "x-uuencode" or encoding == "uue" or encoding == "x-uue":
        text = uu.decode(text)




    return encoding, text

def parse_boundary(line):
    boundaryIndex = line.find("boundary")
    boundaryText = None
    if boundaryIndex != -1:
       logger.info("yay found a boundary")
       boundaryText = line[boundaryIndex-1:]
       if boundaryText.find("="):
           logger.info("yay found a boundry with =")
       else:
           return None

       boundaryText = boundaryText.split('=')
       print(boundaryText)
       if len(boundaryText) > 0:

           try:
               boundaryText = boundaryText[1]
           except IndexError as iex:
               logger.info(boundaryText)
               logger.warn(iex)
               return None

       if boundaryText.startswith('"'):

           boundaryText = boundaryText[1:]
       if boundaryText.endswith('"'):
           boundaryText = boundaryText[:-1]
    print(boundaryText)
    return boundaryText

def fix_subject(result):
    if(result['Subject'].startswith('=?utf-8?B?')):
        try:
            result['Subject'] = base64.b64decode(result['Subject'][10:])
            result['Subject'] = result['Subject'].decode()
            result['SubjectType'] = 'utf-8/base64'
        except:
            print("er")

    if(result['Subject'].startswith('=?utf-8?Q?')):
        try:
            result['SubjectType'] = 'utf-8/quoted'
            result['Subject'] =decode_header(result['Subject'])[0][0].decode('utf-8')
        except:
            print("er2")

def getBetweenAngles(txt):
    start_ = txt.find('<')
    end_ = txt.find('>')
    if start_ != -1 and end_ != -1:
        return txt[start_+1:end_]
    else:
        return txt

def fix_from(result):
    result['FromEmail'] = getBetweenAngles(result['From'])
    if(result['From'].startswith('=?utf-8?B?')):
        try:
            result['From'] = base64.b64decode(result['Subject'][10:])
            result['From'] = result['From'].decode()
            result['FromType'] = 'utf-8/base64'
        except:
            print("er")

    if(result['From'].startswith('=?utf-8?Q?')):
        try:
            result['FromType'] = 'utf-8/quoted'
            result['From'] =decode_header(result['From'])[0][0].decode('utf-8')
        except:
            print("er2")

def timestamp_dict():
    date_ = datetime.datetime.now()
    day_of_year = date_.timetuple().tm_yday

    dateStruct = {'hour': date_.hour,
                  'day': date_.day,
                  'year': date_.year,
                  'month': date_.month,
                  'weekday': date_.weekday(),
                  'hour': date_.hour,
                  'minute': date_.minute,
                  'day_of_year': day_of_year,


                  'short_date': date_.ctime()}

    return dateStruct

if __name__ == "__main__":

    read_data = None
    path = 'mail.samp'
    with open(path) as f:
        read_data = f.read()

    parse_result = mail_parse(read_data)
    pprint.pprint( parse_result )
    print (parse_result['Body'])


