import math,sys,random,bisect,copy,time

from utils import *
        
u1_2 = read_seq("seqs/seq1,2")
u1_3 = read_seq("seqs/seq1,3")
u1_4 = read_seq("seqs/seq1,4")
u1_9 = read_seq("seqs/seq1,9")
u1_11 = read_seq("seqs/seq1,11")
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
lambda1_2 = 5422,2219
lambda1_3 = 6424,2897
lambda01010 = 3923,1125
lambda01001 = 1350,539
beta01001 = 1.26594784

data = {
    "u1_2":{"seq":u1_2,"alpha":alpha1_2,"lambda":(5422,2219),"lambda_s":(540,221)},
    "u1_3":{"seq":u1_3,"alpha":2.8334973144531252,"lambda":(6424,2897),"lambda_s":(1244,561)},
    "u1_4":{"seq":u1_4,"alpha":0.5060131835937502,"lambda":(2769,223),"lambda_s":(149,12)},
    "u2_3":{"seq":u2_3,"alpha":1.16501220703125,"lambda":(2551,473),"lambda_s":(480,89)},
    "u1_9":{"seq":u1_9,"alpha":0.229169921875,"lambda":(4798,175),"lambda_s":(329,12)},
    "01001":{"seq":sf01001,"alpha":2.508619384765625,"lambda":(8909,3557),"lambda_s":(541,216)},
    "01010":{"seq":sf01010,"alpha":1.8018310546875,"lambda":(3923,1125),"lambda_s":(136,39)},
    "10010":{"seq":sf10010,"alpha":1.9559313964843752,"lambda":(9968,3103),"lambda_s":(363,113)},
}

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
    n = 10000
    l = []
    l += [(1,i) for i in range(2,16)]
    l += [(2,3)]
    l += [(3,i) for i in range(4,11) if i % 3 != 0]
    #l += [(4,i) for i in range(4,16) if i % 2 != 0]
    l += [(5,i) for i in range(7,10)]
    for x in l:
        a,b=x
        u = u1_11#ulam(a,b,n)
        alpha,f = find_alpha_fast(u,debug=True)
        F = ft_complex(alpha,u)
        print(a,b,alpha,f/u[-1],2*math.pi/alpha,len(u)/u[-1],f/len(u),"{} + {}i".format(*F))

def experiment1A():
    """Compute alpha_{2,5}"""
    u = ulam(2,5,10000)
    alpha,f = find_alpha_fast(u,debug=False)
    print(a,b,alpha,f/u[-1],2*math.pi/alpha,len(u)/u[-1],f)

def experiment1B():
    """Compute alpha_{1,11}"""
    u = u1_11
    alpha,f = find_alpha_fast(u,debug=True)
    F = ft_complex(alpha,u)
    print(a,b,alpha,f/u[-1],2*math.pi/alpha,len(u)/u[-1],f/len(u),"{} + {}i".format(*F))
            
def experiment1C():
    """Compute alpha_{a,b} for various 1,11-15"""
    n = 20000
    l = [(1,i) for i in range(11,16)]
    for x in l:
        a,b=x
        u = ulam(a,b,n)
        alpha,f = find_alpha_fast(u,debug=False,start=0.1,end=0.2)
        F = ft_complex(alpha,u)
        print(a,b,alpha,f/u[-1],2*math.pi/alpha,len(u)/u[-1],f/len(u),"{} + {}i".format(*F))

def experiment2():
    """Compute alpha_{s} for various s"""
    l = {"01001":sf01001,"01010":sf01010,"10010":sf10010}
    for s in l:
        A = l[s][:10000]
        alpha,f = find_alpha_fast(A,debug=False)
        F = ft_complex(alpha,A)
        print(s,alpha,f/A[-1],2*math.pi/alpha,len(A)/A[-1],f/len(A),"{} + {}i".format(*F))

def experiment2A():
    """Compute alpha_01001 for various s"""
    A = sf01001[:20000]
    alpha,f = find_alpha_fast(A,s=0.0025,debug=True)
    F = ft_complex(alpha,A)
    print(s,alpha,f/A[-1],2*math.pi/alpha,len(A)/A[-1],f/len(A),"{} + {}i".format(*F))

def experiment3():
    """Compute variance of Ulam numbers mod various convergents to alpha"""
    l = u1_2
    ms = [2, 5, 17, 22, 259, 281, 540, 2441, 2981]
    for m in ms:
        rs = [0 for k in range(m)]
        for x in l:
            rs[x%m] += 1
        mu = sum(rs)/m
        var = sum([(r-mu)**2 for r in rs])/m
        print(m,var)

def experiment3A():
    """Compute variance of Ulam numbers mod various less good rational approximations to alpha"""
    l = u1_2
    R = 3
    ms = [540+i for i in range(-R,R+1)] + [2441 + i for i in range(-R,R+1)]
    for m in ms:
        rs = [0 for k in range(m)]
        for x in l:
            rs[x%m] += 1
        mu = sum(rs)/m
        var = sum([(r-mu)**2 for r in rs])/m
        print(m,var)


def experiment3_old():
    """ """
    ls = {"u1_2":(u1_2[:1000],alpha1_2)}
    for s in ls:
        l,alpha = ls[s]
        N = l[-1]
        tot = 0
        for k in range(int(N/2)):
            tot += ft(alpha*k,l)**2
        print(s,tot/N)

def experiment30():
    """Probabalistic version"""
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
    """Search (somewhat) efficiently (if somewhat approximately) for smallest k where ft(k*alpha) > 4/k"""
    for s in data:
        l = data[s]["seq"][:100000]
        a = data[s]["alpha"]
        N = 100
        k_prev = 0
        while N < len(l):
            f = 0
            k = N
            w = N/2
            while(w > 10):
                f = max([j*ft(j*a,l[:N])/l[N] for j in range(k-10,k+10)])
                #print(k,f)
                if f > 4: k -= w
                else: k += w
                k = math.floor(k+0.5)
                w *= 1/2
            x = k+10
            for j in range(k_prev-20,x+10):
                if(j*ft(j*a,l[:N])/l[N] > 4):
                    k = j
                    break
            k_prev = k
            print(s,l[N],k)
            N = math.floor(N * 1.5)

def experiment4A():
    """Compute i*ft(A)(alpha*i) for increasing i"""
    l = u1_2[:1000000]
    a = alpha1_2
    for i in range(1,10):
        print(i,i*ft(a*i,l)/len(l))

def experiment5():
    """Compute distribution mod lambda for the sequences"""
    for s in data:
        l = data[s]["seq"][:10000]
        m,k = data[s]["lambda_s"]
        rs = {i:0 for i in range(m)}
        for x in l:
            rs[(k*x)%m] += 1
        for x in range(m):
            print(s,x,rs[x])
            
def experiment5_old():
    l = u1_2
    a = 2.5714474995
    for k in range(100000):
        d = k*a-2*math.pi*math.floor(k*a/(2*math.pi))
        f = ft(k*a,l)
        if abs(d) > 0.1 and abs(2*math.pi - d) > 0.1 and f > 1000:
            print(k,d,f)

def experiment6():
    """Compute distribution of r_{A+A} mod lambda for the sequences"""
    for s in data:
        l = data[s]["seq"][:10000]
        m,k = data[s]["lambda"]
        
        N = l[-1] - (l[-1]%m)
        rAA = {i:0 for i in range(N)}
        for x in l:
            for y in l:
                if y > x or x+y >= N:
                    break
                rAA[x+y] += 1
        rAA_dist = [0 for i in range(m)]
        for x in range(N):
            rAA_dist[x%m] += rAA[x]
        for x in range(m):
            rAA_dist[x] /= N/m
        for x in range(m):
            print(s,(x*k)%m,rAA_dist[x])

def experiment7():
    """Compute complete spectrum of A--that is, any x with |ft(A_N)(x)| > sqrt(N)"""
    n = 5000
    for s in data:
        l = data[s]["seq"][:n]
        N = l[-1]
        spec = []
        x = 0
        step = 10/N
        while x <= math.pi+step:
            f = ft(x,l)
            if f > math.sqrt(2*N):
                print(s,round(x,4),f)
                spec += [(round(x,4),f)]
            x += step
            #print("step",x)
        #for a in spec:
        #    print(s,a[0],a[1])

def experiment7A():
    spec_size = {
        "01001":22,
        "10010":4,
        "01010":7,
        "u1_2":11,
        "u1_3":52,
        "u1_4":50,
        "u1_9":121,
        "u2_3":24,
    }
    """Compute k*alpha mod 2pi for various k"""
    for s in data:
        a = data[s]["alpha"]
        for k in range(2*spec_size[s]):
            r = real_mod(k*a,2*math.pi)
            if r > math.pi:
                r = 2*math.pi - r
            print(s,r,k,a)
            
def experiment7B():
    """Compute the difference between r_{A_N+A_N}(x) and sum |k|<sqrt(N) ft(A_N)(k*alpha)"""
    for s in data:
        for N in [500,1000,2000,5000,7500]:
            a = data[s]["alpha"]
            l = data[s]["seq"][:N]
            # rAA = {i:0 for i in range(l[-1])}
            # for x in l:
            #     for y in l:
            #         if y > x or x+y >= l[-1]:
            #             break
            #         elif x == y:
            #             rAA[x+y] += 1
            #             break
            #         else:
            #             rAA[x+y] += 2
            la = 2*math.pi/a
            m = 2*l[-1]
            k = math.floor(la*m+0.5)%m
            fts = [ft_complex_2pi(t,l,m) for t in range(m)]
            fts_a = [ft_complex(t*a,l) for t in range(math.floor(math.sqrt(m)))]
            errs = []
            for x in range(l[-1]//2,l[-1]//2+200):
                ccs = [(1/m)*((fts[t][0]**2 - fts[t][1]**2)*math.cos(2*math.pi*t*x/m)+2*fts[t][0]*fts[t][1]*math.sin(2*math.pi*t*x/m)) for t in range(m)]
                ccs_a = [(1 if t == 0 else 2) * (1/m)*((fts_a[t][0]**2 - fts_a[t][1]**2)*math.cos(t*a*x)+2*fts[t][0]*fts[t][1]*math.sin(t*a*x)) for t in range(math.floor(math.sqrt(m)))]
                # bigs = [ccs[0]]
                # for i in range(1,math.floor(math.sqrt(m))):
                #     bigs += [ccs[(i*k)%m],ccs[(-i*k)%m]]
                b = sum(ccs_a)
                c = sum(ccs)
                #print(s,x,rAA[x],round(c,2),round(b,2),round(b-c,2),round((b-c)/m,7))
                errs += [b-c]
            Rm_max = max(errs,key=lambda x: abs(x))
            Rm_avg = sum(errs)/len(errs)
            print(s,m,round(Rm_avg,3),round(Rm_max,3), round(Rm_avg/m,7))

def experiment7C():
    """Compute complete spectrum of A--that is, any x with |ft(A_N)(x)| > sqrt(N)"""
    for s in ["u1_2"]:
        l = data[s]["seq"]
        spec = []
        N = l[-1]
        x = 0
        step = 0.0005
        while x <= math.pi+step:
            n = 10000
            f = ft(x,l[:n])
            logf = math.log(f)/math.log(l[n])
            print(s,round(x,4),round(logf,4))
            x += step
        # for a in spec:
        #     print(s,a[0],a[1])

def experiment7D():
    """Take some values of beta for each sequence that seem to be large Fourier coeffs outside alphaZ and test them"""
    betas = {
        "u1_3":[0.062,1.909,2.7715,1.662],
        "u1_9":[0.012,0.032,0.2555,0.271],
        "u2_3":[2.3695,1.271,2.436,0.0605],
        }
    for s in betas:
        l = data[s]["seq"]
        for b in betas[s]:
            b,f = search_alpha(l,b)
            fs = fts(b,l,1000,10)
            print(s+","+str(b)+',"'+", ".join([str(round(x[2]/x[0],4)) for x in fs])+'"')

            
def experiment7_old():
    l = u1_2[:10000]
    ll = set(l)
    lm = 2*math.pi/alpha1_2
    for i in range(5000):
        s = 0
        for j in range(i):
            if l[i] - l[j] in ll:
                s = l[j]
                break
        print(i+1,real_mod(l[i],lm),l[i],s)

def experiment8():
    """Compute ping-pong sequence mod sqrt(2)"""
    n = 500
    m = math.sqrt(2)
    a,b,c = 0,0,0
    for i in range(1,1000):
        r = real_mod(i,m)
        if r < m/12:
            a = i
        elif a != 0 and r > 11*m/12 and i % a != 0:
            b = i
        elif a != 0 and b != 0 and r > m/3 and r < m/2:
            c = i
        if a != 0 and b != 0 and c != 0:
            break
    print(a,b,c)
    A = [a,b,c]
    x = c
    bat = a
    for i in range(n):
        if bat == a:
            if real_mod(x+bat,m) < 2*m/3:
                x += bat
                A += [x]
            else:
                bat = b
        else:
            if real_mod(x+bat,m) > m/3:
                x += bat
                A += [x]
            else:
                bat = a
    for x in A:
        print(x)
    S = {x:0 for x in A}
    for x in A:
        for y in A:
            if y >= x:
                break
            if x+y in S:
                S[x+y] += 1

    for x in A:
        print(x,S[x])
            

def experiment9():
    """Compute density for various sequences"""
    for s in data:
        l = data[s]["seq"]
        n = len(l)
        n -= n%1000
        #while n > 1000:
        print("{},{},{} = \\frac{{1}}{{{}}}".format(s,n,round(n/l[n-1],5),round(l[n-1]/n,5)))
        #    n //= 2
    
def experiment10():
    """Compute non-sums for various sequences"""
    for s in ["u1_2","u1_3","u1_9","u2_3"]:
        l = data[s]["seq"][:10000]
        m,k = data[s]["lambda_s"]
        ss = set(l)
        nonsums = {x:0 for x in range(m)}
        for x in range(l[-1]):
            for y in l:
                if x-y in ss:
                    break
                elif y >= x/2:
                    nonsums[(k*x)%m] += 1
                    break
        for x in range(m):
            print(s,x,nonsums[x])

def experiment11():
    l = u1_2[:1000000]
    s = set(l)
    summands = {}
    for i in range(2,len(l)):
        x = l[i]
        for j in range(i):
            y = l[j]
            if y >= x/2:
                break
            if x-y in s:
                summands[y] = summands.get(y,0)+1
                break
                
    la = 2*math.pi/alpha1_2
    ll = sorted([(y,summands[y]/len(l)) for y in summands if summands[y] > 1],key=lambda x:x[1])
    for x in ll:
        y,p = x
        q1,q2 = (y + (1 - p)/3)/la,(y - (1 - p)/3)/la
        q1m,q2m = (q1 - math.floor(q1)),(q2 - math.floor(q2))
        if q1m > 1/2:
            q1m = 1-q1m
        if q2m > 1/2:
            q2m = 1-q2m
        if(q1m < q2m):
            q = q1
        else:
            q = q2
        q = round(q,4)
        r = real_mod(y,la)/la
        if r > 1/2:
            r = 1 - r
        print(y,p,r,p+3*r,q1,q2)

def experiment12():
    """Compute how often each element x of l occurs as any summand and compare with x mod lambda"""
    for d in ["u1_2"]:
        l = data[d]["seq"][:10000]
        a = data[d]["alpha"]
        lam = 2*math.pi/a
        s = {x : [] for x in l}
        for i in range(2,len(l)):
            for j in range(i):
                if(l[i] - l[j] in s):
                    s[l[j]].append(l[i])
                    s[l[i] - l[j]].append(l[i])
                    break
        for x in s:
            r = real_mod(x/lam,1)
            if r > .5:
                r = 1-r
            print("{} {} {}".format(x,len(s[x]), r))

def experiment14A(l,a,k,m):
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

def experiment14B(l):
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

def experiment14C(l,k,m):
    """Compute a histogram of values of a_i mod lambda"""
    cs = [0 for i in range(m)]
    for x in l:
        cs[(k*x) % m] += 1
    print(cs)
    return cs

def experiment15():
    for s in ["u1_9"]:
        l = data[s]["seq"]
        a = data[s]["alpha"]
        lam = 2*math.pi/a
        for i in range(7):
            print('y =',i*lam/6)
        for i in range(100):
            print(i+1,real_mod(l[i],lam))
    
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
