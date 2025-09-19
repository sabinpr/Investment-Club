from django.contrib import admin
from .models import MembershipRequest

@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'requested_at', 'responded_at')
    search_fields = ('email', 'status')
    list_filter = ('status', 'requested_at', 'responded_at')
