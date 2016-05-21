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

def find_alpha(l,s=.02,prec=2,ft=ft,candidates=None):
    a = 0.2
    winner = a
    curmax = 0
    if candidates is None:
        candidates = [0.2+i*2*s for i in range(int(math.pi/(2*s)+1))]
    while(prec >= 0):
        contenders = []
        for a in candidates:
            print(a)
            rwinner = a-s
            rmax = 0
            for i in range(-50,50):
                t = a+(i/50)*s
                c = abs(ft(t,l))
                if(c > rmax):
                    rwinner = t
                    rmax = c
            print(rwinner,rmax,curmax)
            if(rmax*10 > curmax):
                contenders.append((rwinner,rmax))
            if(rmax > curmax):
                winner = rwinner
                curmax = rmax
        prec -= 1
        candidates = []
        contenders.sort(key=lambda x:x[1])
        candidates = [x[0] for x in contenders[-100:] if 10*x[1] > curmax]
        print("contenders: {} {}".format(curmax,candidates))
        s /= 10
        print(winner,curmax)
    return winner,curmax

## Experiments: 

def experiment0(l,a,n):
    """Attempt to confirm that f_N(alpha) is linear in N"""
    cs = math.cos(a*l[0])
    ss = math.sin(a*l[0])
    prev = 0
    for N in range(1,min(n,len(l))):
        cs += math.cos(a*l[N])
        ss += math.sin(a*l[N])
        ans = math.sqrt(cs*cs+ss*ss)/N
        #print(ans)
        print(math.log(0.8-ans)/math.log(N) if N > 10 else 0)
        prev = ans
        
def experiment1():
    """Compute alpha_{1,i+1} for i = 1..19"""
    n = 200
    s = 0.0001
    for i in range(1,20):
        print(1,i+1,find_alpha(ulam(1,i+1,n),s))

def experiment2():
    """Compute alpha_{i,i+1} for i = 1..19"""
    n = 200
    s = 0.0001
    for i in range(1,20):
        print(i,i+1,find_alpha(ulam(i,i+1,n),s))

    
def experiment3(l):
    """Check linearity of f_N(alpha) in N"""
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
    """Try to measure the bias in the 'us' mod each m in ms by computing the std dev of the number of times each residue class mod m shows up"""
    m = 1
    for x in ms:
        m = x
        l = [0 for i in range(m)]
        for a in us:
            l[a % m] += 1
        mu = len(us)/x
        sigma = math.sqrt(sum([(i - mu)*(i - mu) for i in l]))
        print(m,sigma)

def experiment7():
    """Approximate alpha for a few precomputed sequences"""
    print("1,2",find_alpha(u1_2[:2000]))
    print("1,3",find_alpha(u1_3[:2000]))
    print("2,3",find_alpha(u2_3[:2000]))
    print("12,13",find_alpha(u12_13[:2000]))
            
def experiment8(l):
    """Compute the summands of each element of l"""
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
    """Compute how many times a_n lies in each additive subgroup mod m:"""
    s = {x:0 for x in range(1,m+1) if m%x == 0}
    for i in l:
        s[gcd(i,m)] += 1
    gcds = phid(m)
    for x in s:
        print("{} : {} =? {}".format(x,s[x],int((len(l)/m)*len([t for t in gcds if t[1] == x]))))

def experiment10(l,k,m,N):
    """Evolve the mod m distribution on the elements of l (multiplied by k) by selecting new summands randomly according to the existing distribution"""
    s = {x:0 for x in range(m)}
    for i in l:
        s[(k*i)%m] += 1
    ev = evolve_random(s,m,len(l),N)
    for x in ev:
        print("{} {}".format(x%m,ev[x]))
    

def experiment11(l,a):
    """Compute how often each element x of l occurs as the small summand and compare with cos(a*x)"""
    s = {x : [] for x in l}
    for i in range(2,len(l)):
        for j in range(i):
            if(l[i] - l[j] in s):
                s[l[j]].append(i)
                break
    for x in s:
        print("{} {} {} {} {}".format(x,len(s[x]), abs(a*x-2*math.pi*math.floor(a*x/(2*math.pi))-math.pi), math.cos(a * x), s[x]))
    return 

def experiment12(l,a):
    """Compute how often each element x of l occurs as any summand and compare with cos(a*x)"""
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

def experiment13(l):
    """For each x in l, compute how far from x the large summand of x is"""
    s = {l[i] : i for i in range(len(l))}
    ans = []
    for i in range(2,len(l)):
        for j in range(i):
            if(l[i] - l[j] in s):
                ans.append((l[j],l[i] - l[j],j,i-(s[l[i] - l[j]]),l[i]-l[i-1]))
                break
    for i in range(len(ans)):
        print("{} \t{} \t{} \t{} \t{} \t{}".format(i+2,l[i],ans[i][0],ans[i][2],ans[i][3],ans[i][4]))
    return s

def experiment14(l,a,k,m):
    """
    For each x in l, create a histogram of all values mod alpha for
    which x shows up as a summand (only for xs that show up as a
    summand at least 10 times)
    """
    s = {x : [] for x in l}
    for i in range(2,len(l)):
        for j in range(i):
            if(l[i] - l[j] in s):
                s[l[j]].append(i)
                break
    for x in s:
        if(len(s[x]) < 10):
            continue
        lm = [0 for i in range(m)]
        for i in s[x]:
            lm[(k*l[i])%m]+=1
        print("{} \t{} \t{} \t{} \t{} \t{}".format(x,len(s[x]), a*x-2*math.pi*math.floor(a*x/(2*math.pi)), math.cos(a * x), (k*x)%m, lm))
    return 


def experiment15(l,k,m):
    """Compute a histogram of values of a_i mod lambda"""
    cs = [0 for i in range(m)]
    for x in l:
        cs[(k*x) % m] += 1
    print(cs)
    return cs


def experiment16(l):
    """
    Factor each element of l into l[0] and l[1] and compute how many of
    each shows up.
    """
    s = {x:() for x in l}
    s[l[0]] = (0,l[0])
    s[l[1]] = (0,l[1])
    for a in l:
        for x in s:
            if(a-x in s and a-x != x):
                s[a] = (x,a-x) if x < a-x else (a-x,x)
                break

    #print(s)
    ans = {l[0]:(1,0),l[1]:(0,1)}
    for a in l[2:]:
        first = ans[s[a][0]]
        second = ans[s[a][1]]
        ans[a] = (first[0]+second[0],first[1]+second[1])
    for a in l:
        print(a,ans[a],ans[a][0]+ans[a][1],(ans[a][0]/(ans[a][0]+ans[a][1]),ans[a][1]/(ans[a][0]+ans[a][1])) if ans[a][0]+ans[a][1] > 0 else 0)

def experiment17(l,k,m):
    """
    Compute all complements of each Ulam number.  Denote any a_i with
    complements both in the low half and the high half mod k/m as being
    weird, and print those.
    """
    s = {x:() for x in l}
    s[l[0]] = (0,l[0])
    s[l[1]] = (0,l[1])
    for a in l:
        for x in s:
            if(a-x in s and a-x != x):
                s[a] = (x,a-x) if x < a-x else (a-x,x)
                break

    #print(s)
    coms = {x:[] for x in [0]+l}
    weird = [];
    weird2 = [];
    for a in l:
        coms[s[a][0]] += [s[a][1]]
        coms[s[a][1]] += [s[a][0]]
    for a in l:
        lo = 0
        hi = 0
        for c in coms[a]:
            if (k*c)%m < m/2:
                lo += 1
            else:
                hi += 1
        low = (k*a)%m < m/2
        if(lo != 0 and hi != 0):
            weird += [(a,lo,hi)]
        if ((low and hi > 0) or (not low and lo > 0)) and hi*lo == 0:
            weird2 += [(a,lo,hi)]
        #print(a,lo,hi,coms[a])
    print("WEIRD")
    for w in weird:
        print(w)
    print("WEIRDER")
    for w in weird2:
        print(w)
    

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
        
def experiment18(l,us,k,m,complete=False):
    """Print the complete factorisation tree of any Ulam number, along with outlier information"""
    # s is a dictionary of summands given as x:(a,b) where a+b = x, are all in l, and a < b
    s = {x:() for x in l}
    s[l[0]] = (0,l[0])
    s[l[1]] = (0,l[1])
    for a in l:
        for x in s:
            if(a-x in s and a-x != x):
                s[a] = (x,a-x) if x < a-x else (a-x,x)
                break
    for u in us:
        b = breakdown(s,u,k,m)
        sq = squash_breakdown(b)
        lsq = sorted([(x[0],sq[x]) for x in sq],key=lambda x: (k*x[0])%m)
        print(u,lsq)
        if(complete):
            pprint(b)

def experiment19(l):
    """Get an idea of the density of l"""
    n = 10
    while(n <= len(l)):
#       print(n,sigma(l[:n]))
        print(n,l[n]/n)
        n *= 10

def experiment20(l):
    """Compute 2A - 2A for the set A given by l"""
    ta = {i+j for i in l for j in l}
    tamta = {i-j for i in ta for j in ta}
    a = sorted([i for i in tamta if i > 0])
    print([i for i in range(a[-1]) if not i in a])
    print(l)

def experiment21(a,l):
    """Compute the complex Fourier transform of a sequence"""
    n = 10
    while(n <= len(l)):
        print(ft_complex(a,l[:n]))
        n *= 10
    print(ft_complex(a,l))

        
u1_2 = read_seq("seqs/seq1,2")
u1_3 = read_seq("seqs/seq1,3")
u1_4 = read_seq("seqs/seq1,4")
u2_3 = read_seq("seqs/seq2,3")
u2_5 = read_seq("seqs/seq2,5")
u12_13 = read_seq("seqs/seq12,13")
u1_2_3 = read_seq("seqs/seq1,2,3")
sf01001 = read_seq("seqs/01001sf")
sf10010 = read_seq("seqs/sf10010")
alpha1_2 = 2.5714474995
alpha1_4 = 0.506013502
alpha1_2_3 = 0.23036348 # 0.23034156 #0.23034016

# m=540
# k=221
# l = {x:0 for x in range(m)}
# for x in u1_2:
#     l[(k*x)%m]+=1
# for x in range(m):
#     print("{} {}".format(x,l[x])) 
# experiment0(u1_2, alpha1_2, 100000)
# experiment6(u1_2,[5,17,22,259,281,540,2441,2981,5422,40935,87292,215519,1380406])
# experiment6(u1_2,list(range(530,550))+list(range(2430,2450)))
# experiment6(u1_2,[540*i for i in range(1,20)])
# experiment6(u1_2,[3*5*2729,3*5*2730])
# experiment6(u1_2,range(1,3000))
# experiment7()
# experiment8(u1_2)
# experiment9(u1_2,2*3*47*69)
# experiment10(u1_2,221,540,100000)
# experiment11(u1_2, alpha1_2)
# experiment12(u1_2, alpha1_2)
# experiment13(u1_2)
# print(extend_with_storage(u1_2,10000))
# ans,c,dq = extend_with_storage_careful([1,2],{3},{},100000)
# print(c)
# print(dq)
# print(ans)
# experiment11(u1_4, alpha1_4)
# experiment14(u1_2, alpha1_2, 2219, 5422)
# experiment15(u1_2, 2219,5422)
#find_alpha(u2_5,prec=1)
#experiment6(u2_5,[x for x in range(1,5001,2) if x < 10 or (x%7 != 0 and x%3!=0)])
#experiment15(u2_5,1,3)
#experiment13(u12_13)
#experiment16(u1_2[:10000])
#experiment17(u1_2,2219,5422)
#experiment18(u1_2[:10000],u1_2[:10000],2219,5422)
#experiment17(u2_3,857,4622)
#experiment19(u1_2)
# c,d,l=extend_with_storage_careful([1,2],{3},{},100000,True)
# for i in range(len(l)):
#     if l[i] != u1_2[i]:
#         print("AAAAA",i,l[i],u1_2[i])
#         break
# print(sigma(u1_2[:1000]))
#experiment20(u1_2[:1000])

#experiment21(alpha1_2,u1_2)
    
# def reps_conv2(x,l,N):
#     al = [ft_complex_2pi(t,l,N) for t in range(N)]
#     #print(sorted([(t,(al[t][0]*al[t][0]+al[t][1]*al[t][1])/N,al[t]) for t in range(N)],key=lambda x:x[1]))
#     ccs = [(al[t][0]**2 - al[t][1]**2)*math.cos(2*math.pi*t*x/N)+2*al[t][0]*al[t][1]*math.sin(2*math.pi*t*x/N) for t in range(N)]
#     ccss = sorted([(t,ccs[t]/N) for t in range(N)],key=lambda x:abs(x[1]))
#     ccsst = [ccss[t][1] for t in range(N)]
#     print(sum(ccsst[:-5]))
#     print(ccss[-5:])
#     print(2219,ccs[2219]/N)
#     return (1/N)*sum(ccs)


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

def experiment22(l,kinv,k,m):
    for x in range(1,int(m/6)):
        t = (kinv*x)%m
        if(t > m/2):
            print(t,"too big")
            continue
        if(t < m/4):
            print(t,"too small")
            continue
        r = reps_conv(t,l,k,m)
        print(x,t,reps_real(t,l),r)

def experiment23(l,a):
    l=[0]+l
    s = {x+y for x in l for y in l if x <= y}
    m = max(s)
    lambda_a=2*math.pi/a
    mods = []
    for i in range(l[-1]):
        if not i in s:
            mods.append((i,real_mod(i,lambda_a)))

            bins = {}
    for x in mods:
        d = round(x[1],2)
        bins[d] = bins.get(d,0)+1
    mods += [("---",x) for x in [lambda_a/6,lambda_a/3,lambda_a/2,2*lambda_a/3,5*lambda_a/6,lambda_a]]
    print("\n".join([str(x[0])+" \t"+str(x[1]) for x in sorted(mods,key=lambda x:x[1])]))
    hist = []
    for i in range(0,int(lambda_a*100)):
        hist.append((i/100,bins.get(i/100,0)))
    print("HISTOGRAM")
    for x in hist:
        print(x[0],x[1])
    #print(lambda_a/6,lambda_a/3,lambda_a/2,2*lambda_a/3,5*lambda_a/6,lambda_a)
        
def experiment24():
    l = ulam_rep_dumb([1,3],5000)
    for n in [10,100,1000,5000]:
        print(n/l[n])
    print(find_alpha(l))
    
#experiment24()
#experiment23(u1_2[:5000],alpha1_2)
# experiment22(u1_2[:253],2441,2219,5422)
# experiment22(u1_2[:8000],87292,88203,215519)
# print(reps_conv(69,u1_2[:500],2*5422))

# print(reps_real(1901,u1_2[:500]))
# print(reps_conv2(1901,u1_2[:500],5422))
# print(reps_real(69,u1_2[:500]))

#
#print(ulam_rep_dumb([2,3],400))

# l=[0]+u1_2[:10000]
# s = {x+y for x in l for y in l if x <= y}
# m = max(s)
# lambda1_2=2*math.pi/alpha1_2
# mods = []
# for i in range(u1_2[10000]):
#     if not i in s:
#         print(i,)
#         mods.append((i,real_mod(i,lambda1_2)))
# print("\n".join([str(x) for x in sorted(mods,key=lambda x:x[1])]))
# print(lambda1_2/3,lambda1_2/2,2*lambda1_2/3,lambda1_2)
        
# d = {}
# idx = {}
# l=u1_2
# for i in range(1,len(l)):
#     diff = l[i]-l[i-1]
#     d[diff] = d.get(diff,0)+1
#     idx[diff] = i
# print(sorted([(x,d[x]) for x in d],key=lambda x:x[0]))
# print(sorted([(x,idx[x]) for x in idx],key=lambda x:x[0]))


    
def experiment25():
    #print(ulam_rep_dumb_k([1,2,3],5000))
    #print(find_alpha(u1_2_3,prec=4))
    print("asd",alpha1_2_3/(2*math.pi))
    print(2*math.pi/alpha1_2_3)
    a=alpha1_2_3/(2*math.pi)
    la = 2*math.pi/alpha1_2_3
    lambda1_2_3 = la-2*math.pi*int(la/(2*math.pi))
    print(lambda1_2_3)
    
# a=alpha1_2_3/(2*math.pi)
# print(ft(alpha1_2_3,u1_2_3))
# print(ft_complex_2pi(a,u1_2_3,1))
# print(ft_complex_2pi(alpha1_2/(2*math.pi),u1_2,1))
# experiment15(u1_2_3,18,491)
# print(find_alpha(u1_2_3,prec=4,ft=lambda t,l: ft_complex(t,l)[0]))

def experiment26(l,lam):
    """
    Compute for all integers up to N within 1/6 of n*lam the number of
    representations as sums of pairs of elements of l
    """
    s = {0:0}
    for x in l:
        print(x,l[-1])
        for y in l:
            if y > x: break
            s[x+y] = s.get(x+y,0)+1
    for i in range(l[-1]):
        r = real_mod(i,lam)
        lo = lam/6
        hi=5*lam/6
        reps = s.get(i,0)
        if(r < lo):
            print(i,reps,lo-r)
        if(r > hi):
            print(i,reps,r-hi)

#experiment26(u1_2[:10000],2*math.pi/alpha1_2)
#find_alpha(u1_2[:10000],prec=2)

def experiment27():
    bigcoeffs = [1.9897120000000001, 1.722024, 1.431156, 1.140288, 2.8623160000000003, 0.290868, 2.28058, 2.5714479999999997]
    for x in bigcoeffs:
        f = ft_complex(x,u1_2[:10000])
        print(f[0],f[1],math.sqrt(f[0]**2+f[1]**2))

    for k in range(540):
        ak = real_mod(k*alpha1_2,2*math.pi)
        f = ft_complex(ak,u1_2[:10000])
        print(k,ak,f,math.sqrt(f[0]**2+f[1]**2))
    print(bigcoeffs)

def experiment28(m,l,N,threshold,d):
    cs = {i:0 for i in range(m)}
    ss = {i:0 for i in range(m)}
    ans = {i:[] for i in range(m)}
    fts = {i:0 for i in range(m)}
    terms = {i:0 for i in range(m)}
    
    for k in range(1,m):
        #print(k)
        for n in range(N):
            cs[k] += math.cos(2*math.pi*k/m*l[n])
            ss[k] += math.sin(2*math.pi*k/m*l[n])
            if n % 999 == 0 and n > 0:
                f = math.sqrt(cs[k]**2+ss[k]**2)
                ans[k] += [math.log(f)/math.log(n)]
                fts[k] = (cs[k],ss[k])
                #terms[k] = cplx_prod(cmplx_exp(-2*math.pi*k/m),dthpower(fts[k],d))

    summary = [(k,ans[k][-1],fts[k]) for k in range(1,m) if len(ans[k]) > 0 and ans[k][-1] > threshold]
    for x in sorted(summary,key=lambda x:x[1]):
        print(*x)

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

def experiment29(l,d,N):
    s = {i:([[i]] if i in l else []) for i in range(N)}
    for i in range(1,d):
        print(i)
        ss = {}
        for x in range(N):
            ss[x] = []
            for a in [k for k in l if k <= x]:
                #print(x-a,s[x-a])
                ss[x] += [b+[a] for b in s[x-a]]
        s = ss
    for x in range(N):
        print(x,x in l,s[x])


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

#experiment22(u1_2[:253],2441,2219,5422)



# m = 5422
# for a in range(m//2):
#     c = sum([math.cos(2*math.pi*2*k*a/m) for k in range(m//2)])
#     s = sum([math.sin(2*math.pi*2*k*a/m) for k in range(m//2)])
#     print(a,c,s)
         

#m=87292
#print([sum([math.cos(2*math.pi*i*k*18/491) for i in u1_2_3 if i < 491]) for k in range(10)])
#print([sum([math.sin(2*math.pi*i*k*18/491) for i in u1_2_3 if i < 491]) for k in range(10)])
#find_alpha(u1_2_3,prec=3)

# experiment28(540,u1_2,10000,0.5,2)
# print("")
# experiment28(491,u1_2_3,5000,0.66,3)

#experiment29(u1_2[:100],3,u1_2[100]+2)

# for k in range(1,25):
#     print(k)
#     for n in range(10,0,-1):
#         #print(math.log(ft(k*alpha1_2,u1_2[:len(u1_2)//n]))/math.log((len(u1_2)//n)))
#         print(ft(k*alpha1_2,u1_2[:len(u1_2)//n])/(len(u1_2)//n), math.log(ft(k*alpha1_2,u1_2[:len(u1_2)//n]))/math.log(len(u1_2)//n))

# for x in u1_2[:10000]:
#     print(math.cos(alpha1_2*x),math.sin(alpha1_2*x))

# N=2
# while N <= len(u1_2):
#     N = (3*N)//2
#     print((2*sum(u1_2[:N])//alpha1_2)/(N*N))
    

# N = len(u1_2)
# u1_2s = [i*i for i in u1_2]
# print((sum(u1_2s)/sum(u1_2))/((2*N+1)/3)/alpha1_2)

# r = 2
# s = 1/3
# a = math.sqrt(2)
# N = 10000
# l = []
# for n in range(N):
#     x = math.floor(random.gauss(r, 1))
#     for j in range(x):
#         l += [n*a + random.uniform(-s,s)]


# n = len(l)
# ls = [i*i for i in l]
# print((sum(ls)/sum(l))/((2*(n//r)+1)/3))
    


# l = theta("01001",10000)[0]
# for x in l:
#     print(x)


#find_alpha(sf01001,prec=4)

alpha01001 = 2.5086204384047996 #2.508619
beta01001 = 1.26594784

# print(len(sf01001))

# for N in range(1000,10000,1000):
#     print(N,ft(alpha01001,sf01001[:N]))

#print(alpha01001/(2*math.pi))
# [ 2, 1, 1, 53, 2, 1, 1, 3, 5, 2, 7, 5, 2, 9, 2, 1, 1, 4, 13, 3, 1, 728, 17, 1, 3 ]
# 1/2
# 1/3
# 2/5
# 107/268
# 216/541
# 323/809
# 539/1350
# 1940/4859
# 10239/25645
# 22418/56149
# 167165/418688
# 858243/2149589
# 1883651/4717866
# 17811102/44610383
# 37505855/93938632
# 55316957/138549015
# 92822812/232487647
# 426608205/1068499603
# 5638729477/14122982486
# 17342796636/43437447061
# 22981526113/57560429547
# 16747893806900/41947430157277
# 284737176243413/713163873103256
# 301485070050313/755111303260533

# ll = experiment15(sf01001,216,541)
# for i in range(len(ll)):
#     print(i,ll[i])

# S = set(u1_2[:10000])
# S2 = sorted(list({x for x in S if x-2 in S}))

# Sa = []
# la = 2*math.pi/alpha1_2
# for x in u1_2[:10000]:
#     r = real_mod(x,la)
#     if(la/3 <= r and r <= 2*la/3):
#         Sa.append(x)
# print(Sa)

# ll = thetainv(Sa,10000)
# for x in ll:
#     print(x,end="")
# print("")

# [ 3, 4, 1, 2, 2, 3, 5, 2, 1, 10, 6, 1, 1, 2, 1, 2, 1, 1, 1, 22, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 126, 1, 1, 2, 3 ]
# 1/3
# 4/13
# 5/16
# 14/45
# 33/106
# 113/363
# 598/1921
# 1309/4205
# 1907/6126
# 20379/65465
# 124181/398916
# 144560/464381
# 268741/863297
# 682042/2190975
# 950783/3054272
# 2583608/8299519
# 3534391/11353791
# 6117999/19653310
# 9652390/31007101
# 218470579/701809532
# 228122969/732816633
# 446593548/1434626165
# 674716517/2167442798
# 1121310065/3602068963
# 1796026582/5769511761
# 4713363229/15141092485
# 6509389811/20910604246
# 17732142851/56962300977
# 24241532662/77872905223
# 41973675513/134835206200
# 108188883688/347543317623
# 258351442889/829921841446
# 32660470687702/104917695339819
# 32918822130591/105747617181265
# 65579292818293/210665312521084
# 164077407767177/527078242223433

# find_alpha(sf10010,prec=4)

# ll = experiment15(sf10010,113,363)
# for i in range(len(ll)):
#     print(i,ll[i])

# ll = theta1("11",200)[0]
# for x in ll:
#     print(x)
# print("")

# l = theta("01001",100000)[0]
# for x in l:
#     print(x)

# find_alpha(sf01001,s=0.2,prec=10,candidates=[alpha01001])

# ll = thetainv(theta("10010",10000)[0][1:],4500)
# for x in ll:
#     print(x,end="")
# print("")
