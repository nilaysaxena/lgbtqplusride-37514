from django.urls import re_path

from .viewsets import PaymentSheetView, GetStripePaymentsView, GetPaymentMethodsView, DetachPaymentMethodsView, \
    AttachPaymentMethodsView

urlpatterns = [
    re_path(r'payment_sheet/?', PaymentSheetView.as_view()),
    re_path(r'get_payments_history/?', GetStripePaymentsView.as_view()),
    re_path(r'get_payments_methods/?', GetPaymentMethodsView.as_view()),
    re_path(r'detach_payment_method/?', DetachPaymentMethodsView.as_view()),
    re_path(r'attach_payment_method/?', AttachPaymentMethodsView.as_view()),
]
