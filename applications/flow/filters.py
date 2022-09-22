import django_filters as filters


class NodeTemplateFilter(filters.FilterSet):
    template_type = filters.CharFilter(lookup_expr="iexact")


class ProcessRunFilter(filters.FilterSet):
    process_id = filters.CharFilter(lookup_expr="exact")


class SubProcessRunFilter(filters.FilterSet):
    process_run = filters.CharFilter(lookup_expr="exact")
