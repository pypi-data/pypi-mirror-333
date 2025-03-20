from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 20  # Maximum allowed page size
