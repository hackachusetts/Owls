#!/bin/python

# Written by Hackachusetts

import argparse
import re
import sys
import socket
import sys
import textwrap
import urllib.request

title_art = '''
  ___       __        __      _           ____      
 / _ \      \ \      / /     | |         / ___|     
| | | |      \ \ /\ / /      | |         \___ \     
| |_| |  _    \ V  V /    _  | |___   _   ___) |  _ 
 \___/  (_)    \_/\_/    (_) |_____| (_) |____/  (_)

'''

logo ='''
          _...._
        /       
       /  o _ o  
       (    \/  )
      )          (
    (    -  -  -  )
    (             )
     (            )
      [          ]
    ---/l\    /l\--------
      ----------------
         (  )
        ( __ _)
    ''' 

print(title_art)
print(logo)

email_dict = {}

class Owls:
    def __init__(self, args):
        self.args = args

    def get_ip(self):
        try:
            ip_addr = socket.gethostbyname(self.args.url)

            return ip_addr

        except socket.gaierror:
            return 'Unable to obtain IP address. Check the URL and try again.'

    def strip_html_tags(self, text):
        finished = 0

        while not finished:
            finshed = 1
            start = text.find('<')

            if start >= 0:
                stop = text[:start].find('>')
                if stop >= 0:
                    text = text[:start] + text[start + stop + 1:]
                    finished = 0

            return text

    def scrape(self):
        ip_addr = self.get_ip()
        domain_name = self.args.url
        page_counter = 0

        print(f'[+] Scanning {self.args.url} ({ip_addr}) for email addresses...\n')

        try:
            while page_counter < 50:
                results = f'http://groups.google.com/groups?q={self.args.url}&hl=en&lr=&ie=UTF-8&start{page_counter}&sa=N'
                request = urllib.request.Request(results)
                request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
                opener = urllib.request.build_opener()
                text = opener.open(request).read().decode('utf-8')
                emails = re.findall('([\w\.\-]+@' + domain_name + ')', self.strip_html_tags(text))
                
                for email in emails:
                    d[email] = 1
                page_counter += 10

        except IOError:
            print('Cannot connect to Google Groups.')
        
        page_counter_web = 0

        try:
            while page_counter_web < 50:
                results_web = f'http://www.google.com/search?q=%40{domain_name}&hl=en&lr=&ie=UTF-8&start={page_counter_web}&sa=N'
                request_web = urllib.request.Request(results_web)
                request_web.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')
                opener_web = urllib.request.build_opener()
                text = opener_web.open(request_web).read().decode('utf-8')
                emails_web = re.findall('([\w\.\-]+@' + domain_name + ')', self.strip_html_tags(text))

                for email_web in emails_web:
                    email_dict[email_web] = 1
                page_counter_web += 10

        except IOError:
            print("Cannot connect to Google Web.")
        
        if email_dict.keys:
            print(f'{len(email_dict)} email(s) found\n')

            for uniq_emails_web in email_dict.keys():
                print(uniq_emails_web)

        else:
            print('0 emails found.')

    def output(self):
        with open(self.args.output, 'w') as f:
            for email in email_dict.keys():
                f.write(email + '\n')

        print(f'\nSaved emails to {self.args.output}')

    def run(self):
        if self.args.url:
            self.scrape()

        if self.args.output:
            self.output()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'owls.py',
        description = 'Owls is a command line tool used for scraping emails from URLS.',
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog = textwrap.dedent('''Example:
            ./owls.py - u example.com # Scrape Url.
            ./owls.py - u example.com -o myfile.txt # Write to file
        '''))

    parser.add_argument('-u', '--url', help = 'specified URL')
    parser.add_argument('-o', '--output', help = 'write to file')

    args = parser.parse_args()

    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit()

    owls = Owls(args)
    owls.run()
