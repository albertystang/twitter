from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep

# Unregister Groups
admin.site.unregister(Group)

# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on admin page
    fields = ['username']
    inlines = [ProfileInline]

# Unregister initial User, Profile
admin.site.unregister(User)

# Register User
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

# Register Meeps
admin.site.register(Meep)

# Register Profile
admin.site.register(Profile)