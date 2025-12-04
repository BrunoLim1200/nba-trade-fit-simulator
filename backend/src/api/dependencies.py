from fastapi import Depends

def get_query_param(param: str):
    return param