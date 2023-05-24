from enum import unique
import json
from typing import final

from django.db.models.query_utils import Q
import graphene
from graphql import GraphQLError
from starter.models import User
from starter.gqTypes import UserInput, UserType
from graphql_jwt.decorators import login_required, user_passes_test
from .gqSubscriptions import NotifyUser 
from starter.authorization import CREATE_METHOD, UPDATE_METHOD, DELETE_METHOD, is_admin_user
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache


class CreateUser(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new User"

    class Arguments:
        user = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info, input=None):
        ok = True
        error = ""

        searchField = input.first_name + \
            input.last_name if input.first_name and input.last_name else ""
        searchField += input.title if input.title is not None else ""
        searchField += input.bio if input.bio is not None else ""
        searchField = searchField.lower()

        user_instance = User(user_id=input.user_id, title=input.title, bio=input.bio,
                             institution_id=input.institution_id, searchField=searchField)
        user_instance.save()

        payload = {"user": user_instance,
                   "method": CREATE_METHOD}
        NotifyUser.broadcast(
            payload=payload)
        return CreateUser(ok=ok, user=user_instance)


class UpdateUser(graphene.Mutation):
    class Meta:
        description = "Mutation to update a User"

    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info, input=None):
        ok = False
        current_user = info.context.user
        user = User.objects.get(pk=current_user.id, active=True)
        user_instance = user
        if user_instance:
            ok = True
            user_instance.first_name = input.first_name if input.first_name is not None else user.first_name
            user_instance.last_name = input.last_name if input.last_name is not None else user.last_name
            user_instance.name = user_instance.first_name + ' ' + user_instance.last_name if user_instance.first_name is not None and user_instance.last_name is not None else ""
            user_instance.avatar = input.avatar if input.avatar is not None else user.avatar
            user_instance.role_id = input.role_id if input.role_id is not None else user.role_id
            user_instance.title = input.title if input.title is not None else user.title
            user_instance.bio = input.bio if input.bio is not None else user.bio

            searchField = user_instance.first_name if user_instance.first_name is not None else ""
            searchField += user_instance.last_name if user_instance.last_name is not None else ""
            searchField += user_instance.title if user_instance.title is not None else ""
            searchField += user_instance.bio if user_instance.bio is not None else ""
            searchField += user_instance.membership_status if user_instance.membership_status is not None else ""
            user_instance.searchField = searchField.lower()

            user_instance.save()
        
            users_modified() # Invalidating users cache

            payload = {"user": user_instance,
                       "method": UPDATE_METHOD}
            NotifyUser.broadcast(
                payload=payload)

            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class DeleteUser(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a User as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info, id, input=None):
        ok = False
        user = User.objects.get(pk=id, active=True)
        user_instance = user
        if user_instance:
            ok = True
            user_instance.active = False

            user_instance.save()

            users_modified() # Invalidating users cache

            payload = {"user": user_instance,
                       "method": DELETE_METHOD}
            NotifyUser.broadcast(
                payload=payload)
            return DeleteUser(ok=ok, user=user_instance)
        return DeleteUser(ok=ok, user=None)

class ClearServerCache(graphene.Mutation):
    class Meta:
        description = "Clear serverside cache"

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    @user_passes_test(lambda user: is_admin_user(user))
    def mutate(root, info):
        cache.clear()
        ok = True
        return ClearServerCache(ok=ok)

class Mutation(graphene.ObjectType):

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    # Admin mutations
    clear_server_cache = ClearServerCache.Field()