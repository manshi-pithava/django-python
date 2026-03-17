from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'role')  # ✅ Ensure these fields exist in UserProfile model

admin.site.register(UserProfile, UserProfileAdmin)
