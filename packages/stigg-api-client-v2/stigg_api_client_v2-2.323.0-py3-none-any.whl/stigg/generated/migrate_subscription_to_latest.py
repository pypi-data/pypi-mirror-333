# Generated by ariadne-codegen
# Source: operations.graphql

from stigg._vendors.pydantic import Field

from .base_model import BaseModel


class MigrateSubscriptionToLatest(BaseModel):
    migrate_subscription_to_latest: "MigrateSubscriptionToLatestMigrateSubscriptionToLatest" = Field(
        alias="migrateSubscriptionToLatest"
    )


class MigrateSubscriptionToLatestMigrateSubscriptionToLatest(BaseModel):
    subscription_id: str = Field(alias="subscriptionId")


MigrateSubscriptionToLatest.model_rebuild()
