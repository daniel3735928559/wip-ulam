import math,sys,random,bisect,copy

from utils import *
        
u1_2 = read_seq("seqs/seq1,2")
u1_3 = read_seq("seqs/seq1,3")
u1_4 = read_seq("seqs/seq1,4")
u2_3 = read_seq("seqs/seq2,3")
u2_5 = read_seq("seqs/seq2,5")
u12_13 = read_seq("seqs/seq12,13")
u1_2_3 = read_seq("seqs/seq1,2,3")
sf01001 = read_seq("seqs/sf01001")
sf01010 = read_seq("seqs/sf01010")
sf10010 = read_seq("seqs/sf10010")
linus = read_seq("seqs/1linus")
alpha1_2 = 2.5714474995
alpha1_4 = 0.506013502
alpha1_2_3 = 0.23036348 # 0.23034156 #0.23034016
alpha01001 = 2.5086204384047996 #2.508619
beta01001 = 1.26594784

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
    """Compute alpha_{a,b} for various a,b"""
    n = 500
    s = 0.0001
    l = [(1,i) for i in range(2,16)]
    l += [(2,3)]
    l += [(3,i) for i in range(4,11) if i % 3 != 0]
    l += [(4,i) for i in range(4,16) if i % 2 != 0]
    l += [(5,i) for i in range(7,10)]
    for x in l:
        a,b=x
        u = ulam(a,b,n)
        alpha,f = find_alpha(u,s,debug=False)
        print(a,b,alpha,f/u[-1],2*math.pi/alpha)

def experiment2():
    """Compute alpha_{a,b} for various a,b"""
    l = {"01001":sf01001,"01010":sf01010,"10010":sf10010}
    for s in l:
        A = l[s][:1000]
        alpha,f = find_alpha(A,0.001,debug=True)
        print(s,alpha,f/A[-1],2*math.pi/alpha)

def experiment3():
    x = 10
    for p in [i/x for i in range(x+1)]:
        print(p)
        y = 200
        ll = [len(extend_few_reps([1,2],1000,0.5)) for xx in range(y)]
        mu = sum(ll)/y
        print(sum([(mu - xx)**2 for xx in ll])/y)
    #s = 0.001
    #print(find_alpha(l,s,debug=False))

def experiment4():
    l = u1_2[:1000000]
    a = alpha1_2
    for i in range(1,10):
        print(i,i*ft(a*i,l)/len(l))
        
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
    
def experiment25():
    #print(ulam_rep_dumb_k([1,2,3],5000))
    #print(find_alpha(u1_2_3,prec=4))
    print("asd",alpha1_2_3/(2*math.pi))
    print(2*math.pi/alpha1_2_3)
    a=alpha1_2_3/(2*math.pi)
    la = 2*math.pi/alpha1_2_3
    lambda1_2_3 = la-2*math.pi*int(la/(2*math.pi))
    print(lambda1_2_3)
    
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

def experiment30(l,a,N):
    f1 = ft(a,l)
    for k in range(1,N):
        f = ft(k*a,l)/f1
        print(k,f,k*f)

def experiment31(a,b,N):
    l = []
    for i in range(N):
        r = real_mod(i,a)
        s = real_mod(i,b)
        if a/3 < r and r <= 2*a/3 and b/3 < s and 2*b/3 < s:
            l += [i]
    return l

if len(sys.argv) < 2:
    print("Specify an experiment number")
else:
    exp = 'experiment'+sys.argv[1]
    if exp in locals():
        locals()[exp]()
    else:
        print("Invalid experiment: {}".format(exp))
