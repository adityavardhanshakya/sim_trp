import math, json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
def f(x):
    return 1/(1 + x**2)

# Implementing trapezoidal method
def trapezoidal(x0,xn,n):
    h = (xn - x0) / n
    kl = []
    inte = []
    # Finding sum 
    integration = f(x0) + f(xn)
    
    for i in range(1,n):
        k = x0 + i*h
        kl.append(k)
        integration = integration + 2 * f(k)
        inte.append(integration)
    
    # Finding final integration value
    integration = integration * h/2
    
    return integration,kl,inte
    

def func( x ):
	return math.log(x)

# Function for approximate integral
def simpsons( ll, ul, n ):

	# Calculating the value of h
	h = ( ul - ll )/n

	# List for storing value of x and f(x)
	x = list()
	fx = list()
	
	# Calculating values of x and f(x)
	i = 0
	while i<= n:
		x.append(ll + i * h)
		fx.append(func(x[i]))
		i += 1

	# Calculating result
	res = 0
	i = 0
	while i<= n:
		if i == 0 or i == n:
			res+= fx[i]
		elif i % 2 != 0:
			res+= 4 * fx[i]
		else:
			res+= 2 * fx[i]
		i+= 1
	res = res * (h / 3)
	return res,x,fx
	

def index(request):
    return render(request,'index.html') 

@csrf_exempt
def solution(request):
    lower = float(request.POST.get('lower'))
    upper = float(request.POST.get('upper'))
    interval = int(request.POST.get('interval'))
    trap,tkl,tintegration = trapezoidal(lower, upper, interval)
    simp,skl,sintegration = simpsons(lower, upper, interval)
    return JsonResponse(json.dumps({
		"trap":{
			"val":trap,
			"x":tkl,
			"int":tintegration
        },
		"simp":{
			"val":simp,
			"x":skl,
			"int":sintegration
        }
    }),safe=False)