from django.shortcuts import render, redirect
from .models import Services, CurrentIssues, ElectionStories, PressReleases, TenderAndVacancies, Voters, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .forms import MyUserCreationForm, UserForm, VoterForm
import random
import string
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            HttpResponse("Hmm, there is no one with that email or password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'main/sign_up.html', {'error': 'Passwords do not match!'})

        User = get_user_model()
        user = User.objects.create(username=username, email=email, name=name)
        user.password = make_password(password1)
        user.save()

        user = authenticate(request, email=email, password=password1)
        login(request, user)

        return redirect('home')

    context = {}
    return render(request, 'main/sign_up.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    services = Services.objects.filter(Q(name__icontains=q))
    current_issues = CurrentIssues.objects.all().order_by('-id')[:2]
    election_stories = ElectionStories.objects.all().order_by('-id')[:2]
    tenders = TenderAndVacancies.objects.all().order_by('-id')[:2]
    return render(request, 'main/home.html', {'services': services, 'current_issues': current_issues, 'elections': election_stories, 'tenders': tenders})

@user_passes_test(lambda u: u.is_superuser)
def voters(request):
    locality = request.GET.get('locality')
    age = request.GET.get('age')
    age_filter = request.GET.get('age_filter')
    gender = request.GET.get('gender')
    district = request.GET.get('district')

    # Start with all objects
    filtered_voters = Voters.objects.all().order_by('-id')

    # Apply filters if provided
    if locality:
        filtered_voters = filtered_voters.filter(locality__icontains=locality)
    if age and age_filter:
        if age_filter == 'above':
            filtered_voters = filtered_voters.filter(age__gte=age)
        elif age_filter == 'below':
            filtered_voters = filtered_voters.filter(age__lte=age)
    if gender:
        filtered_voters = filtered_voters.filter(gender=gender)
    if district:
        filtered_voters = filtered_voters.filter(district=district)

    # Pagination
    paginator = Paginator(filtered_voters, 10)  # Show 10 voters per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get unique localities and genders for filtering options
    unique_localities = Voters.objects.values_list('locality', flat=True).distinct()
    unique_genders = Voters.objects.values_list('gender', flat=True).distinct()
    unique_district = Voters.objects.values_list('district', flat=True).distinct()

    return render(request, 'main/voters.html', {
        'page_obj': page_obj,
        'unique_localities': unique_localities,
        'unique_genders': unique_genders,
        'unique_district': unique_district
    })
def generate_random_vote():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(10))

def create_voter(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        gender = request.POST.get('gender')
        pob = request.POST.get('pob')
        age = int(request.POST.get('age'))  # Convert age to an integer
        house_no = request.POST.get('house_no')
        flat_name = request.POST.get('flat_name')
        locality = request.POST.get('locality')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        aadhar = request.POST.get('aadhar')
        image = request.FILES.get('image')

        try:
            age = int(age)
            if age <= 18:
                raise ValidationError("Age must be greater than 18.")
        except ValueError:
            return render(request, 'voters_form.html', {'error_message': 'Invalid age'})

        try:
            voter = Voters.objects.create(
                name=name,
                fname=fname,
                mname=mname,
                gender=gender,
                pob=pob,
                age=age,
                house_no=house_no,
                flat_name=flat_name,
                locality=locality,
                district=district,
                pincode=pincode,
                aadhar=aadhar,
                vote = generate_random_vote(),
                image = image
            )
            return redirect('home')
        except Exception as e:
            return render(request, 'main/voter_form.html', {'error_message': str(e)})
    else:
        return render(request, 'main/voter_form.html')


def voter_profile(request, aadhar):

    voter = get_object_or_404(Voters, aadhar=aadhar)
    services = Services.objects.all()
    current_issues = CurrentIssues.objects.all().order_by('-id')[:2]
    election_stories = ElectionStories.objects.all().order_by('-id')[:2]
    tenders = TenderAndVacancies.objects.all().order_by('-id')[:2]
    return render(request, 'main/voter_profile.html', {'voter': voter, 'services': services, 'current_issues': current_issues, 'elections': election_stories, 'tenders': tenders})