# Generated by ariadne-codegen
# Source: operations.graphql

from stigg._vendors.pydantic import Field

from .base_model import BaseModel
from .fragments import SubscriptionPreviewV2Fragment


class PreviewSubscription(BaseModel):
    preview_subscription: "PreviewSubscriptionPreviewSubscription" = Field(
        alias="previewSubscription"
    )


class PreviewSubscriptionPreviewSubscription(SubscriptionPreviewV2Fragment):
    pass


PreviewSubscription.model_rebuild()
