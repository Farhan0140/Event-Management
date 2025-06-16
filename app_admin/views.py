from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q, Count
from app_admin.models import Category, Event, Participant
from datetime import date
from app_admin.forms import Create_Model_Event, Create_Model_Category, Create_Model_User


def test(request):
    return render(request, "test.html")

def details(request):

    if request.GET.get('book_now'):
        id = request.GET.get('book_now')
        event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
        total_participant = event.participants.aggregate(p_cnt = Count('id'))
        user_form = Create_Model_User()
        context = {
            'event': event,
            'total_participant': total_participant['p_cnt'],
            'user_form': user_form
        }

        if request.method == "POST":
            user_form = Create_Model_User(request.POST)

            if user_form.is_valid():

                cln_data = user_form.cleaned_data
                print(cln_data)
                email = cln_data['user_email'].lower()
                email_from_db = Participant.objects.filter(user_email__iexact=email)
                print(email, email_from_db)
                
                if not email_from_db:
                    user = user_form.save()
                    user.event.add(event)

                    messages.success(request, "Account created & Booked Successfully")
                    return render(request, "create_user.html", context)

                else:
                    already_registered = email_from_db.prefetch_related('event').filter(event__id=event.id)
                    if already_registered:
                        messages.info(request, "You Registered This Event Already")
                        return render(request, "create_user.html", context)
                    else:
                        user = user_form.cleaned_data
                        user = Participant.objects.get(user_email = email)
                        user.event.add(event)
                        messages.info(request, "Registration Complete Successful For this Event")
                        return render(request, "create_user.html", context)
                
            else:
                messages.error(request, "Enter Valid Email [ example@example.example ] ")
                return render(request, "create_user.html", context)



        return render(request, "create_user.html", context)
    
    else:
        id = request.GET.get('dtl')

        event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
        total_participant = event.participants.aggregate(p_cnt = Count('id'))

        context = {
            'event': event,
            'total_participant': total_participant['p_cnt']
        }

    return render(request, "dashboard/details.html", context)


def organizer_dashboard(request):

    type = request.GET.get('type')
    st_date = request.GET.get('st_date')
    ed_date = request.GET.get('ed_date')
    category_selector = request.GET.get('category_selector')

    category_events = None

    events = Event.objects.select_related('category').prefetch_related('participants')

    total_event = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gt=date.today()).count()
    past_events = Event.objects.filter(date__lt=date.today()).count()
    total_participant = Participant.objects.count()

    counts = {
        'total_event': total_event,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'total_participant': total_participant,
    }

    if category_selector != None:
        event_name = "Categories"
        events = None
        category_events = Category.objects.get(id=category_selector).events.all().prefetch_related('participants')
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
            # print(s_d, l_d)
        else:
            event_name = "Todays Events"
            events = events.filter(date = date.today())

    

    context = {
        'events': events, 
        'counts': counts,
        'event_name': event_name,
        'today': date.today(),
        'categories': Category.objects.all(),
        'category_events': category_events
    }

    return render(request, "dashboard/organizer_dashboard.html", context)



def create_event(request):
    event_form = Create_Model_Event()
    category_form = Create_Model_Category()

    if request.method == "POST":
        event_form = Create_Model_Event(request.POST)
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
                return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form})
            else:
                id = obj.first().id
                objt = Category.objects.get(id=id)
                event = event_form.save(commit=False)
                event.category = objt
                event.save()
                messages.success(request, "Event Created Successfully")
                return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form})


    return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form})


def update_event(request, id):

    event = Event.objects.get(id = id) 

    event_form = Create_Model_Event(instance=event)
    category_form = Create_Model_Category(instance=event.category)

    if request.method == "POST":
        event_form = Create_Model_Event(request.POST, instance=event)
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


    return render(request, "create_event.html", {"event_form": event_form, "category_form": category_form})


def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id = id) 
        event.delete()
        messages.success(request, "Event Deleted Successfully")
    
    return redirect('organizer_dashboard')


def participants_details(request):
    participants = Participant.objects.all()

    context = {
        "participants": participants
    }

    return render(request, "participants_details.html", context)



def edit_participants_details(request, id):

    participant = Participant.objects.get(id = id) 

    user_form = Create_Model_User(instance = participant)

    if request.method == "POST":
        user_form = Create_Model_User(request.POST, instance = participant)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Account Updated Successfully")
            return redirect('participants_details')


    context = {
        'user_form': user_form
    }

    return render(request, "edit_participants_details.html", context)



def delete_participant(request, id):
    if request.method == "POST":
        participant = Participant.objects.get(id = id) 
        participant.delete()
        messages.success(request, "participant Deleted Successfully")
    
    return redirect('participants_details')


def category_details(request):
    categories = Category.objects.all()

    context = {
        "categories": categories
    }

    return render(request, "category_details.html", context)


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


def delete_category(request, id):
    if request.method == "POST":
        category = Category.objects.get(id = id) 
        category.delete()
        messages.success(request, "Category Deleted Successfully")
    
    return redirect('category_details')