import starter.gqSchema
import starter.gqTesting
import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from channels.auth import get_user
import channels_graphql_ws
from django.conf import settings

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()

testQueries = test=starter.gqTesting.Query if settings.ENABLED_AUTOMATED_TESTING else starter.gqTesting.EmptyQuery 


class Query(starter.gqSchema.Query, testQueries, UserQuery, MeQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(starter.gqSchema.Mutation, AuthMutation, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Subscription(starter.gqSchema.Subscription):
    pass



schema = graphene.Schema(query=Query, mutation=Mutation,
                         subscription=Subscription)


def subscription_middleware(next_middleware, root, info, *args, **kwds):
    if(info.operation.name is not None and info.operation.name.value != "IntrospectionQuery"):
        print("Subscription Middleware report")
        print(" user :", info.context.user)
        print(" operation :", info.operation.operation)
        print(" resource :", info.operation.name.value)

    return next_middleware(root, info, *args, **kwds)


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    async def on_connect(self, payload):
        self.scope["user"] = self.scope["session"]
        self.user = self.scope["user"]

    schema = schema
    middleware = [subscription_middleware]
