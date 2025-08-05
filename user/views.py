from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from user.forms import Register_Form, sign_in_form, create_group_form
from django.contrib.auth.models import Group
from app_admin.models import Event, Category
from datetime import date
from django.db.models import Count
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from app_admin.views import is_organizer
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

User = get_user_model()



# checking User groups

def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_participant(user):
    return user.groups.filter(name="Participant").exists()



def user_registration(request):
    form = Register_Form()

    if request.method == 'POST':
        form = Register_Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "A confirmation mail send to your mail..")
            return redirect("sign-in")

    context = {
        "form": form,
    }

    return render(request, "user_authentication/registration_form.html", context)


def activate_user(request, user_id, token):
    user = User.objects.get(id = user_id)
    try:
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            messages.success(request, "Your account already registered, Please Login")
            return redirect('sign-in')
    except Exception as e:
        print("User not found")


def dashboard(request):
    user = request.user

    if is_admin(user):
        return redirect("admin_dashboard")
    elif is_organizer(user):
        return redirect("organizer_dashboard")
    else:
        return redirect("home")


def sign_up(request):
    form = sign_in_form()

    if request.method == 'POST':
        form = sign_in_form(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if is_admin(user):
                return redirect("admin_dashboard")
            elif is_organizer(user):
                return redirect("organizer_dashboard")
            else:
                return redirect("home")
            

    context = {
        'form': form,
    }
    return render(request, "user_authentication/login_form.html", context)


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    
    return redirect('sign-in')


# Admin Part
@login_required(login_url="/user/sign-in/")
@user_passes_test(is_admin, login_url="no_permission")
def show_all_user(request):
    users = User.objects.all()

    context = {
        "users": users,
    }

    return render(request, "admin/admin_dashboard.html", context)


@login_required(login_url="/user/sign-in/")
@user_passes_test(is_admin, login_url="no_permission")
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user_name = user.username

    if request.method == 'POST':
        is_admin = user.groups.filter(name="Admin").exists()

        if is_admin:
            messages.error(request, "You cannot delete Admin")
            return redirect('admin_dashboard')
        else:
            user.delete()
            messages.success(request, f"User {user_name} deleted successfully")
            return redirect('admin_dashboard')
        
    return redirect('admin_dashboard')



@login_required(login_url="/user/sign-in/")
@user_passes_test(is_admin, login_url="no_permission")
def assign_role(request, user_id):
    user = User.objects.get(id = user_id)
    roles = Group.objects.all()

    if request.method == 'POST':
        selected_role = request.POST.get("selected_role")
        role = Group.objects.get(id=selected_role)
        user.groups.clear()
        user.groups.add(role)
        user.save()
        messages.success(request, f"User {user.username} role successfully changed to {role.name}")
        return redirect('admin_dashboard')

    context = {
        "roles": roles,
        "user": user,
    }

    return render(request, "admin/change_role.html", context)


@login_required(login_url="/user/sign-in/")
@user_passes_test(is_admin, login_url="no_permission")
def create_role(request):   # creating group
    form = create_group_form()

    if request.method == 'POST':
        form = create_group_form(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Role created successfully")
            return redirect('create_role')

    context = {
        'form': form,
        "button_name": "Create Role"
    }

    return render(request, "admin/create_role.html", context)


@login_required(login_url="/user/sign-in/")
@user_passes_test(is_admin, login_url="no_permission")
def delete_role(request, group_id):
    group = Group.objects.get(id = group_id)

    if request.method == 'POST':
        group_name = group.name
        group.delete()
        messages.success(request, "Group deleted successfully")
        return redirect('groups')
    
    return redirect('groups')


@login_required(login_url="/user/sign-in/")
@user_passes_test(is_admin, login_url="no_permission")
def update_role(request, group_id):
    group = Group.objects.get(id = group_id)
    form = create_group_form(instance=group)

    if request.method == 'POST':
        form = create_group_form(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group\\Role Updated Successfully")
            return redirect('groups')
    
    context = {
        "form": form,
        "button_name": "Update Role"
    }

    return render(request, "admin/create_role.html", context)


@login_required(login_url="/user/sign-in/")
@user_passes_test(is_admin, login_url="no_permission")
def group_lists(request):
    groups = Group.objects.all()

    context = {
        "groups": groups,
    }

    return render(request, "admin/group_list.html", context)


# Participant Part

@login_required(login_url="user/sign-in/")
def participant_dashboard(request):
    user = User.objects.get(id=request.user.id)
    events = user.rsvp_events.all()

    context = {
        "events": events,
    }
    
    return render(request, "participant/dashboard.html", context)




@login_required(login_url="user/sign-in/")
def events_list(request):

    type = request.GET.get('type')
    st_date = request.GET.get('st_date')
    ed_date = request.GET.get('ed_date')
    category_selector = request.GET.get('category_selector')

    category_events = None

    events = Event.objects.select_related('category').annotate(user_count=Count('participant'))

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
        category_events = (Category.objects.get(id=category_selector).events.annotate(user_count=Count('participant')).select_related('category'))
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

    user = User.objects.get(id=request.user.id)
    user_event_list = user.rsvp_events.all()
    user_events = [event.id  for event in user_event_list]

    context = {
        'events': events, 
        'counts': counts,
        'event_name': event_name,
        'today': date.today(),
        'categories': Category.objects.all(),
        'category_events': category_events,
        'user_events': user_events,
    }

    return render(request, "participant/events_list.html", context)


@login_required(login_url="user/sign-in/")
def view_details(request, event_id):
    user = User.objects.get(id=request.user.id)
    event = Event.objects.get(id = event_id)

    context = {
        "event": event,
        "is_rsvp": user.rsvp_events.filter(id=event_id).exists(),
    }

    return render(request, "participant/event_details.html", context)


@login_required(login_url="user/sign-in/")
def rsvp(request, event_id):
    user = User.objects.get(id=request.user.id)
    event = Event.objects.get(id=event_id)

    is_exist = user.rsvp_events.filter(id=event_id).exists()

    if is_exist:
        messages.error(request, "You already done RSVP in this event")
        return redirect('events_list')
    
    event.participant.add(user)

    messages.success(request, "Your RSVP successfully completed")
    return redirect('events_list')


@login_required(login_url="user/sign-in/")
def search_event(request):

    search_txt = request.GET.get('search')

    search_result_by_name = Event.objects.filter(event_name__icontains=search_txt)
    search_result_by_location = Event.objects.filter(location__icontains=search_txt)
    context = {
        'search_result_by_name': search_result_by_name,
        'search_result_by_location': search_result_by_location,
    }

    return render(request, "participant/search_box.html", context)


def no_permission(request):
    return render(request, "no_permission.html")


class Profile( LoginRequiredMixin, TemplateView ):
    template_name = 'accounts/profile.html'
    login_url = reverse_lazy("sign-in")

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context["user_name"] = user.username 
        context["user_image"] = user.profile_img
        context["full_name"] = user.get_full_name()
        context["email"] = user.email
        context["phone"] = user.phone

        context["last_login"] = user.last_login
        context["date_joined"] = user.date_joined
        return context
    