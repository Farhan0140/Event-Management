
from django.urls import path
from user.views import user_registration, sign_up, sign_out, show_all_user, assign_role, create_role, delete_user, group_lists, update_role, delete_role, activate_user, Profile, Edit_Profile, Change_Password, Reset_Password, Confirm_Reset_Password
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    path("sign-up/", user_registration, name="sign-up"),
    path("sign-in/", sign_up, name="sign-in"),
    path("sign-out/", sign_out, name="sign-out"),
    path("admin/dashboard/", show_all_user, name="admin_dashboard"),
    path("admin/create_role/", create_role, name="create_role"),
    path("admin/<int:user_id>/assign_role/", assign_role, name="assign_role"),
    path("admin/<int:user_id>/delete_user/", delete_user, name="delete_user"),
    path("admin/groups/", group_lists, name="groups"), 
    path("admin/<int:group_id>/update_role/", update_role, name="update_role"),
    path("admin/<int:group_id>/delete_role/", delete_role, name="delete_role"),
    path("activate/<int:user_id>/<str:token>/", activate_user, name="activate_user"),

    path("profile/", Profile.as_view(), name="user_profile"),
    path("update_profile/", Edit_Profile.as_view(), name="update_profile"),
    path("change_password/", Change_Password.as_view(), name="change_password"),
    path("password_changed_done/", PasswordChangeDoneView.as_view(template_name = "accounts/password_changed_done.html"), name="password_change_done"),
    path('reset_password/', Reset_Password.as_view(), name='reset_password'),
    path("password_reset/confirm/<uidb64>/<token>/", Confirm_Reset_Password.as_view(), name="password_reset_confirm")
]
