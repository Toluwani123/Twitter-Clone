from django.contrib import admin
from .models import Person, Talks
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Person)
admin.site.register(Talks)


class ProfileInline(admin.StackedInline):
    model = Person


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on admin page
    fields = ["username"]
    inlines = [ProfileInline]


# Unregister initial User
admin.site.unregister(User)

# Reregister User and Profile
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Register Meeps
