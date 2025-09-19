from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import (
    CustomUser, Contribution, Investment,
    Proposal, Vote, Meeting, AssetInvestment,
    Notification
)

# -------------------------------
# CustomUser Admin
# -------------------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'full_name', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'full_name']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('role', 'full_name')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Info', {
            'classes': ('wide',),
            'fields': ('role', 'full_name'),
        }),
    )



# -------------------------------
# Contribution Admin
# -------------------------------
@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ['user', 'month', 'amount']
    list_filter = ['month']
    search_fields = ['user__username']
    ordering = ['-month']


# -------------------------------
# Investment Admin
# -------------------------------
@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'proposal_asset_name', 'amount', 'invested_at')
    list_filter = ('proposal__status', 'proposal__risk_level')
    search_fields = ('user__username', 'proposal__asset_name')
    ordering = ('-invested_at',)

    def proposal_asset_name(self, obj):
        return obj.proposal.asset_name
    proposal_asset_name.short_description = 'Asset Name'


# -------------------------------
# AssetInvestment Admin
# -------------------------------
@admin.register(AssetInvestment)
class AssetInvestmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'quantity', 'current_value', 'invested_value', 'date_invested')
    list_filter = ('type',)
    search_fields = ('name',)
    ordering = ('-date_invested',)


# -------------------------------
# Proposal Admin
# -------------------------------
@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'proposer', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'risk_level']
    search_fields = ['asset_name', 'proposer__username']
    ordering = ['-created_at']


# -------------------------------
# Vote Admin
# -------------------------------
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['proposal', 'user', 'vote']
    list_filter = ['vote']
    search_fields = ['proposal__asset_name', 'user__username']
    ordering = ['proposal']


# -------------------------------
# Meeting Admin
# -------------------------------
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['date', 'agenda', 'meeting_link', 'status', 'host']
    list_filter = ['date']
    search_fields = ['agenda']
    ordering = ['-date']


# -------------------------------
# Notification Admin
# -------------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'title']
    ordering = ['-created_at']
