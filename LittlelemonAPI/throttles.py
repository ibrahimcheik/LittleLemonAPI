from rest_framework.throttling import UserRateThrottle

class TenCallsPeerMinute(UserRateThrottle):
    
    scope = 'ten'