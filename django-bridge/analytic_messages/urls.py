from django.urls import path, include

from analytic_messages.views import *

urlpatterns = [
    path('messages/', MessageTableView.as_view(), name='datatable'),
    path('', MessageOverview.as_view(), name='overview'),
    path('message/<int:id>/', include([
        path('', MessageInfoView.as_view(), name='info'),
        path('dismiss/', MessageDismissFormView.as_view(), name='dismiss')
    ])),

    # path('admin/', admin.site.urls),
]