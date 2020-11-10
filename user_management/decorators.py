from django.contrib.auth.decorators import user_passes_test


def user_required(function=None, login_url='/forbidden'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_authenticated,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def vendor_required(function=None, login_url='/forbidden'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_vendor and u.is_authenticated,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_required(function=None, login_url='/forbidden'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_admin and u.is_authenticated,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
