import hashlib
import json
import os
import time

def cache(function):
    """
    Simple decorator function for caching.

    Usage:
    1 import cache from cache
    2
    3 @cache
    4 def example(self, text):
    5 	return text * 2
    In this example the result of the example function is cached.

    Current limitations:
    -No cache size limit
    -Not thread safe
    -The first parameter is ignored and not used to create the hash
    -Arguments can't be a reference to other data and need to be JSON serializable
    -Two functions with the same name and parameter data will use the same cache
    -Normal limitations of caches
    """
    def wrapper(*args, **kwargs):
        # Settings
        cache_folder = 'EuretosCache/'
        expire_time = 7 * 24 * 60 * 60

        # Create cache folder if it doesn't exist
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)

        # Remove expired cache items
        for filename in os.listdir(cache_folder):
            mtime = os.path.getmtime(cache_folder + filename)
            if time.time() - mtime > expire_time:
                os.remove(cache_folder + filename)

        # Make hash from input arguments and function name
        call_string = json.dumps([function.__name__,args[1:], kwargs])
        call_hash = hashlib.sha256(call_string.encode()).hexdigest()

        # Read cache if it exists and can be correctly read
        # If not then execute function and write cache
        try:
            with open(cache_folder + call_hash, 'r') as f:
                print('Reading cache (' + function.__name__ + ')')
                return json.load(f)
        except:
            with open(cache_folder + call_hash, 'w') as f:
                print('Writing cache (' + function.__name__ + ')')
                output = function(*args, **kwargs)
                json.dump(output, f)
                return output

    return wrapper
