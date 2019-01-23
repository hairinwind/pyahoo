import threading

lck = threading.Lock()
def runner(fname):
    global lck
    lck.acquire()
    with open(fname, 'r') as f:
        for ln in f:
            n = int(ln)
    n += 1
    with open(fname, 'a') as f:
        f.write(str(n) + '\n')
    lck.release()

if __name__=="__main__":
    fname =  'counter.txt'

    # re-initialize file
    with open(fname, 'w') as f:
        f.write('0\n')

    threads = []
    for i in range(50):
        t = threading.Thread(target = runner, args = (fname, ))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()