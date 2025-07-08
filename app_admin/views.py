from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q, Count
from app_admin.models import Category, Event
from datetime import date
from app_admin.forms import Create_Model_Event, Create_Model_Category
from django.contrib.auth.decorators import login_required


@login_required(login_url="/user/sign-in/")
def organizer_dashboard(request):

    type = request.GET.get('type')
    st_date = request.GET.get('st_date')
    ed_date = request.GET.get('ed_date')
    category_selector = request.GET.get('category_selector')

    category_events = None

    events = Event.objects.select_related('category')

    total_event = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gt=date.today()).count()
    past_events = Event.objects.filter(date__lt=date.today()).count()

    counts = {
        'total_event': total_event,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }

    if category_selector != None:
        event_name = "Categories"
        events = None
        category_events = Category.objects.get(id=category_selector).events.all()
    elif type == 'upcoming_events':
        events = events.filter(date__gt = date.today())
        event_name = "Upcoming Events"
    elif type == 'all':
        events = events.all()
        event_name = "All Events"
    elif type == 'todays_events':
        event_name = "Todays Events"
        events = events.filter(date = date.today())
    elif type == 'past_events':
        events = events.filter(date__lt = date.today())
        event_name = "Past Events"
    else:
        event_name = "In Range"
        if st_date != None and ed_date != None:
            if(st_date < ed_date):
                s_d = st_date
                l_d = ed_date
            else:
                l_d = st_date
                s_d = ed_date
            
            events = events.filter(date__range=(s_d, l_d))
        else:
            event_name = "Todays Events"
            events = events.filter(date = date.today())

    

    context = {
        'events': events, 
        'counts': counts,
        'event_name': event_name,
        'today': date.today(),
        'categories': Category.objects.all(),
        'category_events': category_events,
        'category_name': category_events,
    }

    return render(request, "dashboard/organizer_dashboard.html", context)


@login_required(login_url="/user/sign-in/")
def create_event(request):
    event_form = Create_Model_Event()
    category_form = Create_Model_Category()

    if request.method == "POST":
        event_form = Create_Model_Event(request.POST, request.FILES)
        category_form = Create_Model_Category(request.POST)

        if event_form.is_valid() and category_form.is_valid():

            cln_data = category_form.cleaned_data
            ctg_name = cln_data['category_name'].lower()
            obj = Category.objects.filter(category_name__iexact=ctg_name)

            if not obj.exists():
                category = category_form.save()
                event = event_form.save(commit=False)
                event.category = category
                event.save()
                messages.success(request, "Event Created Successfully")
                return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form, "categories":Category.objects.all()})
            else:
                id = obj.first().id
                objt = Category.objects.get(id=id)
                event = event_form.save(commit=False)
                event.category = objt
                event.save()
                messages.success(request, "Event Created Successfully")
                return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form, "categories":Category.objects.all()})


    return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form, "categories":Category.objects.all()})


@login_required(login_url="/user/sign-in/")
def update_event(request, id):

    event = Event.objects.get(id = id) 

    event_form = Create_Model_Event(instance=event)
    category_form = Create_Model_Category(instance=event.category)

    if request.method == "POST":
        event_form = Create_Model_Event(request.POST, request.FILES, instance=event)
        category_form = Create_Model_Category(request.POST, instance=event.category)

        if event_form.is_valid() and category_form.is_valid():
            cln_data = category_form.cleaned_data
            ctg_name = cln_data['category_name'].lower()
            obj = Category.objects.filter(category_name__iexact=ctg_name)

            if not obj.exists():
                category = category_form.save()
                event = event_form.save(commit=False)
                event.category = category
                event.save()
                messages.success(request, "Event Update Successfully")
                return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form})
            else:
                id = obj.first().id
                objt = Category.objects.get(id=id)
                event = event_form.save(commit=False)
                event.category = objt
                event.save()
                messages.success(request, "Event Update Successfully")
                return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form})


    return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form, "categories":Category.objects.all()})



@login_required(login_url="/user/sign-in/")
def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id = id) 
        event.delete()
        messages.success(request, "Event Deleted Successfully")
    
    return redirect('organizer_dashboard')


@login_required(login_url="/user/sign-in/")
def create_category(request):
    category_form = Create_Model_Category()

    if request.method == "POST":
        category_form = Create_Model_Category(request.POST)

        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category Created Successfully")
            return redirect('category_details')


    context = {
        'category_form': category_form
    }

    return render(request, "edit_category.html", context)



@login_required(login_url="/user/sign-in/")
def category_details(request):
    categories = Category.objects.all()

    context = {
        "categories": categories
    }

    return render(request, "category_details.html", context)



@login_required(login_url="/user/sign-in/")
def edit_category_details(request, id):

    category = Category.objects.get(id = id) 
    category_form = Create_Model_Category(instance = category)

    if request.method == "POST":
        category_form = Create_Model_Category(request.POST, instance = category)

        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category Updated Successfully")
            return redirect('category_details')


    context = {
        'category_form': category_form
    }

    return render(request, "edit_category.html", context)


@login_required(login_url="/user/sign-in/")
def delete_category(request, id):
    if request.method == "POST":
        category = Category.objects.get(id = id) 
        category.delete()
        messages.success(request, "Category Deleted Successfully")
    
    return redirect('category_details')


@login_required(login_url="/user/sign-in/")
def organizer_search_event(request):

    search_txt = request.GET.get('search')

    search_result_by_name = Event.objects.filter(event_name__icontains=search_txt)
    search_result_by_location = Event.objects.filter(location__icontains=search_txt)
    context = {
        'search_result_by_name': search_result_by_name,
        'search_result_by_location': search_result_by_location,
    }

    return render(request, "organizer_search_box.html", context)