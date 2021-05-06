
def cached(_func=None, capacity: int = 1000):
    def cache_decorator(func):
        _cache_capacity = capacity
        _cache = dict()
        _cache_used = 0
        def cached_func(*args, **kwargs):
            cache_key = args + tuple(kwargs.items())
            if cache_key in cached_func._cache:
                print("fetchin")
                return cached_func._cache[cache_key]
            else:
                print("first pull")
                result = func(*args, **kwargs)
                cached_func._cache_used += 1
                cached_func._cache.update({cache_key: result})
            print(cache_key)
        cached_func.__setattr__("_capacity", _cache_capacity)
        cached_func.__setattr__("_cache", _cache)
        cached_func.__setattr__("_cache_used", _cache_used)
        return cached_func
    if _func is None:
        return cache_decorator
    else:
        return cache_decorator(_func)

@cached
def print_m(name, pass_: object):
    return f"{name} : {pass_}"


@cached
def s(a,b):
    return a + b

print(s(1, 2))
print(s(1, b=2))
print(s(a=1, b=2))
print(s(a=1, b=3))