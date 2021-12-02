from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django import forms
from django.http import JsonResponse
from .models import User , NewPost , Follow


class NewPostForm(forms.ModelForm):
    newpost = forms.CharField(label='New Post' , widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 40 , 'rows':3 }))
    
    
    class Meta:
        model = NewPost
        
        fields =['newpost',
                 
                  ]


def index(request):
    if not request.user.is_authenticated:
        #messages.error(request , "You must login to use this Social Network "  )  
        return render(request, 'network/login.html' ) 
    else:    
        user =  User.objects.get(username=request.user.username)
        user0 = user.username
        userx = User.objects.all()
        if request.method=="POST":
            if int(request.POST["postid"])>0:
                 postid = request.POST["postid"]
                 content =request.POST["newpost"]

                 blog = NewPost.objects.filter(id=postid)
                 blog.update(newpost=content)
                 return HttpResponseRedirect(reverse("index"))

            newpost = request.POST["newpost"]
            author_id = user.id
            newpost0 = NewPost.objects.create(newpost=newpost,author_id=author_id)
            newpost0.save

           
            resultpost= NewPost.objects.all().order_by('-created_date')
               
            page = request.GET.get('page', 1)

            paginator = Paginator(resultpost, 10)
            try:
                p = paginator.page(page)
            except PageNotAnInteger:
                p = paginator.page(1)
            except EmptyPage:
                p = paginator.page(paginator.num_pages)

                
            return render(request, "network/index.html" , {'resultpost':resultpost , 'userx':userx ,'p':p }) 
        else:
               
            resultpost= NewPost.objects.all().order_by('-created_date')
               
            page = request.GET.get('page', 1)

            paginator = Paginator(resultpost, 10)
            try:
                p = paginator.page(page)
            except PageNotAnInteger:
                p = paginator.page(1)
            except EmptyPage:
                p = paginator.page(paginator.num_pages)


            #messages.error(request , "Sorry you entered invalid Entries"  )
            return render(request, "network/index.html" , {'resultpost':resultpost ,'userx':userx ,'p':p }) 

def test(request):
    
    pass    
    return render(request,"network/test.html")
     
    
@csrf_exempt

@login_required
def editpost(request,id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")
        if content:
            blog = NewPost.objects.filter(id=id)
            blog.update(newpost=content)
            print(content)
            return JsonResponse({"message": "successfully updated"},
                                status=201)

        return JsonResponse({"message": "not_updated"},
                            status=201)

    if request.user.username == user:
        return JsonResponse({"message": "ok"}, status=201)
    return JsonResponse({"message": "not_ok"},
                        status=201)



            
def profile(request,id):
    user0= User.objects.get(id=id)
    unfollow1 = 0
    unfollow0 = 0
    if user0.follow_status == True:
        unfollow1 =1
    else:
        unfollow0 = 1 

    post0 = NewPost.objects.filter(author_id = id).order_by('-created_date')   
    userx = User.objects.all()
    f=Follow.objects.filter(follow=id)
    

    return render(request, "network/profile.html" , {'user0':user0 , 'unfollow1':unfollow1 , 'unfollow0':unfollow0 , 'post0':post0 , 'userx':userx , 'f':f })

@login_required
def follow(request,id):
    user0= User.objects.get(id=id)
    if Follow.objects.filter(follow_id=request.user.id):
        f =Follow.objects.get(follow_id = request.user.id)
        f.following.add(user0.id)
        f.save() 
        user0.following_no = user0.following_no + 1
        user0.follow_status = True
        user0.save(update_fields=['following_no','follow_status'])

        unfollow1 = 1
        messages.info(request , "You have successfully followed"  )

    else:
        Follow.objects.create(follow_id = request.user.id)
        f =Follow.objects.get(follow_id = request.user.id)
        f.following.add(user0.id)
        f.save()
        user0.following_no = user0.following_no + 1
        user0.follow_status = True
        user0.save(update_fields=['following_no','follow_status'])

        unfollow1 = 1
        messages.info(request , "You have successfully followed"  )

  

    
    user1 = User.objects.get(id = request.user.id)
    if Follow.objects.filter(follow_id = id):
        f =Follow.objects.get(follow_id = id)
        f.follower.add(request.user)
        f.save() 
        user1.follower_no = user1.follower_no + 1
        user1.save(update_fields=['follower_no'])

        unfollow1 = 1
        #return render(request, 'network/profile.html' , {'user0':user0 , 'unfollow1':unfollow1 })


    else:
        Follow.objects.create(follow_id = id)
        f =Follow.objects.get(follow_id = id)
        f.follower.add(request.user)
        f.save()
        user1.follower_no = user1.follower_no + 1
        user1.save(update_fields=['follower_no'])

        unfollow1 = 1
        #return render(request, 'network/profile.html' , {'user0':user0 , 'unfollow1':unfollow1 })

  

    

    #unfollow1 = 1
    return HttpResponseRedirect(reverse("index"))

    #return render(request, 'network/profile.html' , {'user0':user0 , 'unfollow1':unfollow1 })
@login_required
def following(request):
    if not request.user.is_authenticated:
        messages.error(request , "You must login to view followings "  )  
        return render(request, 'network/login.html' ) 
    else:    
        user =  User.objects.get(username=request.user.username)
        user0 = user.username
        userx = User.objects.all() 
        if Follow.objects.filter(follow=request.user):

            fl = Follow.objects.get(follow=request.user).following.all()
            resultpost = NewPost.objects.filter(author__in=fl).order_by('-created_date')
            if len(resultpost)==0:
                messages.error(request , "Sorry you are not following anyone"  )
            page = request.GET.get('page', 1)

            paginator = Paginator(resultpost, 10)
            try:
                p = paginator.page(page)
            except PageNotAnInteger:
                p = paginator.page(1)
            except EmptyPage:
                p = paginator.page(paginator.num_pages)

        else:
            messages.error(request , "Sorry you are not following anyone"  )
            return render(request,"network/following.html",{ 'userx':userx })
        return render(request, "network/following.html" , {'resultpost':resultpost ,'userx':userx ,'p':p }) 




@login_required
def unfollow(request,id): 
    user0= User.objects.get(id=id)
    if Follow.objects.filter(follow_id=request.user.id):
        f =Follow.objects.get(follow_id = request.user.id)
        f.following.remove(user0.id)
        f.save() 
        user0.following_no = user0.following_no - 1
        user0.follow_status = False
        
        user0.save(update_fields=['following_no','follow_status'])
        messages.info(request , "You have successfully unfollowed"  )

    else:
        Follow.objects.create(follow_id = request.user.id)
        f =Follow.objects.get(follow_id = request.user.id)
        f.following.remove(user0.id)
        f.save()
        user0.following_no = user0.following_no - 1
        user0.follow_status = False
        #user0.follow_status = False
        user0.save(update_fields=['following_no','follow_status'])
        messages.info(request , "You have successfully unfollowed"  )


    user1 = User.objects.get(id = request.user.id)
    if Follow.objects.filter(follow_id = id):
        f =Follow.objects.get(follow_id = id)
        f.follower.remove(request.user)
        f.save()
        user1.follower_no = user1.follower_no - 1
        user1.save(update_fields=['follower_no'] )
    else:
        Follow.objects.create(follow_id = id)
        f =Follow.objects.get(follow_id = id)
        f.follower.remove(request.user)
        f.save()
        user1.follower_no = user1.follower_no - 1
        user1.save(update_fields=['follower_no'])
        
        
      
    unfollow0= 1
    #return render(request, 'network/profile.html' , {'user0':user0 , 'unfollow0':unfollow0 })
    return HttpResponseRedirect(reverse("index"))
    

def likesadd(request,id):
    post0 = NewPost.objects.get(id = id)
    post1 = post0.liked.all()
    
    if request.user in post1:

        post0.likes = post0.likes -1
        post0.liked.remove(request.user)
        post0.save()
        liketest = 'False' 
    else:
        post0.likes = post0.likes +1
        post0.liked.add(request.user)
        post0.save()
        liketest  = 'True'

    return JsonResponse({'likes': post0.likes , 'liketest': liketest })



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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html") 

