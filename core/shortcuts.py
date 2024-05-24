from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError as DRFValidationError

from core.exceptions import BadRequestError


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """

    if hasattr(queryset, "_default_manager"):
        queryset = queryset._default_manager.all()

    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except Http404:
        raise NotFound("%s not found" % queryset.model._meta.object_name)
    except (TypeError, ValueError, DRFValidationError, DjangoValidationError):
        raise BadRequestError("Invalid pk type was passed")
