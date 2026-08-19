##   When a user logs out, their token can be added to this set, and any subsequent requests with that token will be denied.
BLACKLISTED_TOKENS = set()