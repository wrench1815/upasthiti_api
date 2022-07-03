from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    '''
        Custom paginator based on PageNumberPagination

        parameters: 
            - page: page number
            - size: number of items per page (not used)

        returns:
            - paginated data

        example response:
            {
                "count": 0,
                "items": 0,
                "next": true,
                "previous": true,
                "current": 0,
                "results": [
                    ...
                ]
            }
    '''
    page_size = 10
    max_page_size = 1000

    # page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({
            # return count of all pages
            'count': self.page.paginator.num_pages,

            # return counts of all items
            'items': self.page.paginator.count,

            # return true if there is a next page
            'next': self.page.has_next(),

            # returns true if there is a previous page
            'previous': self.page.has_previous(),

            # return current page number
            'current': self.page.number,

            # data
            'results': data
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'description': 'Total number of pages'
                },
                'items': {
                    'type': 'integer',
                    'description': 'Total number of Items',
                },
                'next': {
                    'type': 'boolean',
                    'description': 'True if there is a next page'
                },
                'previous': {
                    'type': 'boolean',
                    'description': 'True if there is a previous page'
                },
                'current': {
                    'type': 'integer',
                    'description': 'Current page number'
                },
                'results': schema
            }
        }
