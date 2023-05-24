
from tkinter import N
from django.core.cache import cache

separator = '-'
limit_label = 'limit'
offset_label = 'offset'
searchField_label = 'searchField'
status_label = 'status'

CACHE_ENTITIES = {
    'USERS': 'USERS',
    'RESOURCE1': 'RESOURCE1',
    'RESOURCE2': 'RESOURCE2',
    'RESOURCE3': 'RESOURCE3',
}


def sanitize_cache_key(key):
    return key.replace(" ", separator)

def generate_content_cache_key(entity, searchField, limit, offset):
    cache_key = str(entity) + separator + searchField_label + str(searchField) + \
        separator + limit_label + \
        str(limit) + separator + offset_label + str(offset)
    return sanitize_cache_key(cache_key)


def fetch_cache(entity, key):
    print('Fetching cache => ', entity, ' key => ', key)
    cached_response = None
    cached_item = cache.get(entity)
    if cached_item:
        try:
            cached_response = cached_item[key]
        except:
            pass
    print('cached response => ', cached_response)
    return cached_response

# Set cache method


def set_cache(entity, key, response):
    print('Setting cache => ', entity, 'key => ',
          key, ' response => ', response)
    cached_entity = cache.get(entity)
    if not cached_entity:
        cached_entity = {}
    cached_entity[key] = response
    cache.set(entity, cached_entity, timeout=None)


# Cache Invalidation Methods

def invalidate_cache(entity):
    cache.delete(entity)


def invalidate_cache_with_keyword(entity, keyword):
    cached_entity = cache.get(entity)
    for item in cached_entity.keys():
        if keyword in item:
            del cached_entity[item]
    cache.set(entity, cached_entity)


def invalidate_user_specific_cache(entity, user):
    cached_entity = cache.get(entity)
    for item in cached_entity.keys():
        if item.startswith(str(user.id)):
            del cached_entity[item]
    cache.set(entity, cached_entity)


# Specific methods to invalidate certain entities

def content_modified():
    invalidate_cache(CACHE_ENTITIES['RESOURCE1'])
    invalidate_cache(CACHE_ENTITIES['RESOURCE2'])

