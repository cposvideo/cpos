class AccessDenied(Exception): pass

def require_role(role, allowed):
    if role not in allowed: raise AccessDenied()
