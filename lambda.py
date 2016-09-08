from __future__ import print_function
from urllib2 import Request, urlopen, URLError
import xml.etree.ElementTree

import boto3
import json


def has_elements(iter):
    from itertools import tee
    iter, any_check = tee(iter)
    try:
        any_check.next()
        return True, iter
    except StopIteration:
        return False, iter


def handler(event, context):
    '''Handler which gets called by the Amazon Gateway API.
	   returns a JSON response.
    '''
    try:
        body = json.dumps(event, indent=2)
        #print("Received event: " + json.dumps(event, indent=2))
        textValue = "test"
        j = json.loads(body)
        value =  j['body']
        
        parameters = value.split("&")
        #tokenParam = parameters[0]
        #channelParam = parameters[3]
        textParam = parameters[8]
        textValue = textParam.split("=")[-1]
        if(textValue == None or len(textValue) < 1):
            return {
                'text': "no text supplied"
            }
        request = Request('http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'+textValue+'?key=7ca7d924-81c5-4a0f-9834-1f59f32f0610')
        response = urlopen(request)
        meaning = response.read()
        #return (meaning)
        result = ""
        root = xml.etree.ElementTree.fromstring(meaning)
        rootItr = root.iter()
        if (has_elements(rootItr)):
            childTag = rootItr.next().tag
            if (childTag == "entry"):
                meanings = root.iter('dt')
                for meaning in meanings:
                    if meaning is None or meaning.text is None:
                        result += ",\n"
                    else:
                        result += meaning.text[1:] + ",\n"
            elif (childTag == "suggestion"):
                suggestions = root.iter('suggestion')
                result += "Word not Found. Suggestions:\n"
                for suggestion in suggestions:
                    if suggestion is None or suggestion.text is None:
                        result += ",\n"
                    else:
                        result += suggestion.text + ",\n"
            else:
                result += "Error occured. Please check your spelling."
                    
                
        else:
            result += "Sorry, I don't understand. Please check your spelling."
        
        return {
            'text': result
        }
    except Exception as e:
        return ("error", e)
    
