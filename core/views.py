from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Blog, Category, Industry, NewsletterSubscriber, SiteSettings, Testimonial, FeatureFAQ, FounderSuccessStory, FounderFAQ, ChatbotFAQ
from openai import OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.http import JsonResponse

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def home(request):
    testimonials = Testimonial.objects.all()
    featured_blogs = Blog.objects.filter(is_featured=True, is_published=True).order_by('-created_at')[:3]
    return render(request, 'core/home.html', {
        'title': 'Home',
        'featured_blogs': featured_blogs,
        'testimonials': testimonials,
    })

def about(request):
    return render(request, 'core/about.html', {'title': 'About Us'})


def features(request):
    faqs = FeatureFAQ.objects.all()
    context = {
        'title': 'Features',
        'faqs': faqs,
    }
    return render(request, 'core/features.html', context)


def founders(request):
    success_stories = FounderSuccessStory.objects.all()
    faqs = FounderFAQ.objects.all()
    return render(request, 'core/founders.html', {
        'title': 'For Founders',
        'success_stories': success_stories,
        'faqs': faqs,
    })

def investors(request):
    return render(request, 'core/investors.html', {'title': 'For Investors'})

def pricing(request):
    return render(request, 'core/pricing.html', {'title': 'Pricing'})

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True)
    featured_blog = None
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', '')
    industry_slug = request.GET.get('industry', '')
    
    # Apply filters
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) | 
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    if category_slug:
        blogs = blogs.filter(categories__slug=category_slug)
    
    if industry_slug:
        blogs = blogs.filter(industry__slug=industry_slug)
    
    # Get a featured blog if no filters are applied
    if not (search_query or category_slug or industry_slug):
        featured_blogs = blogs.filter(is_featured=True)
        if featured_blogs.exists():
            featured_blog = featured_blogs.first()
            blogs = blogs.exclude(id=featured_blog.id)
    
    # Paginate the results
    paginator = Paginator(blogs, 6)  # 6 blogs per page
    page_number = request.GET.get('page')
    blogs_page = paginator.get_page(page_number)
    
    # Get all categories and industries for filtering
    categories = Category.objects.all()
    industries = Industry.objects.all()
    
    return render(request, 'core/blog_list.html', {
        'title': 'Blog',
        'blogs': blogs_page,
        'featured_blog': featured_blog,
        'categories': categories,
        'industries': industries,
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_industry': industry_slug,
    })

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    blog.increment_views()
    
    # Get related posts (same category or industry)
    related_posts = Blog.objects.filter(
        is_published=True
    ).exclude(
        id=blog.id
    )
    
    if blog.categories.exists():
        related_posts = related_posts.filter(categories__in=blog.categories.all())
    elif blog.industry:
        related_posts = related_posts.filter(industry=blog.industry)
    
    related_posts = related_posts.distinct()[:2]
    
    # Get categories for sidebar
    categories = Category.objects.all()
    
    # Get recent posts for sidebar
    recent_posts = Blog.objects.filter(
        is_published=True
    ).exclude(
        id=blog.id
    ).order_by('-created_at')[:3]
    
    return render(request, 'core/blog_detail.html', {
        'title': blog.title,
        'blog': blog,
        'related_posts': related_posts,
        'categories': categories,
        'recent_posts': recent_posts,
    })

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            else:
                messages.info(request, 'This email is already subscribed to our newsletter.')
        return redirect(request.META.get('HTTP_REFERER', 'core:home'))
    return redirect('core:home')

def context_processors(request):
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            site_settings = SiteSettings.objects.create()
    except:
        site_settings = None
    
    return {
        'site_settings': site_settings
    }

class ChatbotAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("🔵 Step 1: Received POST request.")
        user_message = request.data.get('message', '')
        print("🟢 Step 2: User message received:", user_message)

        if not user_message:
            return Response({'error': 'No message provided.'}, status=400)

        try:
            # ✅ Create OpenAI client with OpenRouter settings
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=settings.OPENROUTER_API_KEY,
                default_headers={
                    "HTTP-Referer": "https://foundrfuse.com",
                    "X-Title": "FoundrFuse AI Chat",
                }
            )

            print("🟡 Step 3: Sending request to OpenRouter (GPT-4o)...")

            completion = client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[
                    {"role": "system", "content": "You are FoundrFuse AI, a helpful assistant."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=200,
                temperature=0.7
            )

            bot_reply = completion.choices[0].message.content
            print("🟢 Step 4: Bot reply:", bot_reply)
            return Response({'reply': bot_reply})

        except Exception as e:
            print("🔴 Step 5: Error occurred:", str(e))
            return Response({'error': str(e)}, status=500)

def chatbot_faqs(request):
    faqs = list(ChatbotFAQ.objects.values('question', 'answer'))
    return JsonResponse({'faqs': faqs})

# ये सिर्फ available quota नहीं दिखाता, लेकिन API key valid है या नहीं ये चेक कर सकते हो।
