import graphene
from graphene.types import generic
from graphene_django.types import DjangoObjectType
from starter.models import User, UserRole


##############
# Query Types
##############


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserRoleType(DjangoObjectType):
    class Meta:
        model = UserRole


##############
# Mutation Types
##############

class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    nick_name = graphene.String()
    email = graphene.String()
    avatar = graphene.String()
    title = graphene.String()
    bio = graphene.String()
    role_id = graphene.ID(name="role")


class UserRoleInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    priority = graphene.Int(required=True)
    permissions = generic.GenericScalar()
