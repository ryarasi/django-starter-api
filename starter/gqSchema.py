import graphene
from .gqQueries import Query
from .gqMutations import Mutation
from .gqSubscriptions import Subscription


schema = graphene.Schema(query=Query, mutation=Mutation,
                         subscription=Subscription)
