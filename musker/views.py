from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Meep
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import MeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout


def home(request):
    meeps = Meep.objects.all().order_by('-created_at')
    context = {'meeps': meeps}
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        context = {'meeps': meeps, 'form': form}
        if form.is_valid():
            meep = form.save(commit=False)
            meep.user = request.user
            meep.save()
            messages.success(request, 'Your Meep Has Been Posted!')
            return redirect('home')        
        return render(request, 'home.html', context)
    return render(request, 'home.html', context)


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        context = {'profiles': profiles}
        return render(request, 'profile_list.html', context)
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')


def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = get_object_or_404(Profile, pk=pk)
        # Unfollow the profile
        request.user.profile.follows.remove(profile)
        # Save our profile
        request.user.profile.save()
        messages.success(request, f"You have successfully unfollow {profile.user.username}...")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'You must be logged in to unfollow...')
        return redirect('home')
    

def follow(request, pk):
    if request.user.is_authenticated:
        # Get the profile to unfollow
        profile = get_object_or_404(Profile, pk=pk)
        # Unfollow the profile
        request.user.profile.follows.add(profile)
        # Save our profile
        request.user.profile.save()
        messages.success(request, f"You have successfully follow {profile.user.username}...")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'You must be logged in to unfollow...')
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:        
        profile = get_object_or_404(Profile, pk=pk)
        meeps = Meep.objects.filter(user=profile.user)
        # Post Form logic
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            # Save profile
            current_user_profile.save()
        context = {'profile': profile, "meeps": meeps}
        return render(request, 'profile.html', context)
        
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')


def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)            
            context = {'profiles': profiles}
            return render(request, 'followers.html', context)
        else:
            messages.success(request, 'That is not your profile page...')
            return redirect('home')
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')
    

def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            #profiles = Profile.objects.get(user_id=pk)
            profiles = get_object_or_404(Profile, user_id=pk)                        
            context = {'profiles': profiles}
            return render(request, 'follows.html', context)
        else:
            messages.success(request, 'That is not your profile page...')
            return redirect('home')
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in.')
            return redirect('home')
        else:
            messages.success(request, 'There was an error when logging in! Please try again...')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out. Sorry to meep you go...')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']

            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered! Welcome!')
            return redirect('home')
    return render(request, 'register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        # Get forms
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance= current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance= profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, 'Your profile has been updated!')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, 'You must be logged in to view this page...')
        return redirect('home')


def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)        
    else:
        messages.success(request, 'You must be logged in...')        
    return redirect(request.META.get('HTTP_REFERER'))


def meep_show(request, pk):
    meep = get_object_or_404(Meep, pk=pk)
    if meep:
        context = {'meep': meep}
        return render(request, 'meep_show.html', context)
    else:
        messages.success(request, 'That meep does not exist...')
        return redirect('home')


def delete_meep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        # Check to see if you own the meep
        if request.user.username == meep.user.username:
            meep.delete()
            messages.success(request, "The meep has been deleted!")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, "You don't own that meep!")
            return redirect('home')
    else:
        messages.success(request, 'Please log in to continue...')
        return redirect(request.META.get('HTTP_REFERER'))
    

def edit_meep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)        
        if request.user.username == meep.user.username:
            form = MeepForm(request.POST or None, instance=meep)
            context = {'form': form, 'meep': meep}
            if request.method == 'POST':                    
                if form.is_valid():                    
                    form.save()
                    messages.success(request, 'Your Meep Has Been Updated!')                        
                    return redirect('profile', request.user.profile.id)
            else:
                return render(request, 'edit_meep.html', context)
        else:
            messages.success(request, 'You do not own this meep!')                        
            return redirect('home')
    else:
        messages.success(request, 'Please log in to continue...') 
        return redirect('home')


def search(request):
    context = {}
    if request.method == 'POST':        
        search = request.POST['search']
        # Search the database
        searched = Meep.objects.filter(body__contains=search)        
        context = {'search': search, 'searched': searched}
        return render(request, 'search.html', context)
    return render(request, 'search.html', context)


def search_user(request):
    context = {}
    if request.method == 'POST':        
        search = request.POST['search']
        if search == '':
            searched = None     
        else:
            searched = User.objects.filter(username__contains=search)

        context = {'search': search, 'searched': searched}
        return render(request, 'search_user.html', context)
    return render(request, 'search_user.html', context)