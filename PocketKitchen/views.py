from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .forms import *
from django.views.generic import TemplateView,FormView,CreateView,ListView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from .models import *
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,'Please Login First')
            return redirect('login')
    return inner

decorators=[never_cache,signin_required]

class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self,request):
        formdata=LoginForm(data=request.POST)
        if formdata.is_valid():
            usnm=formdata.cleaned_data.get("username")
            pswd=formdata.cleaned_data.get("password")
            user=authenticate(request,username=usnm,password=pswd)
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Login Failed!!...Invalid Username/Password")
                return redirect('login')
        return render(request,"login.html",{"form":formdata})

class SignupView(CreateView):
    template_name="signup.html"
    form_class=SignupForm
    success_url=reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request,'User Registration Completed')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,'Registration Failed!!')
        return super().form_invalid(form)
    
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('login')
    
# ------------------------------------------------------------------------------------------------------------------------------------ 
class IndexView(TemplateView):
    template_name="index.html"

class ExploreRecipe(TemplateView):
    template_name='recipeexplore.html'

@method_decorator(decorator=decorators,name='dispatch')
class HomeView(TemplateView):
    template_name='home.html'

decorators
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST,request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False) 
            recipe.user = request.user 
            recipe.save()  
            messages.success(request,'Your Recipe is Posted')
            return redirect('mypost')  
    else:
        form = RecipeForm()
    return render(request, 'addrecipe.html', {'form': form})

decorators
def upload_video(request):
    if request.method == 'POST':
        form = RecipeVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Your Video is Uploaded')
            return redirect('viewvideo')
    else:
        form = RecipeVideoForm()
    return render(request, 'uploadvideo.html', {'form': form})


@method_decorator(decorator=decorators,name='dispatch')
class MyPostView(TemplateView):
    template_name='mypost.html'

@method_decorator(decorator=decorators,name='dispatch')
class PostView(ListView):
    template_name="mypost.html"
    queryset=Recipe.objects.all()
    context_object_name="data"
    def get_queryset(self):
        qs=self.queryset.filter(user=self.request.user)
        return qs

@method_decorator(decorator=decorators,name='dispatch')
class AllPostView(ListView):
    template_name="viewpost.html"
    queryset=Recipe.objects.all().order_by('-created_at')
    context_object_name="data"

@method_decorator(decorator=decorators,name='dispatch')
class RecipeListView(ListView):
    template_name="recipelist.html"
    queryset=Recipe.objects.all()
    context_object_name='recipe'
    def get_queryset(self):
       cat=self.kwargs.get('cat')
       self.request.session['category']=cat
       return self.queryset.filter(category=cat)

decorators
def searchproduct(request,*args,**kwargs):
    keyword=request.POST['searchkey']
    cat=request.session['category']
    if keyword:
        recipe=Recipe.objects.filter(name__icontains=keyword,category=cat)
        return render(request,'recipelist.html',{"recipe":recipe})
    else:
       return redirect('recipelist',cat=cat)

decorators
class VideoView(ListView):
    template_name='viewvideos.html'
    queryset=RecipeVideo.objects.all()
    context_object_name='videos'
    # def get_queryset(self):
    #     qs=self.queryset.filter(user=self.request.user)
    #     return qs

@method_decorator(decorator=decorators,name='dispatch')
class RecipeDetailView(DetailView):
    template_name='recipedetail.html'
    queryset=Recipe.objects.all()
    context_object_name='recipe'
    pk_url_kwarg='id'

@method_decorator(decorator=decorators,name='dispatch')
class EditRecipeView(View):
    def get(self,request,**kwargs):
        rid=kwargs.get('id')
        recipe=Recipe.objects.get(id=rid)
        form=RecipeForm(instance=recipe)
        return render(request,'editrecipe.html',{"form":form})
    def post(self,request,**kwargs):
        rid=kwargs.get('id')
        recipe=Recipe.objects.get(id=rid)
        formdata=RecipeForm(data=request.POST,files=request.FILES,instance=recipe)
        if formdata.is_valid():
            formdata.save()
            messages.success(request,"Updated Successfully")
            return redirect('mypost')
        messages.error(request,"Checking")
        return render(request,'editrecipe.html',{"form":formdata})

@method_decorator(decorator=decorators,name='dispatch')
class DeleteRecipeView(View):
    def get(self,request,*args,**kwargs):
        sid=kwargs.get('id')
        print('tid')
        task=Recipe.objects.get(id=sid)
        task.delete()
        messages.success(request,"Deleted Successfully")
        return redirect('mypost')

decorators   
def like_recipe(request, recipe_id):
    # Attempt to retrieve the post using filter
    recipe = Recipe.objects.filter(id=recipe_id).first()

    if not recipe:
        # If no post is found, raise an Http404 or redirect to another page
        raise Http404("Post not found")

    if request.user in recipe.likes.all():
        recipe.likes.remove(request.user)  # Unlike
        messages.info(request, f"You unliked '{recipe.name}'.")
    else:
        recipe.likes.add(request.user)  # Like
        messages.success(request, f"You liked '{recipe.name}'.")

    return redirect('recipedetail', id=recipe.id)  # Redirect to the post detail page



decorators
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted!')
            return redirect('home')  # Redirect to your home page or any other page
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

decorators
@login_required
def add_comment(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()


    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None

        Comment.objects.create(recipe=recipe, user=request.user, content=content, parent=parent_comment)
        return redirect('manage_comments', recipe_id=recipe.id)

    comments = Comment.objects.filter(recipe=recipe).order_by('-date')
    return render(request, 'comment.html', {'recipe': recipe, 'comments': comments})

decorators
@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.filter(id=comment_id, user=request.user).first()

    recipe_id = comment.recipe.id
    comment.delete()
    return redirect('manage_comments', recipe_id=recipe_id)

decorators
@login_required
def like_comment(request, comment_id):
    comment_queryset = Comment.objects.filter(id=comment_id)

    if not comment_queryset.exists():
        return redirect('error_page') 

    comment = comment_queryset.first()

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    return redirect('manage_comments', recipe_id=comment.recipe.id)

decorators
def addToFavorite(request,*args,**kwargs):
    rid = kwargs.get('id')
    recipe = Recipe.objects.get(id=rid)
    user = request.user
    favorite_exists = Favorite.objects.filter(recipe=recipe, user=user).exists()
    if favorite_exists:
        messages.warning(request, f"{recipe.name} is already in your favorites.")
    else:
        Favorite.objects.create(recipe=recipe, user=user)
        messages.success(request, f"{recipe.name} has been added to your favorites!") 
    return redirect('favorite')

decorators  
def favorites_view(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    return render(request, 'favorite.html', {'favorite': favorites})

decorators
def RemoveFavorite(request,id):
   
        favorite = Favorite.objects.get(user=request.user, id=id)
        favorite.delete()
        messages.success(request,'Recipe removed from favorites')
        return redirect('favorite')
    

@method_decorator(decorator=decorators,name='dispatch')   
class ContactView(TemplateView):
    template_name='contact.html'

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated! Please log in again.')
            logout(request) 
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'changepass.html', {'form': form})