from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q, Count
from app_admin.models import Category, Event
from datetime import date
from app_admin.forms import Create_Model_Event, Create_Model_Category

# Create your views here.

def test(request):
    return render(request, "test.html")



def organizer_dashboard(request):

    type = request.GET.get('type')
    st_date = request.GET.get('st_date')
    ed_date = request.GET.get('ed_date')
    category_selector = request.GET.get('category_selector')

    category_events = None

    events = Event.objects.select_related('category').prefetch_related('participants')
    

    counts = events.aggregate(
        total_event = Count('id'),
        total_participant = Count('participants'),
        upcoming_events = Count('id', filter = Q(date__gt = date.today())),
        past_events = Count('id', filter = Q(date__lt = date.today()))
    )

    if category_selector != None:
        event_name = "Categories"
        events = None
        category_events = Category.objects.get(id=category_selector)
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