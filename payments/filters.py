import django_filters
from django.forms import *
from django_filters.widgets import RangeWidget

from payments.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    """
    filter for product.
    """
    # status = django_filters.CharFilter(lookup_expr='icontains')  # filter if abc jacket and if user entered only abc then
    status = django_filters.ChoiceFilter(choices=Transaction.STATUS_IN_TRANSACTION_CHOICES, widget=Select(attrs={'class':'form-control'}))
    # status = django_filters.AllValuesFilter(choices=Transaction.STATUS_IN_TRANSACTION_CHOICES)
    # also show the result
    date = django_filters.DateFromToRangeFilter(
        label='By Date Range',
        widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date'}))  # From- To date filter

    class Meta:
        model = Transaction
        fields = {'status', 'date'}

