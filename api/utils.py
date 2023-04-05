from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"
    max_page_size = 2

def paginate(query_set, request, Serializer):
    paginator=CustomPagination()
    pagined_queryset= paginator.paginate_queryset(query_set, request)
    serializer=Serializer(pagined_queryset, many=True, context={"request":request})

    return {
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results':serializer.data
    }
