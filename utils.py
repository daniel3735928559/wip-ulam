import math,sys,random,bisect,copy

## Utility functions: 

def read_seq(fn):
    l = []
    with open(fn) as f:
        for x in f:
            l.append(int(x))
    return l

def real_mod(x,m):
    return x - int(x/m)*m

def red(x,a=2*math.pi):
    return abs(x - a*math.floor(x/a)-(a/2))

def extend_lambda(l,m,k,N):
    am = {i:set([]) for i in range(m)}
    A = l
    for x in l:
        am[(k*x)%m].add(x)
    x = l[-1]+1
    while(len(A)) < N:
        reps = 0
        for i in range(m//2):
            breaking1 = False
            for a in am[(k*(x-i))%m]:
                if a >= x/2:
                    continue
                if x-a in am[(k*i)%m]:
                    reps += 1
                    if(reps > 1):
                        breaking1 = True
                        break
            if breaking1:
                break
        if reps == 1:
            am[(k*x)%m].add(x)
            A.append(x)
        x += 1
    return A

def extend_few_reps(l,N,p=1):
    ans = l
    reps = {i:0 for i in range(1,2*N+1)}
    for x in l:
        for y in l:
            reps[x+y] += 1
    for n in range(max(l)+1,N):
        r = random.random()
        if reps[n] == 0 or r < p/reps[n]:
            for x in ans:
                reps[x+n] += 1
            ans += [n]
    return ans

def extend_with_storage(l,N,debug=True):
    ans = l
    top = l[-1]
    sums = {}
    for i in range(len(l)):
        for j in range(i):
            if(ans[i]+ans[j] > top):
                sums[ans[i]+ans[j]] = 1 if (not ans[i]+ans[j] in sums) else sums[ans[i]+ans[j]]+1
        if(i % 500 == 0):
            print("{} / {}".format(i,len(l)))
            sys.stdout.flush()
    print(sums)
    prev_an = 0
    for c in range(N):
        an = ans[-1]+1
        while((not an in sums) or sums[an] != 1):
            an += 1
        for i in ans:
            sums[an+i] = 1 if (not an+i in sums) else sums[an+i]+1
        ans.append(an)
        if(c % 500 == 0):
            for i in range(prev_an,an):
                sums.pop(i,None)
            prev_an = an
            sys.stderr.write("{} {}\n".format(c,len(sums)))
            sys.stderr.flush()
            sys.stdout.flush()
    return ans

def sigma(l):
    return len({i+j for i in l for j in l})/len(l)

def extend_with_storage_careful(l,c,dq,N,debug=True):
    ans = l
    top = l[-1]
    candidates = c
    candidates_list = sorted([-x for x in c])
    disqualified = dq
    prev_an = 0
    num_hidden = 0
    for c in range(N):
        an = 0
        while(an <= ans[-1]):
            an = -candidates_list.pop(-1)
            candidates.remove(an)
        for i in ans:
            v = an+i
            if(v in disqualified):
                pass
            elif(v in candidates):
                candidates.remove(an+i)
                candidates_list.pop(bisect.bisect_left(candidates_list,-v))
                disqualified[v] = 2
            else:
                candidates.add(v)
                candidates_list.insert(bisect.bisect_left(candidates_list,-v),-v)
        ans.append(an)
        if(c % 500 == 0):
            for i in range(prev_an,an):
                num_hidden += 1 if disqualified.pop(i,None) != None else 0
        #     prev_an = an
        #     if(debug):
        #         print(c,len(disqualified))
        #     sys.stdout.flush()
        if(debug and c % 100 == 0):
            #print(len(ans),len(candidates),len(disqualified))
            print(c,'e',(num_hidden+len(disqualified)),len(ans))
            print(c,'sigma',(num_hidden+len(ans)+len(candidates)+len(disqualified))/len(ans))
    return candidates,disqualified,ans

def extend_seq(l,a,N):
    d = {x for x in l}
    al = [(x,red(a*x)) for x in l]
    al.sort(key=lambda x:-x[1])
    dists = [x[1] for x in al]
    xs = [x[0] for x in al]
    sums = {}
    for rep in range(N):
        min_sum = 2*l[-1]
        best_small = 1
        for i in range(len(xs)):
            small = xs[i]
            large_idx = -1
            top = l[-1]
            while(small+large > top and small+large < min_sum):
                large = l[large_idx]
                if(not small+large in candidates):
                    sums[small+large] = 0
                sums[small+large] += 1
                large_idx -= 1
            candidates = [x for x in sums if sums[x] == 1 and x < min_sum]
            for s in candidates:
                j = i+1
                ok = True
                while(j < len(s)-1 and l[j]+l[j+1] <= s):
                    if(s-l[j] in d):
                        sums[s] += 1
                        ok = False
                        break
                if(ok):
                    min_sum = s
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

def ulam_old(a,b,n):
    seq = [a,b]
    m = 2
    for i in range(n):
        m = next_seq(seq)
        seq.append(m)
    return seq

def ulam(a,b,n,debug=False):
    c,dq,ans = extend_with_storage_careful([a,b],{a+b},{},n,debug)
    return ans

def ulam_rep_dumb(l,n):
    seq = l
    d = {}
    for x in l:
        for y in l:
            if(x+y in d):
                d[x+y]+=1
            else:
                d[x+y]=1
    for x in l:
        d[x] = 0
    
    for i in range(n):
        m = min(x for x in d if d[x] == 1 and x > seq[-1])
        seq.append(m)
        d[m] = 0
        for x in seq:
            if(x+m in d):
                d[x+m] += 1
            else:
                d[x+m] = 1
    return seq


def ulam_rep_dumb_k(l,n):
    seq = l
    d = {}
    for x in l:
        for y in l:
            for z in l:
                if(x < y and y < z):
                    d[x+y+z]=d.get(x+y+z,0)+1
    for x in l:
        d[x] = 0
    
    for i in range(n):
        m = min(x for x in d if d[x] == 1 and x > seq[-1])
        seq.append(m)
        d[m] = 0
        for x in seq:
            for y in seq:
                if(y < x):
                    d[x+y+m] = d.get(x+y+m,0)+1
                else:
                    break

        print(i,seq[-1])
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

def ft_complex_2pi(t,l,N):
    d=len(l)/N
    cs = sum([math.cos(2*math.pi*t*x/N) for x in l])
    ss = sum([math.sin(2*math.pi*t*x/N) for x in l])
    return cs,ss

def ft_complex(t,l):
    cs = sum([math.cos(t*x) for x in l])
    ss = sum([math.sin(t*x) for x in l])
    return cs,ss
    
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

def find_alpha_search(l,t,s,N,debug=False):
    if debug: print('search',t,s,N)
    L = abs(ft(t,l))
    for i in range(1,N):
        M = 4
        Fs = [(abs(ft(t-s+(i/M)*2*s,l)),t-s+(i/M)*2*s) for i in range(M)]
        L,t = max(Fs,key=lambda x:x[0])
        s /= 2
    return t,L

def find_alpha_fast(l,prec=10,debug=False):
    a = 0.2
    s = 0.005
    prec = 4
    winner = a
    curmax = 0
    for i in range(int(math.pi/s+1)):
        a = 0.2+i*s
        if debug: print('around',a)
        rwinner,rmax = find_alpha_search(l,a,s/2,3*prec,debug)
        if debug: print('found',rwinner,rmax,curmax)
        if(rmax > curmax):
            winner = rwinner
            curmax = rmax
    return winner,curmax

def find_alpha(l,s=.02,prec=2,ft=ft,candidates=None,debug=True):
    a = 0.2
    winner = a
    curmax = 0
    if candidates is None:
        candidates = [0.2+i*2*s for i in range(int(math.pi/(2*s)+1))]
    while(prec >= 0):
        contenders = []
        for a in candidates:
            if debug: print(a)
            rwinner = a-s
            rmax = 0
            for i in range(-50,50):
                t = a+(i/50)*s
                c = abs(ft(t,l))
                if(c > rmax):
                    rwinner = t
                    rmax = c
            if debug: print(rwinner,rmax,curmax)
            if(rmax*10 > curmax):
                contenders.append((rwinner,rmax))
            if(rmax > curmax):
                winner = rwinner
                curmax = rmax
        prec -= 1
        candidates = []
        contenders.sort(key=lambda x:x[1])
        candidates = [x[0] for x in contenders[-100:] if 10*x[1] > curmax]
        if debug: print("contenders: {} {}".format(curmax,candidates))
        s /= 10
        if debug: print(winner,curmax)
    return winner,curmax

def breakdown(s,u,k,m):
    if((k*u)%m < m/3):
        return [(u,"lo")]
    if((k*u)%m > 2*m/3):
        return [(u,"hi")]
    if(s[u][0] == 0):
        return [(s[u][1],"init")]
    if(s[u][1] == 0):
        return [(s[u][0],"init")]
    
    return {s[u][0]:breakdown(s,s[u][0],k,m), s[u][1]:breakdown(s,s[u][1],k,m)}

def pprint(d, i=0):
    idt = " "
    if(isinstance(d, list)):
        print(idt*(i-1)+str(d))
    else:
        for x in d:
            #print(idt*i+str(x))
            pprint(d[x],i+1)

def squash_breakdown(b):
    if type(b) == dict:
        bs = [squash_breakdown(b[x]) for x in b]
        ans = {}
        for bl in bs:
            for x in bl:
                ans[x] = ans.get(x,0)+bl[x]
        return ans
    if type(b) == list:
        return {b[0]:1}

def reps_conv(x,l,k,m):
    fts = [ft_complex_2pi(t,l,m) for t in range(m)]
    #print(sorted([(t,(fts[t][0]*fts[t][0]+fts[t][1]*fts[t][1])/m,fts[t]) for t in range(m)],key=lambda x:x[1]))
    ccs = [(fts[t][0]**2 - fts[t][1]**2)*math.cos(2*math.pi*t*x/m)+2*fts[t][0]*fts[t][1]*math.sin(2*math.pi*t*x/m) for t in range(m)]
    ccsm = [(1/m)*x for x in ccs]
    bigs = [ccsm[0],ccsm[k],ccsm[m-k]]
    mediums = [ccsm[(i*k)%m] for i in range(2,7)]
    mediums += [ccsm[(m*m-i*k)%m] for i in range(2,7)]
    mediums += [ccsm[1],ccsm[m-1]]
    #if(sum(mediums) > 0):
    #    bigs += mediums
    bigs += mediums
    b = sum(bigs)
    c = sum(ccsm)
    return b>abs(c-b)+3,c,b,c-b,[round(t,2) for t in bigs]

# def reps_conv2(x,l,N):
#     al = [ft_complex_2pi(t,l,N) for t in range(N)]
#     return (1/N)*sum([(al[t][0]**2 - al[t][1]**2)*math.cos(2*math.pi*t*x/N)-2*al[t][0]*al[t][1]*math.sin(2*math.pi*t*x/N) for t in range(N)])

def reps_real(x,l):
    """
    Return a count for how many representations of x there are as a+b
    for a and b in l, where a and b are neither necessarily distinct nor 
    in order
    """
    ans = 0
    s = {t for t in l}
    for t in l:
        if x-t in s:
            ans += 1
    return ans

def cplx_prod(x,y):
    return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
            
def dthpower(z,d):
    m = z
    ans = (1,0)
    while d > 0:
        if(d % 2 == 1):
            ans = cplx_prod(m,ans)
        m = cplx_prod(m,m)
        d //= 2
    return ans

def cmplx_exp(theta):
    return (math.cos(theta),math.sin(theta))

def theta(seq,N):
    p = len(seq)
    S = set()
    T = set()
    U = set()
    n = 1
    for i in range(N):
        while n in S or n in T or n in U:
            n += 1
        if(seq[i%p] == "1" or seq[i%p] == 1):
            S.add(n)
            for a in S:
                T.add(a+n)
        else:
            U.add(n)
    return sorted(list(S)),T,U


def theta1(seq,N):
    p = len(seq)
    S = set()
    C = {1,2}
    T = set()
    U = set()
    n = 1
    for i in range(N):
        while n in S or n not in C or n in U:
            n += 1
        if(seq[i%p] == "1" or seq[i%p] == 1):
            for a in S:
                if a+n in C:
                    C.remove(a+n)
                    T.add(a+n)
                elif not a+n in T:
                    C.add(a+n)
            S.add(n)
        else:
            U.add(n)
    return sorted(list(S)),C,T,U

def thetainv(S,N):
    SS = {a+b for a in S if a <= N for b in S if b <= N}# and a < b}
    return [1 if n in S else 0 for n in range(1,N+1) if not n in SS]
