from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render  , get_object_or_404
from django.urls import reverse
from django import forms
from datetime import timedelta ,datetime ,date
from django.contrib.auth.decorators import login_required

from .models import User , Category ,List ,Comment ,Whistlistx ,Bid
class DateInput(forms.DateInput):
    input_type = 'date'


class CreateListForm(forms.ModelForm):
    image = forms.ImageField(required = False)
    user = forms.CharField(label='user', max_length=256, widget=forms.HiddenInput(), required = False)
    bidder = forms.CharField(label='bidder', max_length=256, widget=forms.HiddenInput() ,required = False)
    p_slug = forms.CharField(label='slug', max_length=256, widget=forms.HiddenInput() , required = False)
    class Meta:
        model = List
        start_time= forms.DateField(widget=DateInput())

        fields =['p_name',
                  'image',
                  'p_description',
                  'bid',
                  'p_period',
                  'category',
                  'start_time'
                  ]

        widgets = {
            'start_time': DateInput()
        }

        labels = {
            'p_name': 'Name' ,'p_description':'Description' , 'p_period':'Period'
        }

       

        exclude ={'close' , 'status' }
        

space =""    

def index(request):
    list0 = List.objects.all()
    list00 = list0.filter(status=True)
    list1 = list00.filter(close=False)
    bid0=Bid.objects.all()
    comment = Comment.objects.all()
    nw1 = datetime.now()
    #nw = datetime.strptime(nw1, '%m/%d/%y %H:%M:%S')
    # myDate.strftime("%Y-%m-%d %H:%M:%S")
    nw2 = nw1.strftime("%Y-%m-%d %H:%M:%S %p")

   # "M d, Y g:ma
    for li in list1:
        end0=li.end_time
        end1=end0.strftime("%Y-%m-%d %H:%M:%S %p")
        if(end1 < nw2):
            li.close = True
            li.save(update_fields=['close'])
            messages.success(request,li.close)

    
    
    return render(request, 'auctions/index.html' , {'product':list1 ,'comment':comment  , 'bid0':bid0 })

def category_single(request , id):
    category_id = Category.objects.get(id=id)
    list0 = List.objects.all()
    list01=list0.filter(category_id=category_id.id)
    list10 =list01.filter(status=True)
    cat0 = Category.objects.all()
    cat1 =cat0.filter(id = id)
    bid0 = Bid.objects.all()

    list1 = list10.filter(close=False)
    comment = Comment.objects.all()
    nw1 = datetime.now()
    nw2 = nw1.strftime("%Y-%m-%d %H:%M:%S %p")

   # "M d, Y g:ma
    for li in list1:
        end0=li.end_time
        end1=end0.strftime("%Y-%m-%d %H:%M:%S %p")
        if(end1 < nw2):
            li.close = True
            li.save(update_fields=['close'])
            
    if list1 :
        return render(request, 'auctions/index.html' , {'product':list1 , 'title':cat1 , 'comment':comment , 'bid0':bid0  })
        # , 'category':Category.objects.filter(id=id , name)})
    return render(request, 'auctions/nocategory.html' )


    

def closing_list(request, id):
    closelist0=List.objects.get(id=id)
    closelist0.close = True

    
    closelist0.save(update_fields=['close'])
    list1 = List.objects.all()
    comment = Comment.objects.all()

    messages.success(request , " You have just manually closed your submitted Listing "  )
    return HttpResponseRedirect(reverse('index' ))
    #return render(request, 'auctions/index.html' , {'product':list1 ,'comment':comment })

def create(request):
    if not request.user.is_authenticated:
        messages.error(request , "You must login to Create a listing "  )  
        return render(request, 'auctions/create.html' ) 
    else:    
        user =  User.objects.get(username=request.user.username)
        user0 = user.username
        if request.method=="POST":
            form=CreateListForm(request.POST or None, request.FILES  or None, )
            if form.is_valid():

                list0 = form.save(commit=False)

                list0.user = request.user
                list0.bidder = request.user
                list0.p_slug =form.cleaned_data["p_name"]               
                period =form.cleaned_data["p_period"]
               
                list0.save()
                list0.end_time=list0.start_time + timedelta(days=period)
                
                list0.save(update_fields=['end_time'])
                messages.success(request,"Listing Added Successfully")        
                        
                return HttpResponseRedirect(reverse("index"))
            
            else:
                return render(request, "auctions/create.html" ,{ 
                    "form":form
                })

        return render(request, "auctions/create.html" , { 
            "form":CreateListForm() , 'user0':user0 
        })

def view(request , id  , us_id):
    if not request.user.is_authenticated:
        messages.error(request , "You must login to View Contact ,  Plus you have to be the one who created the listing "  )  
        win0=Bid.objects.all()
        list0 = List.objects.filter(close=True)
        user = User.objects.all()
        return render(request, "auctions/winners.html" ,{ 'list0':list0 ,  'win0': win0  , 'user1':user} )
   
    
    
    
    else:
        
        userbid = User.objects.get(id= us_id)
        user = User.objects.get(id= request.user.id)
        bidlist = id

        #bid0 = Bid.objects.get(user_id = us_id)
        #bid0 = bid00.filter(listing_id=id)
        if user == userbid:
            user = User.objects.get(id =us_id )
            list0 = List.objects.filter(id=id)
            print(id,us_id)
            
            return render(request, "auctions/view.html" ,{ 'list0':list0 ,  'bidlist': bidlist , 'user1':user} )
        else: 
            messages.error(request,"Sorry  you have can't view contact because ,you are not the one who posted this listing ")
            win0=Bid.objects.all()
            list0 = List.objects.filter(close=True)
            user = User.objects.all()
            return render(request, "auctions/winners.html" ,{ 'list0':list0 ,  'win0': win0  , 'user1':user} )

   
    



def winners(request):
    list00 = List.objects.all()
    win0=Bid.objects.all()
    list0 = list00.filter(close=True)
    user = User.objects.all()

    return render(request, "auctions/winners.html" ,{ 'list0':list0 ,  'win0': win0  , 'user1':user} )





def whishlistadd(request,id):
    
    list0=List.objects.get(id=id)
    
    if request.user.is_authenticated:
        user = User.objects.get(username= request.user.username)

        whishlist00 = Whistlistx.objects.filter(user=user.id)
        whishlist0= whishlist00.filter(wlistings=list0.id)
        if whishlist0:
            messages.info(request,"You can't add "+ list0.p_name + " to your watchlist, because you have added it already")
            return HttpResponseRedirect(reverse('index' ))
        else:
            
            # same as below whish =  Whistlistx.objects.create(user=user, wlistings=list0)
            whish =  Whistlistx.objects.create(user_id=user.id, wlistings_id=list0.id)
            whishlist00 = Whistlistx.objects.filter(user=user.id)
            
            list0=List.objects.all()
            
            #return render(request, 'auctions/whishlist.html' , {'whish': whishlist0 , 'list0':list0 } )
            messages.info(request,"You successfully added to your watchlist . Click on watchlist on menu")
            return HttpResponseRedirect(reverse('index' ))

    messages.error(request,"You must login add to whishlist ")    
    return HttpResponseRedirect(reverse('index' ))


@login_required
def whishlist(request,id):
    user= User.objects.get(id=id)
    whishlist00 = Whistlistx.objects.filter(user = user.id )
    bid0= Bid.objects.all()
    
    list0= List.objects.filter(close = False)

    if whishlist00:
        pass
    else:    
        messages.success(request,"Sorry You dont have anything yet on your whishlist. You add on the active listing page")
    
    
    
    
    
    return render(request, 'auctions/whishlist.html' , {'whish': whishlist00  , 'list0':list0 , 'bid0':bid0 } )


def remove(request,id):
    
    whishlist000 = Whistlistx.objects.get( wlistings_id = id  ,user =  request.user  )
    whishlist00 =  whishlist000.delete()

    list0= List.objects.all()
    bid0= Bid.objects.all()
    
    
    if whishlist00:
             
        messages.success(request,"You have successfully deleted from your watchlist")
        whishlist00 = Whistlistx.objects.filter(user = request.user)
        list0= List.objects.filter(close = False)
       
    
        return render(request, 'auctions/whishlist.html' , {'whish': whishlist00  , 'list0':list0 , 'bid0':bid0 } )

    messages.success(request,"Sorry file not deleted")
    whishlist000 = Whistlistx.objects.get( user = request.user )
    list0 = List.objects.filter(close = False)
    
    return render(request, 'auctions/whishlist.html' , {'whish': whishlist00  , 'list0':list0 , 'bid0':bid0 } )





def list_single(request , id):
    list0 = List.objects.get(id=id)
    bid0=Bid.objects.filter( listing_id = list0.id)
    if bid0:
        bid0 = Bid.objects.get(listing_id = list0.id)
    else:
        pass    
        
    userlist = list0.user
    if list0: 
        com = Comment.objects.all()
        comment = com.filter(listing=list0)
        comment0 = comment.filter(user=userlist)
        if request.user.is_authenticated:
            
            user =  User.objects.get(username=request.user.username)
            user0 = user.username 
            if list0.close == True:
                    if bid0.user_id == user.id:
                        messages.success(request,"Congradulations!!! You won the bid")


                    else:
                        pass 

            if request.user == list0.user:

                userlist1 = 1

                return render(request, 'auctions/listsingle.html' , {'list':list0 ,'comment':comment0 , 'userlist':userlist ,'userlist1':userlist1  , 'bid0':bid0  })
        

           
        return render(request, 'auctions/listsingle.html' , {'list':list0 ,'comment':comment0 , 'userlist':userlist , 'bid0':bid0 })
    else:
        list0 = List.objects.all()
        list1 = list0.filter(status=True)
        

        return render(request, 'auctions/index.html' , {'product':list1  , 'bid0':bid0 })


def login_view(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def categories(request):
    return {'categories': Category.objects.all()
    }



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def submitbid(request , id):
    if request.method == "POST":
        
        # Attempt to sign user in
        bid = float(request.POST["bid"])
        msgtop = "-----------------------------"
             
                
        list0 = List.objects.get(id = id)
        if request.user.is_authenticated:
            bid00 = Bid.objects.filter(listing_id =id)
            #update bidding
            if bid00:
                bid0 = Bid.objects.get(listing_id =id)
           
                if bid > bid0.price:
                    bid0.price = bid
                    bid0.user= request.user
                    bid0.save(update_fields=['price' , 'user' ])
                    bid0 = Bid.objects.get(listing_id =id)
                    list0.bid =bid
                    list0.save(update_fields=['bid'])
                
                


                    return render(request, 'auctions/listsingle.html' , {'list':list0  , 'bid0':bid0  })

                msg = "**Value"
                msg1="must"
                msg2 ="greater"
                msg3 = "than"
                msg4= "Bid***"
                messages.error(request, "Please enter a  value greater than Bid" )
                return render(request, 'auctions/listsingle.html' , {'list':list0  , 'bid0':bid0 , 'msgtop':msgtop , 'msg':msg , 'msg1':msg1 ,'msg2':msg2 , 'msg3':msg3 , 'msg4':msg4 ,'sapce':space  })
            
            else:
                #create biding


                if bid > list0.bid:
                    bid00 = Bid.objects.create(price=bid ,listing_id = id , user = request.user )
                    bid0 = Bid.objects.get(listing_id = id , user = request.user)           
                

                    return render(request, 'auctions/listsingle.html' , {'list':list0  , 'bid0':bid0  })

                 
                msg = "**Value"
                msg1="must"
                msg2 ="greater"
                msg3 = "than"
                msg4= "Bid***"
                messages.error(request, "Please enter a  value greater than Bid" )
                return render(request, 'auctions/listsingle.html' , {'list':list0  , 'msgtop':msgtop , 'msg':msg , 'msg1':msg1 ,'msg2':msg2 , 'msg3':msg3 , 'msg4':msg4 ,'sapce':space  })


        msg = "**login_to_Bid**"
        messages.error(request,"You must login 1st to Bid ")          
        return render(request, 'auctions/listsingle.html' , {'list':list0  ,'msgtop':msgtop , 'msg':msg , 'sapce':space })    


        
def comment(request,id):

    list0 = List.objects.get(id=id)
    if request.method=="POST":
        comment = request.POST["comment"]
        msgtop = "--------------------------"
        
        if request.user.is_authenticated:
            user =  User.objects.get(username=request.user.username)        
            
            comments = Comment(body=comment , user= user ,listing= list0)
            if comments:
                comments.save()
                messages.success(request , " Thank you.  Your Comment has been recorded  Successfully "  )
                msg = "Comment"
                msg1 = "saved"
                return render(request, 'auctions/listsingle.html' , {'list':list0 , 'msgtopc':msgtop , 'msgc1':msg , 'msg1c1':msg1 })
            
            msg = "Comment_not_Submited"
            messages.error(request ,"Comment not Submited"    )  
            return render(request, 'auctions/listsingle.html' , {'list':list0 , 'msgc':msg ,'msgtopc':msgtop } )
        
        msg = "You"
        msg1 ="must"
        msg2 ="login"
        msg3 = "first."
        messages.error(request , "You must login to Comment"  )  
        return render(request, 'auctions/listsingle.html' , {'list':list0 , 'msgc':msg , 'msg1c':msg1  , 'msg2c':msg2 , 'msg3c':msg3 , 'msgtopc':msgtop } )   

    return render(request, 'auctions/listsingle.html' , {'list':list0 })
            



            

