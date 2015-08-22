
from django.contrib import admin

from .models import Galaxy, Planet, Ship


admin.site.register(Galaxy)
admin.site.register(Planet)
admin.site.register(Ship)

