from gevent import monkey; monkey.patch_socket()
import gevent
import urllib2
import time

def fetch(pid):
    response = urllib2.urlopen('http://www.baidu.com')
    print time.time()
    #result = response.read()
    #json_result = json.loads(result)
    #datetime = json_result['datetime']

    #print('Process %s: %s' % (pid, datetime))
    #return json_result['datetime']

def synchronous():
    for i in range(1,10):
        fetch(i)

def asynchronous():
    threads = []
    for i in range(1,10):
        threads.append(gevent.spawn(fetch, i))
    gevent.joinall(threads)

#synchronous()
#print 'end'
asynchronous()
