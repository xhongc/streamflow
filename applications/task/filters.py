import django_filters as filters


class VarTableFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")


class TaskFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    process__name = filters.CharFilter(lookup_expr="icontains")
    run_type = filters.CharFilter(lookup_expr="exact")
