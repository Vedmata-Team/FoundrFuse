from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q, F
from django.http import JsonResponse
import csv
import os
from django.conf import settings
from .forms import UserRegistrationForm, ProfileForm, WaitlistForm
from .models import Profile, Match, SwipeAction, Waitlist
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
import base64
from django.core.files.base import ContentFile

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

def register(request):
    print("DEBUG: Entered register view. Method:", request.method)
    if request.method == 'POST':
        print("DEBUG: POST data received:", request.POST)
        print("DEBUG: FILES data received:", request.FILES)
        form = UserRegistrationForm(request.POST, request.FILES)
        print("DEBUG: Form created. Is valid?", form.is_valid())
        if form.is_valid():
            user = form.save()
            print("DEBUG: User created:", user)
            profile = user.profile
            print("DEBUG: Profile accessed:", profile)
            profile.user_type = form.cleaned_data['user_type']
            profile.country = form.cleaned_data['country']
            profile.state = form.cleaned_data['state']
            profile.city = form.cleaned_data['city']
            profile.pincode = form.cleaned_data['pincode']
            profile.phone = request.POST.get('phone', '')
            profile.country_code = request.POST.get('country_code', '')

            cropped_data = request.POST.get('cropped_image_data')
            print("DEBUG: Cropped image data present?", bool(cropped_data))
            if cropped_data:
                try:
                    format, imgstr = cropped_data.split(';base64,')
                    ext = format.split('/')[-1]
                    profile.profile_image = ContentFile(base64.b64decode(imgstr), f"profile_{user.id}.{ext}")
                    print("DEBUG: Cropped image saved to profile.")
                except Exception as e:
                    print("DEBUG: Error processing cropped image:", e)
            elif form.cleaned_data.get('profile_image'):
                profile.profile_image = form.cleaned_data['profile_image']
                print("DEBUG: Uploaded image saved to profile.")
            else:
                print("DEBUG: No image provided.")

            profile.save()
            print("DEBUG: Profile saved.")
            messages.success(request, 'Your account has been created successfully! You can now log in.')
            print("DEBUG: Success message added. Redirecting to home.")
            return redirect('core:home')
        else:
            print("DEBUG: Form errors:", form.errors)
    else:
        print("DEBUG: GET request, rendering empty form.")
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form, 'title': 'Register'})

@login_required
def profile(request):
    user = request.user
    user_profile = user.profile
    
    # Redirect to appropriate dashboard based on user type
    if user_profile.user_type == 'founder':
        return founder_dashboard(request)
    else:
        return investor_dashboard(request)
        
@login_required
def founder_dashboard(request):
    user = request.user
    user_profile = user.profile
    
    # Get pending matches
    pending_matches = Match.objects.filter(
        Q(user1=user) | Q(user2=user),
        status='pending'
    )[:5]  # Limit to 5 most recent
    
    # Format matches for display
    formatted_matches = []
    for match in pending_matches:
        # Determine the other user in the match
        other_user = match.user2 if match.user1 == user else match.user1
        formatted_matches.append({
            'match_id': match.id,
            'user2': other_user,
            'created_at': match.created_at
        })
    
    return render(request, 'accounts/founder_dashboard.html', {
        'title': 'Founder Dashboard',
        'profile': user_profile,
        'pending_matches': formatted_matches,
    })

@login_required
def investor_dashboard(request):
    user = request.user
    user_profile = user.profile
    
    # Get pending matches
    pending_matches = Match.objects.filter(
        Q(user1=user) | Q(user2=user),
        status='pending'
    )[:5]  # Limit to 5 most recent
    
    # Format matches for display
    formatted_matches = []
    for match in pending_matches:
        # Determine the other user in the match
        other_user = match.user2 if match.user1 == user else match.user1
        formatted_matches.append({
            'match_id': match.id,
            'user2': other_user,
            'created_at': match.created_at
        })
    
    return render(request, 'accounts/investor_dashboard.html', {
        'title': 'Investor Dashboard',
        'profile': user_profile,
        'pending_matches': formatted_matches,
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            cropped_data = request.POST.get('cropped_image_data')
            if cropped_data:
                format, imgstr = cropped_data.split(';base64,')
                ext = format.split('/')[-1]
                profile.profile_image = ContentFile(base64.b64decode(imgstr), f"profile_{request.user.id}.{ext}")
            elif form.cleaned_data.get('profile_image'):
                profile.profile_image = form.cleaned_data['profile_image']
            profile.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'title': 'Edit Profile',
        'form': form,
    })

@login_required
def discover(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)
        profile = user.profile
    
    # Check if the user has free swipes left (for non-premium users)
    if not profile.is_premium and profile.swipes_left <= 0:
        messages.warning(request, 'You have used all your daily swipes. Upgrade to Premium for unlimited swipes!')
        return render(request, 'accounts/discover.html', {
            'title': 'Discover',
            'out_of_swipes': True,
        })
    
    # Get profiles that haven't been swiped on yet
    swiped_users = SwipeAction.objects.filter(from_user=user).values_list('to_user_id', flat=True)
    
    # Find opposite user type (founder -> investor, investor -> founder)
    opposite_type = 'investor' if profile.user_type == 'founder' else 'founder'
    
    profiles_to_show = Profile.objects.filter(
        user_type=opposite_type
    ).exclude(
        user__in=swiped_users
    ).exclude(
        user=user
    )
    
    # Apply filtering logic for premium users
    if profile.is_premium:
        if request.GET.get('industry'):
            profiles_to_show = profiles_to_show.filter(industry=request.GET.get('industry'))
        
        if request.GET.get('location'):
            profiles_to_show = profiles_to_show.filter(location__icontains=request.GET.get('location'))
            
        # Additional premium filters
        if request.GET.get('stage') and profile.user_type == 'investor':
            # Filter for investors looking at founders at specific stages
            # This assumes you have a 'stage' field or similar in Profile
            profiles_to_show = profiles_to_show.filter(stage=request.GET.get('stage'))
            
        if request.GET.get('investment_range') and profile.user_type == 'founder':
            # Filter for founders looking at investors with specific investment ranges
            # This assumes you have an 'investment_range' field or similar in Profile
            profiles_to_show = profiles_to_show.filter(investment_range=request.GET.get('investment_range'))
    
    # Get profiles to show (now we'll show multiple in a stack)
    if profiles_to_show.exists():
        # Limit to 10 profiles for better performance
        profiles = list(profiles_to_show.order_by('?')[:10])
    else:
        profiles = []
        messages.info(request, "You've viewed all available profiles for now. Check back soon!")
    
    return render(request, 'accounts/discover.html', {
        'title': 'Discover',
        'profiles': profiles,
        'swipes_left': profile.swipes_left,
    })

@login_required
def swipe_action(request, profile_id, action):
    user = request.user
    profile = user.profile
    to_user = get_object_or_404(User, id=profile_id)
    
    # Check if user has swipes left (free tier limit)
    if not profile.is_premium and profile.swipes_left <= 0:
        return JsonResponse({'status': 'error', 'message': 'No swipes left. Upgrade to Premium!'})
    
    # Record the swipe action
    SwipeAction.objects.update_or_create(
        from_user=user,
        to_user=to_user,
        defaults={'action': action}
    )
    
    # Decrease swipe count for non-premium users
    if not profile.is_premium:
        profile.swipes_left -= 1
        profile.save()
    
    # Check if it's a match
    match_created = False
    if action == 'like':
        # Check if the other user also liked the current user
        mutual_like = SwipeAction.objects.filter(
            from_user=to_user,
            to_user=user,
            action='like'
        ).exists()
        
        if mutual_like:
            # Create a match
            Match.objects.get_or_create(
                user1=user,
                user2=to_user,
                defaults={'status': 'accepted'}
            )
            match_created = True
    
    return JsonResponse({
        'status': 'success',
        'action': action,
        'match': match_created,
        'swipes_left': profile.swipes_left
    })

@login_required
def matches(request):
    user = request.user
    
    # Get all matches involving the current user
    matches_as_user1 = Match.objects.filter(user1=user, status='accepted')
    matches_as_user2 = Match.objects.filter(user2=user, status='accepted')
    
    # Combine and format the matches for display
    matches_data = []
    
    for match in matches_as_user1:
        matched_user = match.user2
        matches_data.append({
            'match_id': match.id,
            'user': matched_user,
            'profile': matched_user.profile,
            'created_at': match.created_at,
        })
    
    for match in matches_as_user2:
        matched_user = match.user1
        matches_data.append({
            'match_id': match.id,
            'user': matched_user,
            'profile': matched_user.profile,
            'created_at': match.created_at,
        })
    
    # Sort matches by created_at (newest first)
    matches_data.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render(request, 'accounts/matches.html', {
        'title': 'My Matches',
        'matches': matches_data,
    })

def waitlist(request):
    if request.method == 'POST':
        form = WaitlistForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_type = form.cleaned_data['user_type']
            company_name = form.cleaned_data['company_name']
            
            # Check if email already exists in waitlist
            if not Waitlist.objects.filter(email=email).exists():
                Waitlist.objects.create(
                    email=email,
                    user_type=user_type,
                    company_name=company_name
                )
                messages.success(request, "You've been added to our waitlist! We'll notify you when you're granted access.")
            else:
                messages.info(request, "This email is already on our waitlist. We'll be in touch soon!")
            
            return redirect('core:home')
    else:
        form = WaitlistForm()
    
    return render(request, 'accounts/waitlist.html', {
        'title': 'Join Waitlist',
        'form': form,
    })

def get_states(request):
    country_code = request.GET.get('country_code')
    states = []
    with open(os.path.join(settings.BASE_DIR, 'accounts', 'states.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['country_code'] == country_code:
                states.append({'id': row['id'], 'name': row['name'], 'state_code': row['state_code']})
    return JsonResponse({'states': states})

def get_cities(request):
    state_code = request.GET.get('state_code')
    cities = []
    with open(os.path.join(settings.BASE_DIR, 'accounts', 'cities.csv'), encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['state_code'] == state_code:
                cities.append({'id': row['id'], 'name': row['name']})
    return JsonResponse({'cities': cities})
