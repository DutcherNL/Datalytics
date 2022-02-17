from django.urls import path

from analytic_messages.views import MessageTableView, MessageInfoView, MessageOverview

urlpatterns = [
    path('messages/', MessageTableView.as_view(), name='datatable'),
    path('', MessageOverview.as_view(), name='overview'),
    path('message/<int:id>/', MessageInfoView.as_view(), name='info'),
    # path('admin/', admin.site.urls),
]