from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from user.forms import Register_Form, sign_in_form

# Create your views here.


def user_registration(request):
    form = Register_Form()

    if request.method == 'POST':
        form = Register_Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "User Created Successfully")
            return redirect("user_registration")

    context = {
        "form": form,
    }

    return render(request, "user_authentication/registration_form.html", context)


def sign_up(request):
    form = sign_in_form()

    if request.method == 'POST':
        form = sign_in_form(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # return redirect("eikhane user jei group er oi dashboard e redirect korbe")
            return redirect("organizer_dashboard")

    context = {
        'form': form,
    }
    return render(request, "user_authentication/login_form.html", context)


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    
    return redirect('sign-in')



def details(request):
    pass

#     if request.GET.get('book_now'):
#         id = request.GET.get('book_now')
#         event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
#         total_participant = event.participants.aggregate(p_cnt = Count('id'))
#         user_form = Create_Model_User()
#         context = {
#             'event': event,
#             'total_participant': total_participant['p_cnt'],
#             'user_form': user_form
#         }

#         if request.method == "POST":
#             user_form = Create_Model_User(request.POST)

#             if user_form.is_valid():

#                 cln_data = user_form.cleaned_data
#                 print(cln_data)
#                 email = cln_data['user_email'].lower()
#                 email_from_db = Participant.objects.filter(user_email__iexact=email)
#                 print(email, email_from_db)
                
#                 if not email_from_db:
#                     user = user_form.save()
#                     user.event.add(event)

#                     messages.success(request, "Account created & Booked Successfully")
#                     return render(request, "create_user.html", context)

#                 else:
#                     already_registered = email_from_db.prefetch_related('event').filter(event__id=event.id)
#                     if already_registered:
#                         messages.info(request, "You Registered This Event Already")
#                         return render(request, "create_user.html", context)
#                     else:
#                         user = user_form.cleaned_data
#                         user = Participant.objects.get(user_email = email)
#                         user.event.add(event)
#                         messages.info(request, "Registration Complete Successful For this Event")
#                         return render(request, "create_user.html", context)
                
#             else:
#                 messages.error(request, "Enter Valid Email [ example@example.example ] ")
#                 return render(request, "create_user.html", context)



#         return render(request, "create_user.html", context)
    
#     else:
#         id = request.GET.get('dtl')

#         event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
#         total_participant = event.participants.aggregate(p_cnt = Count('id'))

#         context = {
#             'event': event,
#             'total_participant': total_participant['p_cnt']
#         }

#     return render(request, "dashboard/details.html", context)



def participants_details(request):
    # participants = Participant.objects.all()

    # context = {
    #     "participants": participants
    # }

    # return render(request, "participants_details.html", context)
    pass



def edit_participants_details(request, id):
    pass

    # participant = Participant.objects.get(id = id) 

    # user_form = Create_Model_User(instance = participant)

    # if request.method == "POST":
    #     user_form = Create_Model_User(request.POST, instance = participant)

    #     if user_form.is_valid():
    #         user_form.save()
    #         messages.success(request, "Account Updated Successfully")
    #         return redirect('participants_details')


    # context = {
    #     'user_form': user_form
    # }

    # return render(request, "edit_participants_details.html", context)



def delete_participant(request, id):
    pass
    # if request.method == "POST":
    #     participant = Participant.objects.get(id = id) 
    #     participant.delete()
    #     messages.success(request, "participant Deleted Successfully")
    
    # return redirect('participants_details')

