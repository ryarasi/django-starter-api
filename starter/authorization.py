from django.db.models.query_utils import Q
from graphql import GraphQLError
from django.conf import settings
from starter.models import User

SORT_BY_OPTIONS = {'NEW': 'NEW', 'TOP':'TOP'}

UPDATE_METHOD = "UPDATE"
DELETE_METHOD = "DELETE"
CREATE_METHOD = "CREATE"
# whever changes are made below to the User role names, Resources and actions
# need to be reflected in the UI too.

USER_ROLES_NAMES = {
    "SUPER_ADMIN": "Super Admin",
}


RESOURCES = {
    "RESOURCE1": "RESOURCE1",
    "RESOURCE2": "RESOURCE2",
    "RESOURCE3": "RESOURCE3",
}

ACTIONS = {
    "LIST": "LIST",
    "GET": "GET",
    "CREATE": "CREATE",
    "UPDATE": "UPDATE",
    "DELETE": "DELETE",
}


def has_access(user=None, resource=None, action=None, silent=True):
    result = False
    if user:
        user_permissions = user.role.permissions
        if user_permissions and resource and action:
            result = user_permissions[resource][action]

    if result is False and silent is False:
        raise GraphQLError("You are not authorized to access this resource")
    return result

def is_admin_user(user):
    admin_user = False

    try:
        if not user.is_anonymous:
            current_user_role_name = user.role.name
            admin_user = current_user_role_name == USER_ROLES_NAMES["SUPER_ADMIN"]
    except:
        admin_user = False
        pass

    return admin_user

def redact_user(root, info, user):
    current_user = info.context.user
    redact = True

    if not current_user.is_anonymous:
        admin_user = is_admin_user(current_user)
        if admin_user:
            redact = False # We never redact for the super admin user
        if current_user.institution:
            if user.institution_id == current_user.institution.id:
                redact = False # We redact the user"s info if the current user is not of the same institution
            
    if redact == True:
        user.avatar = settings.DEFAULT_AVATARS["USER"]

    return user

def is_content_locked(user, content):
    locked = True
    # Checking if the user is the author of the content
    if content.author.id == user.id:
        # If yes, we mark it as unlocked
        locked = False    
    else:
        locked = True

    return locked


def rows_accessible(user, RESOURCE_TYPE, options={}):
    try:
        subscription_method = options['subscription_method']
    except:
        subscription_method = None

    if RESOURCE_TYPE == RESOURCES["RESOURCE1"]:
        try:
            content_id = user.content.id
        except:
            pass

        admin_user = is_admin_user(user)
        
        all_institutions = True if options["all_institutions"] == True else False

        if admin_user or all_institutions == True:
            # if the user is super user then they see users from all institutions
            qs = User.objects.all().order_by("-id")
        else:
            # If the user is not a super user, we filter the users by institution
            qs = User.objects.all().filter(content_id=content_id).order_by("-id")

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

