import threading

lck = threading.Lock()
def runFuncSynchronized(func, *args):
    global lck
    lck.acquire()
    func(*args)
    lck.release()

# def test(fname):
#     with open(fname, 'r') as f:
#         for ln in f:
#             n = int(ln)
#     n += 1
#     with open(fname, 'a') as f:
#         f.write(str(n) + '\n')

# if __name__=="__main__":
#     fname =  'counter.txt'

#     # re-initialize file
#     with open(fname, 'w') as f:
#         f.write('0\n')

#     threads = []
#     for i in range(50):
#         t = threading.Thread(target = runFuncSynchronized, args = (test, fname))
#         threads.append(t)
#         t.start()
    
#     for t in threads:
#         t.join()