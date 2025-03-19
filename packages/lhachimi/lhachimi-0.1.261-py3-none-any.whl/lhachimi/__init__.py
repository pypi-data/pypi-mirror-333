from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sympy import symbols, Eq, linsolve
from scipy.special import lambertw,gamma,beta,polygamma
from scipy.linalg import lu
from collections import defaultdict
from fractions import Fraction
import matplotlib.pyplot as plt
import itertools as it
import math as m
import numpy as np
import sympy as sp
import requests as rq
import os,random
from sympy import multiplicity as val,is_primitive_root,isprime,divisor_count,divisors,legendre_symbol,jacobi_symbol


def PolyNewton(coef, x0, n):
    coef = [Fraction(v) for v in coef]
    d = [i*coef[i] for i in range(1, len(coef))]
    rf, rd = coef[::-1], d[::-1]
    x = Fraction(x0)
    for _ in range(n):
        f = Fraction(0)
        for v in rf: f = f*x + v
        df = Fraction(0)
        for v in rd: df = df*x + v
        x -= f/df
    return x

def log_p(x, N):
    if N < 1:
        return (0, 1)
    a, b = 0, 1
    tn, td = x-1, 1
    for n in range(1, N+1):
        a = a * td + tn * b
        b *= td
        g = m.gcd(abs(a), b)
        a, b = a//g, b//g
        if n < N:
            tn *= -x+1
            td = n + 1
    return (a, b)

def exp_p(x, N):
    if N < 0:
        return (0, 1)
    a, b = 1, 1
    tn, td = 1, 1
    for n in range(1, N+1):
        tn *= x
        td *= n
        a = a * td + tn * b
        b *= td
        g = m.gcd(abs(a), b)
        a, b = a//g, b//g
    return (a, b)

def p_frac(a,b,p,l=10):
    if a>0 and b%p!=0:
        D=[]
        n=a
        i=pow(b,-1,p)
        for _ in range(l):
            d=(n*i)%p
            D.append(d)
            n=(n-d*b)//p
        return D
    if a<0 and b%p!=0:
        L=[p-1-d for d in p_frac(-a,b,p,l)]
        L[0]+=1
        for x in range(l):
            if L[x]>=p:
                c=L[x]//p
                L[x]%=p
                if x+1<l:L[x+1]+=c
        return L
    return [0]*l

def approach(a, b, digits=1):
    str_a = str(abs(a)).replace('.', '')
    str_b = str(abs(b)).replace('.', '')
    return str_a[:digits] == str_b[:digits]

def CRT(matrix):
    def ext_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_, x1, y1 = ext_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_, x, y
    x = 0 
    N = 1 
    data=[list(item) for item in zip(*matrix)]
    remainders=data[0]
    moduli=data[1]
    for i in range(len(remainders)):
        ai, ni = remainders[i], moduli[i]
        gcd_, m1, m2 = ext_gcd(N, ni)
        if (ai - x) % gcd_ != 0:
            return None
        x += (ai - x) // gcd_ * m1 * N
        N = N * ni // gcd_
        x = (x % N + N) % N
    return x, N

def Inv_mod(a, b, n):
    b = b % n
    for x in range(n):
        if (a * x) % n == b:
            return x
            
    return None

def Ord_mod(a, b, n):
    k = 1
    current_value = a % n

    while k < n:
        if current_value == b % n:
            return k
        k += 1
        current_value = (current_value * a) % n
    
    return None

def enum(array, start=1 ,step=1):
    e=[]
    i=start
    while len(e) != len(array):
        e.append(i)
        i +=step
    return e

def Gsort(f, n):
    value_to_indices = defaultdict(list)
    for x in range(1, n + 1,2):
        value = f(x)
        value_to_indices[value].append(x)

    grouped = [[value, indices] for value, indices in value_to_indices.items() if len(indices) > 1]
    return sorted(grouped, key=lambda x: x[0])

def poly(x,coeff_array):
    r=0
    for i in range(len(coeff_array)):
        r+= coeff_array[i] * pow(x,i)
    return r

def poly_regression(x_array,y_array,degree=2):
    poly_features = PolynomialFeatures(degree=degree,include_bias=False)
    X_poly = poly_features.fit_transform(x_array)

    reg = LinearRegression()
    reg.fit(X_poly,y_array)

    return np.concatenate(([reg.intercept_[0]], reg.coef_[0]))

def single_test(n,a):
    exp=n-1
    while not exp & 1:
        exp >>= 1
        if pow(a,exp,n) == n-1:
            return True

    if pow(a,exp,n) == 1:
        return True
    
    return False

def miller_rabin(n,k=40):
    if n <= 1 or n == 4:
        return False
    if n == 2 or n == 3:
        return True
    for _ in range(k):
        a = random.SystemRandom().randrange(2,n-2)
        if not single_test(n,a):
            return False
    return True

def sieve_of_eratosthenes(max):
    is_prime = [True] * (max + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(max**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i , max + 1, i):
                is_prime[j] = False

    primes = [i for i, prime in enumerate(is_prime) if prime]
    return primes

def color(txt,rgb):
    color_id = 16 + (36 * (rgb[0] // 51)) + (6 * (rgb[1] // 51)) + (rgb[2] // 51) 
    return "\033[38;5;"+str(color_id)+"m"+str(txt)+"\033[0m"

def digits(n):
    return [int(digit) for digit in list(str(n))]

def linear_regression(x_array,y_array):
    x_array = np.array(x_array).reshape(-1,1)
    y_array = np.array(y_array).reshape(-1,1)

    model = LinearRegression()
    model.fit(x_array,y_array)

    y0 = model.predict(np.array([1]).reshape(-1,1))[0][0]
    y1 = model.predict(np.array([2]).reshape(-1,1))[0][0]
    
    m=round(y1-y0,3)
    p=round(y0-m,3)

    return m,p

def derive(func):
    x = sp.symbols('x')
    f = func(x)
    f_prime = sp.diff(f, x)
    derivative_func = sp.lambdify(x, f_prime)
    return derivative_func

def primitive(func):
    x = sp.symbols('x')
    f = func(x)
    integral = sp.integrate(f, x)
    integral_func = sp.lambdify(x, integral)
    return integral_func

def integral(func, min, max, limit=1000):
    from scipy.integrate import quad
    integrand = lambda x: func(x)
    result, _ = quad(integrand, min, max, limit=limit)
    return result

def is_consecutive(array):
    if len(array) < 2:
        if len(array) == 1:
            return -1
        else:
            return 1
    
    for i in range(len(array) - 1):
        if abs(array[i] - array[i + 1]) != 1:
            return 0
    
    return 1

def bezout_coeff(a, b):
    def extended_gcd(a, b):
        s0, s1 = 1, 0
        t0, t1 = 0, 1
        r0, r1 = a, b
        while r1 != 0:
            q = r0 // r1
            r0, r1 = r1, r0 - q * r1
            s0, s1 = s1, s0 - q * s1
            t0, t1 = t1, t0 - q * t1
        return r0, s0, t0
    gcd_ab, x, y = extended_gcd(a, b)
    factor = m.gcd(a,b) // gcd_ab
    return x * factor, y * factor

def inv_mod(a,b):
    if m.gcd(a,b) != 1:
        return None
    else:
        u,v=bezout_coeff(a,b)
        return u

def pq_maj(p, q):
    if len(p) != len(q) or sum(p) != sum(q):
        return -1
    
    for i in range(1, len(p)):
        if sum(p[:i]) < sum(q[:i]):
            return q
        if sum(p[:i]) > sum(q[:i]):
            return p

def p_avr(p,xi_array):
    n = len(xi_array)
    perm_ = list(it.permutations(range(n)))
    
    product_ = []
    for perm in perm_:
        product = 1
        for i in range(n):
            product *= xi_array[perm[i]] ** p[i]
        product_.append(product)
    
    avr = sum(product_) / m.factorial(n)
    return avr

def kronecker_delta(i,j):
    if i==j:
        return 1
    else:
        return 0

def muirhead(p,q):
    min= q if pq_maj(p,q) == p else p
    print(str(min) + " ≺ " + str(pq_maj(p,q))) 
    print("=> "+str(p_avr(min,[10,50,8])) + " ≺ " + str(p_avr(pq_maj(p,q),[10,50,8])))

def size(file_name,system='decimal'):
    if system == 'decimal':
        d=1000
    if system == 'binary':
        d=1024
    s=os.path.getsize(file_name)
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB' , 'EB', 'ZB', 'YB']:
        if s < d:
            return str(round(s,3)) + " " + x
        s /= d

def bin_str(binary_str):
    return ''.join([chr(int(bv, 2)) for bv in binary_str.split()])

def str_bin(string,space=True):
    if not space:
        binary_string = ''.join(format(ord(char), '08b') for char in string)
        return binary_string
    else:
        binary_string = ' '.join(format(ord(char), '08b') for char in string)
        return binary_string  

def map(value,fromLow,fromHigh,toLow,toHigh):
    x = (toHigh - toLow) / (fromHigh - fromLow)
    y = (toLow * fromHigh - fromLow * toHigh) / (fromHigh - fromLow)
    return x * value + y

def convert_base(number,base_from, base_to):
    r=[]
    hex_dict={10:'A',11:'B',12:'C',13:'D',14:'E',15:'F'}
    try:
        b10 = int(str(number),base_from)
    except ValueError:
        result, temp, inside = [], '', False
        for char in str(number):
            if char == '(':
                if temp:
                    result.append(temp)
                temp, inside = '', True
            elif char == ')':
                result.append(temp)
                temp, inside = '', False
            else:
                temp += char
                if not inside:
                    result.append(temp)
                    temp = ''
        if temp:
            result.append(temp)
        b10=int(sum(base_from ** i * int(x) for i, x in enumerate(result[::-1])))
    if b10 == 0:
        return "0"
    while b10 > 0:
        if b10 % base_to <= 9:
            r.append(str(b10 % base_to))
        else:
                if base_to != 16:
                    r.append("("+str(b10 % base_to)+")")
                else:
                    r.append(hex_dict[b10 % base_to])
        b10 //= base_to
    r.reverse()
    return "".join(r)

def inv_dict(dict):
    return {v: k for k, v in dict.items()}

def plot(function,min,max,speed=0,verbose=False,error_verbose=False,color="blue",linestyle="solid",linewidth=1.5,scatter=False,scatter_color="red",scatter_size=20,step=0.1,show=True,fig=0):
    x_values=[]
    y_values=[]
    i = min

    if fig != 0:
        plt.figure(fig)

    while i<max:
        E=False
        error=""
        i=round(i,3)
        if is_int(i) == 1 :
            i=int(i)

        try:
            v=function(i)
            if v == None:
                E=True
        except Exception as e:
            E=True
            error=str(e)

        if E == False:
            x_values.append(i)
            y_values.append(function(i))

            if scatter:
                plt.plot(x_values,y_values,c=color,linestyle=linestyle,linewidth=linewidth)
                plt.scatter(x_values,y_values,c=scatter_color,s=scatter_size)
            else:
                plt.plot(x_values,y_values,c=color,linestyle=linestyle,linewidth=linewidth)

            if verbose:
                print(i,function(i))
            if speed != 0:
                plt.pause(speed)

        else:
            if error_verbose:
                print("Error at " + str(i),error)

        i+= step

    plt.plot(x_values,y_values,c=color,linestyle=linestyle,linewidth=linewidth,label=function.__name__)
    
    if show:
        plt.legend()
        plt.show()

def poly_plot(functions,colors,min,max,lines_style=[],lines_width=[],scatters=[],scatters_colors=[],scatters_size=[],steps=[],distinct=False):
    if not lines_style:
        lines_style = np.full((1,len(functions)),"solid")
        lines_style = lines_style[0]
    else:
        c=0
        for i in lines_style:
            if i == "":
                lines_style[c] = "solid"
            else:
                c+=1
    if not lines_width:
        lines_width = np.full((1,len(functions)),1.5)
        lines_width = lines_width[0]
    else:
        c=0
        for i in lines_width:
            if i == "":
                lines_width[c] = 1.5
            else:
                c+=1
    if not scatters:
        scatters = np.full((1,len(functions)),0)
        scatters = scatters[0]
    
    if not steps:
        steps = np.full((1,len(functions)),0.1)
        steps = steps[0]

    if not scatters_colors:
        scatters_colors = np.full((1,len(functions)),"red")
        scatters_colors = scatters_colors[0]
    else:
        c=0
        for i in scatters_colors:
            if i == "":
                scatters_colors[c] = "red"
            else:
                c += 1     
    if not scatters_size:
        scatters_size = np.full((1,len(functions)),20)
        scatters_size = scatters_size[0]
    else:
        c = 0
        for i in scatters_size:
            if i == "":
                scatters_size[c] = 20
            else:
                c+=1

    if distinct:
        for i in range(len(functions)):
            if scatters[i] == 1:
                plot(functions[i],min,max,color=colors[i],linestyle=lines_style[i],linewidth=lines_width[i],scatter=True,scatter_color=scatters_colors[i],scatter_size=scatters_size[i],step=steps[i],show=False,fig=i+1)
                plt.legend()
            else:
                plot(functions[i],min,max,color=colors[i],linestyle=lines_style[i],linewidth=lines_width[i],step=steps[i],show=False,fig=i+1)
                plt.legend()                
        plt.show()
    else:
        for i in range(len(functions)):
            if scatters[i] == 1:
                plot(functions[i],min,max,color=colors[i],linestyle=lines_style[i],linewidth=lines_width[i],scatter=True,scatter_color=scatters_colors[i],scatter_size=scatters_size[i],step=steps[i],show=False)
                plt.legend()                 
            else:
                plot(functions[i],min,max,color=colors[i],linestyle=lines_style[i],linewidth=lines_width[i],step=steps[i],show=False)
                plt.legend() 
        plt.show()

def ord_mod(x, n):
    if m.gcd(x, n) != 1:
        return -1
    k = 1
    current = x % n
    while current != 1:
        current = (current * x) % n
        k += 1
        
    return k


def is_int(n):
    if int(n) == n:
        return 1
    else:
        return 0

def is_power(n,p):
    if is_int(n) == 1 and is_int(p) == 1:
        if int(n**(1/p)) == n**(1/p):
            return 1
        else:
            return 0
    else:
        raise ValueError("Input must be a positive integer.")
    
def is_sqrt(n):
    return n&(n-1)==0

def phi(n):
    if is_int(n) == 0 or n <= 0:
        raise ValueError("Input must be a positive integer.")
    else:    
        result = n 
        p = 2
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        if n > 1:
            result -= result // n
        return result

def mobius(n):
    if n == 1:
        return 1
    for k in range(2, int(n**0.5) + 1):
        if n % (k * k) == 0:
            return 0
    prime_count = 0
    num = n
    for i in range(2, n + 1):
        if num % i == 0:
            prime_count += 1
            while num % i == 0:
                num //= i
        if num == 1:
            break
    if prime_count % 2 == 0:
        return 1
    else:
        return -1

def f_n(f,n,x):
    for _ in range(n):
        x=f(x)
    return x

def prime_counting(n):
    return len(sieve_of_eratosthenes(n))

def mod_period(mod_n, func):
    i = 0
    r = []
    while True:
        r.append(func(i) % mod_n)
        i += 1
        if func(i) % mod_n in r:
            break
    return sorted(r)

def sym_mod(mod_n, func):
    half_mod = mod_n / 2
    symmetric_values = [v if v <= half_mod else v - mod_n for v in mod_period(mod_n,func)]
    principal_values = [v for v in symmetric_values if v >= 0]
    return sorted(principal_values)

r2d = lambda r: r * 180 / m.pi
d2r = lambda d: d * m.pi / 180

def decompose(n):
    if n == 0:
        return None
    else:
        def get_prime_factors(n):
            factors = {}
            while n % 2 == 0:
                if 2 in factors:
                    factors[2] += 1
                else:
                    factors[2] = 1
                n //= 2
            for i in range(3, int(n**0.5) + 1, 2):
                while n % i == 0:
                    if i in factors:
                        factors[i] += 1
                    else:
                        factors[i] = 1
                    n //= i
            if n > 2:
                factors[n] = 1
            return factors
        def format_decomposition(factors):
            terms = []
            for prime, exponent in sorted(factors.items()):
                if exponent > 1:
                    terms.append(f"{prime}^{exponent}")
                else:
                    terms.append(f"{prime}")
            return " * ".join(terms)
        
        factors = get_prime_factors(n)
        return format_decomposition(factors)

def decompose_matrix(n):
    if n == 1:
        return [1] 
    if n == 0:
        return []
    
    def get_prime_factors(n):
        factors = {}
        while n % 2 == 0:
            factors[2] = factors.get(2, 0) + 1
            n //= 2
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                factors[i] = factors.get(i, 0) + 1
                n //= i
        if n > 2:
            factors[n] = 1
        return factors
    
    factors = get_prime_factors(n)
    matrix = [[prime, exponent] for prime, exponent in sorted(factors.items())]
    
    return matrix

def reduce(n,p):
    if n%p==0:
        return n//(pow(p,val(p,n)))

def pD(x,p):
    return (val(p,x)*x)//p

def D(x):
    if x == 1 or x == 0:
        return 0
    if x < 0:
        return -D(-x)
    if Fraction(x).denominator != 1:
        a=Fraction(x).numerator
        b=Fraction(x).denominator
        return (D(a)*b-a*D(b))/(b**2)
    d=0
    for P in decompose_matrix(x):
        d+=pD(x,P[0])
    return d

def Newton_method(func,x0,seed):
    return f_n(lambda x_n: x_n - (float(sp.N(func(x_n))) / derive(func)(x_n)),seed,x0)


