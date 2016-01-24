import math,sys,random,bisect

## Utility functions: 

def read_seq(fn):
    l = []
    with open(fn) as f:
        for x in f:
            l.append(int(x))
    return l

def red(x):
    return abs(x - 2*math.pi*math.floor(x/2*math.pi)-math.pi)

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

def extend_with_storage_careful(l,c,dq,N,debug=True):
    ans = l
    top = l[-1]
    candidates = c
    candidates_list = sorted([-x for x in c])
    disqualified = dq
    prev_an = 0
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
                disqualified.pop(i,None)
            prev_an = an
            if(debug):
                print(c,len(disqualified))
            sys.stdout.flush()
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

def find_alpha(l,s=.02,prec=2):
    a = 0.2
    winner = a
    curmax = 0
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
    s = {x : [] for x in l}
    for i in range(2,len(l)):
        for j in range(i):
            if(l[i] - l[j] in s):
                s[l[j]].append(i)
                break
    for x in s:
        if(len(s(x)) < 10):
            continue
        lm = [0 for i in range(m)]
        for i in s[x]:
            lm[(k*l[i])%m]+=1
        print("{} \t{} \t{} \t{} \t{} \t{}".format(x,len(s[x]), a*x-2*math.pi*math.floor(a*x/(2*math.pi)), math.cos(a * x), (k*x)%m, lm))
    return 


def experiment15(l,k,m):
    cs = [0 for i in range(m)]
    for x in l:
        cs[(k*x) % m] += 1
    print(cs)


def experiment16(l):
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
        print(a,ans[a],ans[a][0]/ans[a][1] if ans[a][1] > 0 else 0)

def experiment17(l,k,m):
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
        if(lo != 0 and hi != 0):
            weird += [(a,lo,hi)]
        print(a,lo,hi,coms[a])
    print("WEIRD")
    for w in weird:
        print(w)

def breakdown(s,u,k,m):
    if((k*u)%m < m/3 or (k*u)%m > 2*m/3):
        return [u]
    if(s[u][0] == 0):
        return [s[u][1]]
    if(s[u][1] == 0):
        return [s[u][0]]
    
    return breakdown(s,s[u][0],k,m) + breakdown(s,s[u][1],k,m)
    
def experiment18(l,us,k,m):
    s = {x:() for x in l}
    s[l[0]] = (0,l[0])
    s[l[1]] = (0,l[1])
    for a in l:
        for x in s:
            if(a-x in s and a-x != x):
                s[a] = (x,a-x) if x < a-x else (a-x,x)
                break
    for u in us:
        print(breakdown(s,u,k,m))
    
u1_2 = read_seq("seqs/seq1,2")
u1_3 = read_seq("seqs/seq1,3")
u1_4 = read_seq("seqs/seq1,4")
u2_3 = read_seq("seqs/seq2,3")
u2_5 = read_seq("seqs/seq2,5")
u12_13 = read_seq("seqs/seq12,13")
alpha1_2 = 2.5714474995
alpha1_4 = 0.506013502

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
#experiment16(u1_2)
#experiment17(u1_2[:100000],2219,5422)
experiment18(u1_2[:100],u1_2[50:60],2219,5422)
