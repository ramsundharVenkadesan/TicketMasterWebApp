"""
URL configuration for TicketMaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # Admin controller
from django.urls import path, include # Include other applications
from django.conf.urls.static import static # The static helper function
from django.conf import settings # Settings module imported from configuration package

urlpatterns = [ # URL patterns to include various applications
    path('admin/', admin.site.urls), # Admin path
    path('', include('application.urls')) # Application path
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Serve static files from the static-files folder
