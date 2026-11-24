from pyutil import *
import time
import gemini

s = readfile('ne2.csv')
lines = s.split('\n')
lines = [x.strip() for x in lines if x.strip() != '']
lines = [x for x in lines if x[0] != '#']

tlines = []
for x in lines:
    xs = x.split(',')
    xs = [x.strip() for x in xs]
    if len(xs) < 11:
        xs = xs + (11 - len(xs)) * ['']
    school = "%s, %s, %s %s %s" % tuple(xs[i] for i in [1,2,3,4,5])
    print(school, flush=True)
    
    s = gemini.gemini(r"""
Find the CS / Robotics / Engineering / MATH CTE teachers of this school.
All CS / Robotics / Engineering / MATH teachers must be included.
If there are no teachers of the above kind, add CTE teachers up to 2.
Give me the name (include Mr./Mrs./Ms./Dr.) and email address
(enclosed in "<...>") of the teachers in a semicolon separated values.
For instance: Mr. John Doe <jdoe@xyz.edu>; Mr. Tom Smith <tsmith@xyz.edu>.
%s
""" % school)    
    lines = s.split('\n')
    lines = [x for x in lines if '@' in x]
    s = '\n'.join(lines)

    new_ = s.split(';')
    new_ = [_.strip() for _ in new_]
    news_ = [x for x in new_ if x != '']
    
    old = xs[10]
    old = old.split(';')
    old = [_.strip() for _ in old]
    old = [x for x in old if x != '']

    print('new_:', len(new_), new_)
    print('old:', len(old), old)
    comb = set(new_ + old)
    print('comb:', len(comb), comb)
    print()
    
    #xs[10] = s
    #xs = ','.join(xs)
    #tlines.append(xs)
    #writefile('ne2.csv', '\n'.join(tlines))

