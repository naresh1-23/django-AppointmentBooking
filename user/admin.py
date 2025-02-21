from django.contrib import admin
from user.models import UserModel


class UserModelAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('username', 'email', 'contact',
                    'is_doctor', 'specialist', 'study')

    # Add search functionality for specific fields
    search_fields = ('username', 'email', 'specialist')

    # Filter by doctor status or other key fields
    list_filter = ('is_doctor', 'specialist')

    # Show all the details when editing an entry
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email', 'contact', 'is_doctor', 'specialist', 'study')
        }),
    )


# Register the model with the custom admin view
admin.site.register(UserModel, UserModelAdmin)
