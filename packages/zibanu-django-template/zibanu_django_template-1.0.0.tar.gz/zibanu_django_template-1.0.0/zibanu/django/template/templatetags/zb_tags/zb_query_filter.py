# -*- coding: utf-8 -*-
# ****************************************************************
# IDE:          PyCharm
# Developed by: "Jhony Alexander Gonzalez Córdoba"
# Date:         7/03/2025 3:44 p. m.
# Project:      zibanu-django
# Module Name:  zb_query_filter
# Description:  
# ****************************************************************
from django.db.models import QuerySet


def zb_query_filter(queryset: QuerySet, **kwargs):
    """
    Filter a queryset
    :param queryset:  type argument queryset.
    :param kwargs: Arguments for which the queryset will be filtered.
    :return: queryset.
    """
    try:
        return queryset.filter(**kwargs)
    except AttributeError:
        return None
