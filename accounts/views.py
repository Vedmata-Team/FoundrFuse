from django.shortcuts import render, redirect

def join_beta(request):
    if request.method == 'POST':
        # Handle form submission here (save data, send email, etc.)
        # For now, just redirect to a thank you page or show a success message
        return render(request, 'accounts/join_beta.html', {'success': True})
    return render(request, 'accounts/join_beta.html')

def login_view(request):
    # You can implement your login logic here or use Django's built-in auth views
    return render(request, 'accounts/login.html')