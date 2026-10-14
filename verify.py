import math, json
age=[3,7,14,21,28]; load=[[385,395,400],[525,535,545],[655,665,680],[740,755,760],[800,815,830]]
x=[a for a in age for _ in range(3)]; y=[p*1000/22500 for r in load for p in r]
N=len(x)
def lin(X,Y):                      # booklet slide formulas
    n=len(X); sx=sum(X); sy=sum(Y); sxx=sum(a*a for a in X); sxy=sum(a*b for a,b in zip(X,Y))
    b=(n*sxy-sx*sy)/(n*sxx-sx**2); a=sy/n-b*sx/n; return a,b
def solve3(M,v):                   # Cramer's rule
    def det(m): return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    D=det(M); out=[]
    for j in range(3):
        Mj=[row[:] for row in M]
        for i in range(3): Mj[i][j]=v[i]
        out.append(det(Mj)/D)
    return out
def r2(f): 
    m=sum(y)/N; return 1-sum((yi-f(xi))**2 for xi,yi in zip(x,y))/sum((yi-m)**2 for yi in y)
def rmse(f): return math.sqrt(sum((yi-f(xi))**2 for xi,yi in zip(x,y))/N)
out={}
a,b=lin(x,y); f=lambda t:a+b*t; out["Linear"]=(f"{a:.4f}+{b:.5f}t",r2(f),rmse(f),f(10),f(35))
S=lambda k:sum(t**k for t in x); T=lambda k:sum(t**k*v for t,v in zip(x,y))
a,b,c=solve3([[N,S(1),S(2)],[S(1),S(2),S(3)],[S(2),S(3),S(4)]],[T(0),T(1),T(2)])
f=lambda t:a+b*t+c*t*t; out["Quadratic"]=(f"{a:.4f}+{b:.5f}t{c:+.6f}t^2",r2(f),rmse(f),f(10),f(35))
a,b=lin([math.log(t) for t in x],y); f=lambda t:a+b*math.log(t); out["Logarithmic"]=(f"{a:.4f}+{b:.5f}ln t",r2(f),rmse(f),f(10),f(35))
A,b=lin(x,[math.log(v) for v in y]); a=math.exp(A); f=lambda t:a*math.exp(b*t); out["Exponential"]=(f"{a:.4f}exp({b:.6f}t)",r2(f),rmse(f),f(10),f(35))
for k,v in out.items(): print(f"{k:12s}{v[0]:42s} R2={v[1]:.4f} RMSE={v[2]:.3f} f10={v[3]:.2f} f35={v[4]:.2f}")
# fit on the 5 mean strengths only (alternative reading)
xm=age; ym=[sum(r)/3*1000/22500 for r in load]
print("\nMEANS-ONLY fit")
def r2m(f): m=sum(ym)/5; return 1-sum((b-f(a))**2 for a,b in zip(xm,ym))/sum((b-m)**2 for b in ym)
a,b=lin(xm,ym); print("Linear",round(a,4),round(b,5),round(a+10*b,2),round(a+35*b,2))
a,b=lin([math.log(t) for t in xm],ym); print("Log",round(a,4),round(b,5),round(a+b*math.log(10),2),round(a+b*math.log(35),2))
A,b=lin(xm,[math.log(v) for v in ym]); a=math.exp(A); print("Exp",round(a,4),round(b,6),round(a*math.exp(10*b),2),round(a*math.exp(35*b),2))
# hand check of log fit on the 15 points using sums
z=[math.log(t) for t in x]; print("\nsum z",sum(z),"sum y",sum(y),"sum z^2",sum(i*i for i in z),"sum zy",sum(i*j for i,j in zip(z,y)))
# check ln(t) fit passes near data
print("log model at 3,7,14,21,28:",[round(7.904+8.3746*math.log(t),2) for t in age],"means",[round(v,2) for v in ym])
# percent errors
print("max |resid| log:",max(abs(yi-(out['Logarithmic'] and (7.9040+8.37458*math.log(xi)))) for xi,yi in zip(x,y)))
