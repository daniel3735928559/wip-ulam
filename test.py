import math,sys,random

## Utility functions: 

def read_seq(fn):
    l = []
    with open(fn) as f:
        for x in f:
            l.append(int(x))
    return l

def next_seq(l):
    i = 0
    j = len(l)-1
    M = l[-1]
    ans = {}
    while(i < j):
        k = j
        while(j < len(l)):
            ans[l[i] + l[j]] = not (l[i] + l[j] in ans)
            j += 1
        j = k
        i += 1
        #print("A",ans)
        while(l[i] + l[j-1] > M and i < j-1):
            j -= 1
        #print("IJ",i,j,l[i],l[j])
        m = min([x for x in ans if ans[x] == True])
        if(i+1 >= len(l) or l[i] + l[i+1] > m):
            #print("---------------",i,j,m)
            return m
        #print(i,j,l[i],ans)
    return m
            
def next_seq2(l,d):
    s = [x+y for x in l for y in l if x < y and x+y > l[-1]]
    s.sort()
    i = 0
    while(i+1 < len(s)):
        if(s[i] == s[i+1]):
            val = s[i]
            while(s[i] == val):
                s.pop(i)
        else:
            return s[i]
    return s[0]

def ulam(a,b,n):
    seq = [a,b]
    m = 2
    for i in range(n):
        m = next_seq(seq)
        seq.append(m)
    return seq

def gcd(a,b):
    return b if a == 0 else gcd(b,a%b if b != 0 else a)

def phi(d):
    m = 2
    f = {}
    while d > 1:
        if d % m == 0:
            f[m] = 1
            d //= m
            while(d % m == 0):
                f[m] += 1
                d //= m
        m += 1
    ans = 1
    for p in f:
        ans *= p**f[p] - p**(f[p]-1)
    return ans

def phid(a):
    return [(i,gcd(i,a)) for i in range(a)]

def ft(a,l):
    cs = sum([math.cos(a*x) for x in l])
    ss = sum([math.sin(a*x) for x in l])
    return math.sqrt(cs*cs+ss*ss)


def find_alpha(l,s=.02,prec=2):
    a = 0.2
    winner = a
    curmax = 0
    candidates = [0.2+i*2*s for i in range(int(math.pi/(2*s)+1))]
    while(prec >= 0):
        contenders = []
        for a in candidates:
            #print(a)
            rwinner = a-s
            rmax = 0
            for i in range(-50,50):
                t = a+(i/50)*s
                c = abs(ft(t,l))
                if(c > rmax):
                    rwinner = t
                    rmax = c
            #print(rwinner,rmax,curmax)
            if(rmax*10 > curmax):
                contenders.append((rwinner,rmax))
            if(rmax > curmax):
                winner = rwinner
                curmax = rmax
        prec -= 1
        candidates = []
        contenders.sort(key=lambda x:x[1])
        candidates = [x[0] for x in contenders[-100:] if 10*x[1] > curmax]
        #print("contenders: {} {}".format(curmax,candidates))
        s /= 10
        #print(winner,curmax)
    return winner,curmax

## Experiments: 

def experiment0():
    print("Attempt to confirm that alpha_{12,13} == pi")
    print(ft(math.pi,ulam(12,13,500)))

def experiment1():
    print("Compute alpha_{1,i+1} for i = 1..19")
    n = 200
    s = 0.0001
    for i in range(1,20):
        print(1,i+1,find_alpha(ulam(1,i+1,n),s))

def experiment2():
    print("Compute alpha_{i,i+1} for i = 1..19")
    n = 200
    s = 0.0001
    for i in range(1,20):
        print(i,i+1,find_alpha(ulam(i,i+1,n),s))

    
def experiment3(l):
    print("Check linearity of f_N(alpha) in N")
    a = alpha1_2
    for N in range(0,1000,100):
        print(ft(a,l[:N]))


def experiment4():
    a,f = find_alpha(ulam(3,4,200),0.0001)
    print((2*math.pi/a).as_integer_ratio())

def experiment5():
    l = u1_2
    a = 2.5714474995
    for k in range(100000):
        d = k*a-2*math.pi*math.floor(k*a/(2*math.pi))
        f = ft(k*a,l)
        if(abs(d) > 0.1 and abs(2*math.pi - d) > 0.1 and f > 1000):
            print(k,d,f)

def experiment6(us,ms):
    print("Try to measure the bias in the 'us' mod each m in ms by computing the std dev of the number of times each residue class mod m shows up")
    m = 1
    for x in ms:
        m = x
        l = [0 for i in range(m)]
        for a in us:
            l[a % m] += 1
        mu = len(us)/x
        sigma = math.sqrt(sum([(i - mu)*(i - mu) for i in l]))
        print(sigma/m, m,sigma)
    
def experiment7():
    print("Approximate alpha for a few precomputed sequences")
    print("1,2",find_alpha(u1_2[:2000]))
    print("1,3",find_alpha(u1_3[:2000]))
    print("2,3",find_alpha(u2_3[:2000]))
    print("12,13",find_alpha(u12_13[:2000]))
            
def experiment8(l):
    print("Compute the summands of each element of l")
    s = {x : (0, x) for x in l}
    for i in range(2,len(l)):
        for j in range(i):
            if(l[i] - l[j] in s):
                #s[l[j]] += 1
                #s[l[i] - l[j]] += 1
                s[l[i]] = (l[j], l[i] - l[j])
                break
    for x in s:
        print("{} = {} + {}".format(x,s[x][0],s[x][1]))

def experiment9(l,m):
    print("Compute how many times a_n lies in each additive subgroup mod m:")
    s = {x:0 for x in range(1,m+1) if m%x == 0}
    for i in l:
        s[gcd(i,m)] += 1
    gcds = phid(m)
    for x in s:
        print("{} : {} =? {}".format(x,s[x],int((l/m)*len([t for t in gcds if t[1] == x]))))

def evolve_random(d,m,total,N):
    end = total + N
    while total < end:
        r1 = random.uniform(0,total)
        r2 = random.uniform(0,total)
        c = 0
        a = -1
        b = -1
        for i in range(m):
            c += d[i]
            if r1 < c and a == -1:
                a = d[i]
            if r2 < c and b == -1:
                b = d[i]
            if a != -1 and b != -1:
                break
        d[(a+b)%540] += 1
        total += 1
    return d

def experiment10(l,k,m,N):
    print("Evolve the mod m distribution on the elements of l (multiplied by k) by selecting new summands randomly according to the existing distribution")
    s = {x:0 for x in range(m)}
    for i in l:
        s[(k*i)%m] += 1
    ev = evolve_random(s,m,len(l),N)
    for x in ev:
        print("{} {}".format(x%m,ev[x]))
    

def experiment11(l,a):
    print("Compute how often each element x of l occurs as the small summand and compare with cos(a*x)")
    s = {x : [] for x in l}
    for i in range(2,len(l)):
        for j in range(i):
            if(l[i] - l[j] in s):
                s[l[j]].append(i)
                break
    for x in s:
        print("{} {} {} {}".format(x,len(s[x]), math.cos(a * x), s[x]))
    return s

def experiment12(l,a):
    print("Compute how often each element x of l occurs as any summand and compare with cos(a*x)")
    s = {x : [] for x in l}
    for i in range(2,len(l)):
        for j in range(i):
            if(l[i] - l[j] in s):
                s[l[j]].append(l[i])
                s[l[i] - l[j]].append(l[i])
                break
    for x in s:
        print("{} {} {} {}".format(x,len(s[x]), math.cos(a * x), s[x]))
    return s

u1_2 = read_seq("seq1,2")
u1_3 = read_seq("seq1,3")
u2_3 = read_seq("seq2,3")
u12_13 = read_seq("seq12,13")
alpha1_2 = 2.5714474995
# experiment6(u1_2,[5,17,22,259,281,540,2441,2981,5422,2711,27*5,2*2*3*3*3*5*5,2*2*2,2**4,2*2*3*3*5,7*7*7*7*7*7])
# experiment6(u1_2,[540*i for i in range(1,20)])
# experiment6(u1_2,[3*5*2729,3*5*2730])
# experiment6(u1_2,range(1,3000))
# experiment7()
# experiment8(u1_2)
# experiment9(u1_2,87292)
# experiment10(u1_2,221,540,100000)
# experiment11(u1_2, alpha1_2)
# experiment12(u1_2, alpha1_2)
