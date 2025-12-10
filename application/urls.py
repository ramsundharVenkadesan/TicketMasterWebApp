from django.urls import path
from . import views
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('favorites/', views.SavedEvents.as_view(), name='favorites'),
    path('<str:event_id>', views.DeleteEvent.as_view(), name='delete'),
]