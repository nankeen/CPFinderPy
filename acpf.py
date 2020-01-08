#!/usr/bin/env python3
from os import system
from sys import argv
import re
import urllib.request
import json


def leave(msg):
    '''
    To quit the script gracefully
    '''
    print("\n [!] {}".format(msg))
    if found:
        print(" [?] Found following panel: {}".format('|'.join(found)))
    print(" [*] Exiting")
    exit()


def check(req):
    '''
    Checks for certain keywords in `req`
    True if found
    False if not
    '''
    if re.search(r'Password', req, re.IGNORECASE) or \
            re.search(r'Username', req, re.IGNORECASE) or \
            re.search(r'Wachtwoord', req) or \
            re.search(r'Senha', req) or \
            re.search(r'Personal', req) or \
            re.search(r'Usuario', req) or \
            re.search(r'Clave', req) or \
            re.search(r'Usager', req, re.IGNORECASE) or \
            re.search(r'Sing', req) or \
            re.search(r'passe', req) or \
            re.search(r'P\/W', req) or \
            re.search(r'Admin Password', req):
        return True
    else:
        return False


def main():
    '''
    This script tries to find admin panels by trial and error
    '''

    # The splash
    print("\n\t>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("\t> [!] Control Panel Finder                           >")
    print("\t> [!] ACPF Python port by Sygnogen                   >")
    print("\t>       ======================================       >")
    print("\t>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(" Supported site source: php | asp | aspx | cfm | js | cgi | brf")

    # Unpacks the arguments respectively
    try:
        site, code = argv[1:]
    except:
        leave("Usage: ./acpf.py host[:port] source")

    # Appends `http://` and `/` if none present
    if not re.search(r'^http://', site):
        site = 'http://' + site
    if not re.search(r'\/$', site):
        site = site + '/'
    print('\n')

    # Just to make sure lol
    print("-> Target: {}\n".format(site))
    print("-> Site source code: {}\n".format(code))
    print("-> Searching admin cp...\n\n")

    # Loads the JSON and refers by the site's source code
    paths = json.load(open('path.json'))
    path = paths[code]

    # Iterate through all the paths checking for keywords
    for ways in path:
        final = site + ways
        req = ''

        # Makes a HTTP GET request to the url, the response is read into `req`
        try:
            req = str(urllib.request.urlopen(final).read())
        # In the case of 404, 403 and etc we don't wan't it to crash
        except urllib.error.HTTPError:
            pass
        # This handles the mountain of connection error
        except urllib.error.URLError:
            # EZPZ handling
            leave("Connection error")

        # Checks it with a bunch of patterns and adds it to the `found` list if it exists
        if check(req) is True:
            print('\033[32m [+] Found -> {}\033[39m'.format(final))
            found.append('/' + ways)
        else:
            print('\033[33m [-] Not Found <- {}\033[39m'.format(final))

# The script won't run when imported as a module
if __name__ == '__main__':
    # A list of potential admin panels
    found = []
    try:
        main()

    # This ensures that when the interrupt key is pressed, Python won't spew it's guts out
    # Seriously I hate it when interrupts just floods the screen
    # A LOT
    except KeyboardInterrupt:
        leave("Interrupt received")
    # Yeah no problem
    leave("Search complete")

