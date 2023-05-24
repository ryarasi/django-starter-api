import channels_graphql_ws
import graphene
from graphql_jwt.decorators import login_required
from .gqTypes import UserType, UserRoleType
from starter.authorization import is_record_accessible, RESOURCES

class NotifyUser(channels_graphql_ws.Subscription):
    user = graphene.Field(UserType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if is_record_accessible(info.context.user, RESOURCES['MEMBER'],payload['user'], payload['method']):
            return NotifyUser(user=payload["user"], method=payload["method"])
        else:
            return None        


class NotifyUserRole(channels_graphql_ws.Subscription):
    user_role = graphene.Field(UserRoleType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if is_record_accessible(info.context.user, RESOURCES['USER_ROLE'],payload['user_role'], payload['method']):
            return NotifyUserRole(user_role=payload["user_role"], method=payload["method"])
        else:
            return None


class Subscription(graphene.ObjectType):
    notify_user = NotifyUser.Field()
    notify_user_role = NotifyUserRole.Field()