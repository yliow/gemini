import time

def sleep(n, dt=1.0, places=None, template='[sleep %s]'):
    t = 0.0
    if places==None:
        if dt >= 1.0: places = 0
        elif dt >= 0.1: places = 1
        elif dt >= 0.01: places = 2
        else: places = 3
    while t <= n:
        str_t = str(round(t, places))
        if places == 0: str_t = str_t.replace(".0", '')
        s = "%s/%s" % (str_t, n)
        s = template % s
        print(s, flush=True, end='')
        time.sleep(dt)
        t += dt
        a = '\b' * (len(s))
        b = ' ' * (len(s))
        print('%s%s%s' % (a, b, a), flush=True, end='')
