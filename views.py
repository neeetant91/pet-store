from django.shortcuts import render,HttpResponse,redirect
from petapp.models import Petstore,Cart,Buy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout

from datetime import date
import random
import math

# Create your views here.
def test(request):
    return render(request,'test.html')
# this function will go through home page
def home(request):
    # # mai pagination kar rha hu so don't disturb me
    no_of_post=9
    page=request.GET.get('page')
    if page is None:
        page=1
    else:
        page=int(page)

    pets=Petstore.objects.all()
    length=len(pets)
    pets=pets[(page-1)*no_of_post:page*no_of_post]

    if page>1:
        prev=page-1
    else:
        prev=None
    if page<math.ceil(length/no_of_post):
        nxt=page+1
    else:
        nxt=None

    pet={
        'pet':pets,
        'prev':prev,
        'nxt':nxt
    }
    print('name is: ', request.session.get('username'),'and id is; ',request.session.get('user_id'))
    return render(request,'home.html',pet)

# this is sign up function
def sign_up(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        cpassword=request.POST.get('Cpassword')
        if password==cpassword:

            myuser=User.objects.create_user(username,email,password)
            # myuser.is_staff=True
            myuser.save()
            myuser=authenticate(username=username,password=password)
            login(request,myuser)
            return redirect('/')
        else:
            messages.warning(request,'Password not match')
            return redirect('/signup')
    return render(request,'signup.html')
# this is sign up function
def log_in(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            request.session['user_id']=user.id
            request.session['username']=user.username
            login(request,user)
            return redirect('/')
        else:
            messages.warning(request,'Credential did not match..')
            return redirect("/login")
    return render(request,'login.html')

# this function is for log out
def log_out(request):
    # del request.session['user_id']
    logout(request)
    # messages.success('')
    return redirect('/')
# this page will go ate about page
def about(request,id):
    pet={
        'id':Petstore.objects.get(id=id).id,
        'name':Petstore.objects.get(id=id).name,
        'line':Petstore.objects.get(id=id).line,
        'price':Petstore.objects.get(id=id).price,
        'desc':Petstore.objects.get(id=id).desc,
        'img1':Petstore.objects.get(id=id).img1,
        'img2':Petstore.objects.get(id=id).img2,
        'img3':Petstore.objects.get(id=id).img3
        }
    return render(request,'about.html',pet)

# this function will add pets
def addpet(request):
    if request.method=="POST":
        name=request.POST.get('name')
        line=request.POST.get('line')
        price= random.randint(50,500)
        category=request.POST.get('category')
        desc=request.POST.get('desc')
        img1=request.POST.get('img1')
        img2=request.POST.get('img2')
        img3=request.POST.get('img3')
        pet= Petstore(name=name,line=line,category=category,price=price,desc=desc,img1=img1,img2=img2,img3=img3)
        pet.save()
    return render(request,'addpet.html')


# this function will search the query as user enter the search box
def search(request):
    pet=request.GET['query']
    if pet=='':
        return redirect('/')
    else:
        search={
            'pet':Petstore.objects.filter(category__icontains=pet)|Petstore.objects.filter(name__icontains=pet) | Petstore.objects.filter(line__icontains=pet)|Petstore.objects.filter(desc__icontains=pet)
        }
        return render(request,'search.html',search)
    # return HttpResponse('this is django search')

# this function is for sort the result according to name..
def orderByName(request):
    pet={
        'pet':Petstore.objects.all().order_by('name')
    }
    return render(request,'search.html',pet)
def orderByPrice(request):

    pet={
        'pet':Petstore.objects.all().order_by('price')
    }
    return render(request,'search.html',pet)


# this is cart function
def cart(request,id):

        if request.user.is_active:
            # return HttpResponse('yes the user is active and logged in')
            pet_id=Petstore.objects.get(id=id).id
            name=Petstore.objects.get(id=id).name
            line=Petstore.objects.get(id=id).line
            # 'desc':Petstore.objects.get(id=id).desc,
            img1=Petstore.objects.get(id=id).img1
            # 'img2':Petstore.objects.get(id=id).img2,
            # 'img3':Petstore.objects.get(id=id).img3
            dates=date.today()
            user_id=request.session['user_id']
            cart=Cart(pet_id=pet_id,name=name,line=line,img1=img1,date=dates,user_id=user_id)
            cart.save()
            #--------------- yha mai msg show karwaungaaaa -------------------
            messages.success(request,'Your Pet has been added to carts. Please check Cart..!')
            # ----------------------------------------------------------------
            # return redirect(f'/cartItem')
            return redirect(f'/about/{id}')
        else:
            return redirect('/login')
            # return HttpResponse('no, first you have to loggin')

# this function will the cartItems in the templates....
def cartItem(request):
    if request.user.is_authenticated:
        carts={
            'items':Cart.objects.filter(user_id=request.session['user_id'])
            # 'items':Cart.objects.all()
        }
        return render(request,'cart.html',carts)
    else:
        return redirect("/login")

# this function will delete the carts items from the cart html------
def deleteCart(request,id):
    if request.user.is_active:
        Cart.objects.filter(id=id).delete()
        messages.warning(request,'Your Item has been Removed successfully..!')
        return redirect('/cartItem')
    else:
        return redirect('/login')

# this is Buy function
def buyCart(request,pet_id):
    if request.user.is_active:
        # pet_id=Cart.objects.get(id=id).pet_id
        name=Cart.objects.get(pet_id=pet_id).name
        line=Cart.objects.get(pet_id=pet_id).line
        # 'desc':Petstore.objects.get(id=id).desc,
        img1=Cart.objects.get(pet_id=pet_id).img1
        # 'img2':Petstore.objects.get(id=id).img2,
        # 'img3':Petstore.objects.get(id=id).img3
        user_id=request.session['user_id']
        dates=date.today()
        cart=Buy(pet_id=pet_id,name=name,line=line,img1=img1,date=dates,user_id=user_id)
        cart.save()
        Cart.objects.filter(pet_id=pet_id).delete()
        #--------------- yha mai msg show karwaungaaaa -------------------
        messages.success(request,'Yeahhh, Your Order has been Placed..! ')

        # ----------------------------------------------------------------
        # return redirect('/yourOrder')
        return redirect('/cartItem')
    else:
        return redirect('/login')
# this is Buy function
def buy(request,id):
        if request.user.is_active:
            # return HttpResponse('yes the user is active and logged in')
            pet_id=Petstore.objects.get(id=id).id
            name=Petstore.objects.get(id=id).name
            line=Petstore.objects.get(id=id).line
            # 'desc':Petstore.objects.get(id=id).desc,
            img1=Petstore.objects.get(id=id).img1
            # 'img2':Petstore.objects.get(id=id).img2,
            # 'img3':Petstore.objects.get(id=id).img3
            user_id=request.session['user_id']
            dates=date.today()
            cart=Buy(pet_id=pet_id,name=name,line=line,img1=img1,date=dates,user_id=user_id)
            cart.save()
            #--------------- yha mai msg show karwaungaaaa -------------------
            messages.success(request,'Congrates, Your Order has been Placed Successfully ! ')

            # ----------------------------------------------------------------
            # return redirect('/yourOrder')
            return redirect(f'/about/{id}')
        else:
            return redirect('/login')
            # return HttpResponse('no, first you have to loggin')

# this is show for payment
def payment(request,pet_id):
    details={
        'name':Petstore.objects.get(id=pet_id).name,
        'price':Petstore.objects.get(id=pet_id).price,
        'img':Petstore.objects.get(id=pet_id).img1,
        'pet_id':Petstore.objects.get(id=pet_id).id

        }


    return render(request,'paypal.html',details)

# this function will the Ordersss in the templates....
def yourOrder(request):
    if request.user.is_active:
        order={
            'orders':Buy.objects.filter(user_id=request.session['user_id'])
        }
        return render(request,'buy.html',order)
    else:
        return redirect('/login')

# this function will delete oreder itmes from buy templates
def deleteOrder(request,id):
    if request.user.is_active:
        Buy.objects.filter(id=id).delete()
        messages.warning(request,'Congrates, You Successfully cancelled Your order..')
        return redirect('/yourOrder')
    else:
        return redirect('/login')


# these are pet search functions
def dog(request):
    dog="dog"
    search={
        'pet':Petstore.objects.filter(category=dog)
    }
    return render(request,'search.html',search)

def cat(request):
    cat="cat"
    search={
        'pet':Petstore.objects.filter(category=cat)
    }
    return render(request,'search.html',search)

def snake(request):
    pet="snake"
    search={
        'pet':Petstore.objects.filter(category=pet)
    }
    return render(request,'search.html',search)

def bird(request):
    pet="bird"
    search={
        'pet':Petstore.objects.filter(category=pet)
    }
    return render(request,'search.html',search)

def lizard(request):
    pet="lizard"
    search={
        'pet':Petstore.objects.filter(category=pet)
    }
    return render(request,'search.html',search)

def cow(request):
    pet="cow"
    search={
        'pet':Petstore.objects.filter(category=pet)
    }
    return render(request,'search.html',search)

def cock(request):
    pet="cock"
    search={
        'pet':Petstore.objects.filter(category=pet)
    }
    return render(request,'search.html',search)

def goat(request):
    pet="goat"
    search={
        'pet':Petstore.objects.filter(category=pet)
    }
    return render(request,'search.html',search)

def buffalo(request):
    pet="buffalo"
    search={
        'pet':Petstore.objects.filter(category=pet)
    }
    return render(request,'search.html',search)

def wolf(request):
    pet="wolf"
    search={
        'pet':Petstore.objects.filter(category=pet)
    }
    return render(request,'search.html',search)

def bear(request):
    pet="bear"
    search={
        'pet':Petstore.objects.filter(category=pet)
    }
    return render(request,'search.html',search)
# -----------------------------------------------------------------------------------------
# i want to create a function that can search category from only one function

# def cate(self,request):
#     category=request.data.get('select')
#     # category=request.DATA['select']
#     pet=Petstore.objects.filter(category=category)
#     # pet=Petstore.objects.get(id=id).category
#     search={
#         # 'pet':Petstore.objects.filter(category=pet)
#         'pet':pet
#     }
#     return render(request,'category.html',search)

# -----------------------------------------------------------------------------------------
