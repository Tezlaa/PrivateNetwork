import time
import functools

from django.db import connection, reset_queries

from rest_framework.exceptions import ValidationError


def api_validation_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise ValidationError(e)
    return wrapper


def banchmark_queries(func):
    GREEN   = '\033[0;32m'
    YELLOW  = '\033[0;33m'
    NOCOLOR = '\033[0m'

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
    
        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)
        count_queries = (end_queries - start_queries)
        
        if count_queries == 0:
            return result

        print(GREEN, f'\nFunction : {func.__name__}')
        print(f'Number of Queries : {count_queries}')
        print(f'Finished in : {(end - start):.5f}s')
        
        print('\nRaw SQL:\n', NOCOLOR)
        for query in connection.queries:
            print(f'{YELLOW}{query.get("sql")}{NOCOLOR}', end='\n\n')
        
        return result

    return inner_func