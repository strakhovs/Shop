from rest_framework import pagination
from rest_framework.response import Response


class CustomPaginator(pagination.PageNumberPagination):
    page_size = 6
    page_query_param = 'currentPage'

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages,
        })
