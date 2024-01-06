from base64 import b64encode
from re import sub
from os.path import dirname, realpath

def revshell(args):
    language = args.language
    encoding = args.encoding
    attackerIP = args.attacker_ip
    attackerPort = args.attacker_port
    with open(dirname(realpath(__file__)) + f"/../data/reverse shells/{language}","r") as code:
        shell = b""
        for line in code:
            line = sub("ATTACKER_IP",attackerIP,line)
            line = sub("ATTACKER_PORT",attackerPort,line)
            shell += line.encode()
    if encoding == "base64":
        output = b64encode(shell).decode()
    elif encoding == "none":
        output = shell.decode()
    print(output)
