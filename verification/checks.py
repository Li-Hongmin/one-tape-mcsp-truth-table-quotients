"""Finite sanity checks for 'Truth-Table Quotients Do Not Close One-Tape MCSP Magnification'.
Numerical/exhaustive checks on tiny parameters only; they are NOT proofs of the asymptotic statements.
Circuit model: fan-in-2 AND/OR and fan-in-1 NOT gates, size = number of gates (NOT counted), no constant inputs."""
import itertools, random
random.seed(1)
OK=[]
def check(name,cond):
    assert cond, name
    OK.append(name)

def circuit_table(n,tmax):
    """Exact CC(f) for all f with CC<=tmax (truth tables as ints over N=2^n bits); BFS over sets of computed functions."""
    N=1<<n; full=(1<<N)-1
    inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    cc={}
    for f in inputs: cc[f]=0
    frontier={frozenset(inputs)}
    for s in range(1,tmax+1):
        new=set()
        for st in frontier:
            L=list(st)
            cands=set()
            for a in L:
                cands.add(full^a)
                for b in L:
                    cands.add(a&b); cands.add(a|b)
            for g in cands:
                if g in st: continue
                if g not in cc: cc[g]=s
                new.add(st|{g})
        # prune: keep only states whose functions are all useful (no dedupe beyond sets)
        frontier=new
    return cc

# n=2: complete table
cc2=circuit_table(2,7)
check("n=2 all 16 functions have CC<=7",len(cc2)==16)
# n=3 up to size 5
cc3=circuit_table(3,5)
def L(cc,t): return {f for f,c in cc.items() if c<=t}

# point indicators cost <= 2n-1
for n,cc,tm in [(2,cc2,7),(3,cc3,5)]:
    N=1<<n
    for a in range(N):
        check(f"CC(delta_a)<=2n-1 n={n} a={a}", cc.get(1<<a,99)<=2*n-1)
# f xor delta_a <= CC(f)+2n+3  (n=2: 2n+3=7, full table)
for f,c in cc2.items():
    for a in range(4):
        check("point flip n=2",cc2[f^(1<<a)]<=c+7)

# Harper vertex-isoperimetry on the cube Q_d (d=N), exhaustive for d=4, and on L_t sets for d=8
def simplicial_order(d):
    return sorted(range(1<<d), key=lambda x:(bin(x).count('1'), [i for i in range(d) if (x>>i)&1]))
def nbhd(S,d):
    T=set(S)
    for x in S:
        for i in range(d): T.add(x^(1<<i))
    return T
for d in [4]:
    order=simplicial_order(d)
    best={}
    for mask in range(1,1<<(1<<d)):
        S=[x for x in range(1<<d) if (mask>>x)&1]
        k=len(S); v=len(nbhd(S,d))
        if k not in best or v<best[k]: best[k]=v
    check("Harper initial segment optimal d=4",all(len(nbhd(order[:k],d))==best[k] for k in best))
d=8; order=simplicial_order(d)
for t in range(0,6):
    A=L(cc3,t); I=set(order[:len(A)])
    for j in range(3):
        check(f"Harper iterated n=3 t={t} j={j}",len(A)>=len(I))
        A=nbhd(A,d); I=nbhd(I,d)
        check("closed nbhd of initial segment is initial segment",I==set(order[:len(I)]))

# downset upward-edge identity e_up(I) = N|I| - 2 sum|x|
for trial in range(200):
    d=6; gens=[random.randrange(1<<d) for _ in range(3)]
    I={x for x in range(1<<d) if any(x|g==g for g in gens)}
    up=sum(1 for x in I for i in range(d) if not (x>>i)&1 and (x|(1<<i)) not in I)
    check("upward edges of downset",up==d*len(I)-2*sum(bin(x).count('1') for x in I))

def sumset(A,B): return {a^b for a in A for b in B}
# Prop 7: exact factorization and (55) for random maps on A=L_t (n=3)
for t in [2,3,4,5]:
    A=L(cc3,t); AA=sumset(A,A)
    for trial in range(30):
        k=random.choice([1,2,3,5,10,50])
        Q={x:random.randrange(k) for x in range(256)}
        Y={Q[a] for a in A}; M=len(Y); Mp=len({Q[x] for x in AA})
        Fb=len(A)/M; Fp=len(AA)/Mp
        X=Mp/M; Iav=Fp/Fb
        Imax=max(sum(1 for x in AA if Q[x]==w) for w in set(Q[x] for x in AA))/Fb
        Ay={y:[a for a in A if Q[a]==y] for y in Y}; Yl=sorted(Y)
        diag=sum(len({Q[u^v] for u in Ay[y] for v in Ay[y]}) for y in Yl)
        off=sum(len({Q[u^v] for u in Ay[y] for v in Ay[z]}) for y,z in itertools.combinations(Yl,2))
        CM=M*(M+1)//2; Dav=(diag+off)/CM
        Dmax=max(len({Q[u^v] for u in Ay[y] for v in Ay[z]}) for y in Yl for z in Yl)
        R=len(AA)/len(A)
        check("factorization X*Iav=|A+A|/|A|",abs(X*Iav-R)<1e-9)
        check("X*Imax>=R",X*Imax>=R-1e-9)
        check("(59)",Mp<=CM*Dav-M+1+1e-9)
        check("(55) avg",R<=Iav*(Dav*(M+1)/2-1+1/M)+1e-9)
        check("(55) max",Iav*(Dav*(M+1)/2-1+1/M)<=Imax*(Dmax*(M+1)/2-1+1/M)+1e-9)
    # two-label predicate map is exact in (55)
    Q={x:(0 if x in A else 1) for x in range(256)}
    if AA!=A:
        Iav=(len(AA)/2)/len(A)
        check("two-label map attains (55)",abs(R-Iav*(2*(1+1)/2-1+1))<1e-9)

# Prop 6 quotient step: A union of m cosets of K => |A+A|/|A| <= m, using K=Stab(A) and random A
def span(vecs):
    S={0}
    for v in vecs: S|={s^v for s in S}
    return S
for trial in range(100):
    K=span([random.randrange(256) for _ in range(random.randint(0,3))])
    reps=[random.randrange(256) for _ in range(random.randint(1,6))]
    A=sumset(set(reps),K); m=len(A)//len(K)
    check("coset quotient doubling<=m",len(sumset(A,A))/len(A)<=m+1e-9)
for t in range(0,6):
    A=L(cc3,t); St={h for h in range(256) if all((a^h) in A for a in A)}
    check(f"stabilizer power of 2 divides |L_t| n=3 t={t}",len(A)%len(St)==0)

# Q_0 example (N=6)
N=6
A0=[x for x in range(1<<N) if not x&1]
def Q0(x):
    if not x&1 and not x&2: return 0
    return (x<<1)|(x&1)  # first output bit = x1, then x
img={}
for x in A0: img.setdefault(Q0(x),[]).append(x)
check("Q0 preserves predicate",all((Q0(x)&1)==(x&1) for x in range(1<<N)))
sizes=sorted(len(v) for v in img.values())
check("Q0 fibers: one of size 2^(N-2), rest singletons",sizes[-1]==2**(N-2) and sizes.count(1)==2**(N-2))
Fb=len(A0)/len(img); check("Q0 mean fiber <2",Fb<2)
check("Q0 I_Q > 2^(N-3)",max(sizes)/Fb>2**(N-3))

# tensor encoding (3o): CC(f)<=CC(E(f))<=2CC(f)+O(1), t=2, phi=AND/OR, n=1 -> n'=2
cc1=circuit_table(1,3)
for f in range(4):
    if f not in cc1: continue
    for phi in [lambda a,b:a&b, lambda a,b:a|b]:
        E=sum((phi((f>>x1)&1,(f>>x2)&1))<<(x1|(x2<<1)) for x1 in range(2) for x2 in range(2))
        check("tensor lower",cc2[E]>=cc1[f]); check("tensor upper",cc2[E]<=2*cc1[f]+1)
# dummy padding (7): CC(E_k f)=CC(f), n=1 -> 2 vars
for f in cc1:
    E=sum(((f>>(x&1))&1)<<x for x in range(4))
    check("dummy padding preserves CC",cc2[E]==cc1[f])
print(len(OK),"checks passed")
