from django.contrib import admin
from .models import Login, Profile, Reports, Review, Address, Medical1, Doc_login, Doc_profile, Doc_address,Report_sent, Conversation
# Register your models here.
admin.site.register(Login)
admin.site.register(Profile)
admin.site.register(Reports)
admin.site.register(Review)
admin.site.register(Address)
admin.site.register(Medical1)
admin.site.register(Doc_login)
admin.site.register(Doc_profile)
admin.site.register(Doc_address)
admin.site.register(Report_sent)
admin.site.register(Conversation)
