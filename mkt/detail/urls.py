from django.conf.urls import include, patterns, url
from django.http import HttpResponse

from mkt.purchase.urls import app_purchase_patterns
from mkt.receipts.urls import app_receipt_patterns

from . import views


DummyResponse = lambda *args, **kw: HttpResponse()


urlpatterns = patterns('',
    # Merge app purchase / receipt patterns.
    ('^purchase/', include(app_purchase_patterns)),
    ('^purchase/', include(app_receipt_patterns)),

    url('^activity/', views.app_activity, name='detail.app_activity'),
)
