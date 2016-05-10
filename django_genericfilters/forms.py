# -*- coding: utf-8 -*-
"""
django generic filters implement a set of mixin to work with ordered,
paginated and filtered queryset.

"""
from django import forms
from django.utils.translation import ugettext_lazy as _

from .fields import *  # NOQA


class QueryFormMixin(object):
    """
    Mixin implementing a query parameters for filtering results.
    """
    def __init__(self, *args, **kwargs):
        super(QueryFormMixin, self).__init__(*args, **kwargs)
        self.fields['query'] = forms.CharField(required=False,
                                               widget=forms.HiddenInput)


class OrderFormMixin(object):
    """
    Mixin implementing order_by and order_by_reverse for your filtered
    results

    A Form accept as argument in the __init__:
        def __init__(self, data=None, files=None, auto_id='id_%s',
        prefix=None, initial=None, error_class=ErrorList,
        label_suffix=None, empty_permitted=False):
    """
    _FORM_KWARGS = ['data', 'files', 'auto_id', 'prefix',
                    'initial', 'error_class', 'label_suffix',
                    'empty_permitted', ]


    def __init__(self, *args, **kwargs):
        # we can override the .get_form_kwargs() in our views
        # to add for instance the ``request``, and not break
        # this code
        super_kwargs = kwargs.copy()
        for key_to_delete in super_kwargs.keys():
            if key_to_delete not in OrderFormMixin._FORM_KWARGS:
                super_kwargs.pop(key_to_delete)

        super(OrderFormMixin, self).__init__(*args, **super_kwargs)

        self.fields['order_by'] = forms.ChoiceField(
            label=_('order by'),
            required=False,
            widget=forms.HiddenInput,
            choices=self.get_order_by_choices())
        self.fields['order_reverse'] = forms.BooleanField(
            label=_('order by'),
            required=False,
            widget=forms.HiddenInput)

    def clean_order_by(self):
        if self['order_by'].html_name not in self.data:
            return self.initial.get(self['order_by'].html_name,
                                    self.fields['order_by'].initial)
        return self.cleaned_data['order_by']

    def get_order_by_choices(self):
        """
        If you use OrderFormMixin, this method must be implemented in
        your form.

        get_order_by choices should return a list of tuples. Those
        will be used as choices for the order_by field.

        Example:

        .. code-block:: python

            def get_order_by_choices(self):
                return [("1", "choice1"),
                        ("2", "choice2")]
        """

        raise NotImplementedError(
            _("Don't forget to implements get_order_by_choices"))


class FilteredForm(OrderFormMixin, QueryFormMixin, forms.Form):
    """
    FilteredForm is like a classic forms. But It use OrderFormMixin,
    PaginationFormMixin and QueryFormMixin
    """
    pass
