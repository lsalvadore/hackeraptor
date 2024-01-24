from itertools import product
from re import sub
from requests import request
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def webfuzz(args):
    url = args.url
    wordlists = args.wordlists
    headers = args.headers
    method = args.method
    data = args.data

    no_verify = args.no_verify
    if no_verify:
        disable_warnings(InsecureRequestWarning)

    status_codes = args.status_codes
    sizes = args.sizes

    no_status_codes = args.no_status_codes
    no_sizes = args.no_sizes

    words = []
    variablesNumber = len(wordlists)
    wordsSpaceCardinality = 1
    for variableIndex in range(variablesNumber):
        with open(wordlists[variableIndex],"r") as wordlistFile:
            words += [wordlistFile.read().splitlines()]
            wordsSpaceCardinality *= len(words[-1])

    wordsSpace = product(*words)
    wordsIteration = 0
    for wordsTuple in product(*words):
        wordsIteration += 1
        print(f"{wordsIteration}/{wordsSpaceCardinality}", end="\t")
        parameters = [method,url]
        if not data:
            parameters += [""]
        if not headers:
            parameters += []
        for variableIndex in range(variablesNumber):
            for index in range(len(parameters)):
                try:
                    parameters[index] = sub(f"\${variableIndex+ 1}",wordsTuple[variableIndex],parameters[index])
                except:
                    pass
        response = request(method=parameters[0],url=parameters[1],data=parameters[2],headers=parameters[3:],verify=(not no_verify))
        size = len(response.content)
        if ( type(status_codes) == list and response.status_code not in status_codes ) or \
           ( type(no_status_codes) == list and response.status_code in no_status_codes) or \
           ( type(sizes) == list and response.size not in sizes ) or \
           ( type(no_sizes) == list and response.size in no_sizes ):
             pass
        print(f"{response.status_code}\t{size}\t{parameters}")
