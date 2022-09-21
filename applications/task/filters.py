import django_filters as filters


class VarTableFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
