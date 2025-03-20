#  Copyright (c) ZenML GmbH 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""RBAC model classes."""

from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
)

from zenml.utils.enum_utils import StrEnum


class Action(StrEnum):
    """RBAC actions."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    READ_SECRET_VALUE = "read_secret_value"
    PRUNE = "prune"

    # Service connectors
    CLIENT = "client"

    # Models
    PROMOTE = "promote"

    # Secrets
    BACKUP_RESTORE = "backup_restore"

    SHARE = "share"


class ResourceType(StrEnum):
    """Resource types of the server API."""

    ACTION = "action"
    ARTIFACT = "artifact"
    ARTIFACT_VERSION = "artifact_version"
    CODE_REPOSITORY = "code_repository"
    EVENT_SOURCE = "event_source"
    FLAVOR = "flavor"
    MODEL = "model"
    MODEL_VERSION = "model_version"
    PIPELINE = "pipeline"
    PIPELINE_RUN = "pipeline_run"
    PIPELINE_DEPLOYMENT = "pipeline_deployment"
    PIPELINE_BUILD = "pipeline_build"
    RUN_TEMPLATE = "run_template"
    SERVICE = "service"
    RUN_METADATA = "run_metadata"
    SECRET = "secret"
    SERVICE_ACCOUNT = "service_account"
    SERVICE_CONNECTOR = "service_connector"
    STACK = "stack"
    STACK_COMPONENT = "stack_component"
    TAG = "tag"
    TRIGGER = "trigger"
    TRIGGER_EXECUTION = "trigger_execution"
    WORKSPACE = "workspace"
    # Deactivated for now
    # USER = "user"

    def is_workspace_scoped(self) -> bool:
        """Check if a resource type is workspace scoped.

        Returns:
            Whether the resource type is workspace scoped.
        """
        return self not in [
            self.FLAVOR,
            self.SECRET,
            self.SERVICE_CONNECTOR,
            self.STACK,
            self.STACK_COMPONENT,
            self.TAG,
            self.SERVICE_ACCOUNT,
            self.WORKSPACE,
            # Deactivated for now
            # self.USER,
        ]


class Resource(BaseModel):
    """RBAC resource model."""

    type: str
    id: Optional[UUID] = None
    workspace_id: Optional[UUID] = None

    def __str__(self) -> str:
        """Convert to a string.

        Returns:
            Resource string representation.
        """
        workspace_id = self.workspace_id
        if self.type == ResourceType.WORKSPACE and self.id:
            # TODO: For now, we duplicate the workspace ID in the string
            # representation when describing a workspace instance, because
            # this is what is expected by the RBAC implementation.
            workspace_id = self.id

        if workspace_id:
            representation = f"{workspace_id}:"
        else:
            representation = ""
        representation += self.type
        if self.id:
            representation += f"/{self.id}"

        return representation

    @model_validator(mode="after")
    def validate_workspace_id(self) -> "Resource":
        """Validate that workspace_id is set in combination with workspace-scoped resource types.

        Raises:
            ValueError: If workspace_id is not set for a workspace-scoped
                resource or set for an unscoped resource.

        Returns:
            The validated resource.
        """
        resource_type = ResourceType(self.type)

        if resource_type.is_workspace_scoped() and not self.workspace_id:
            raise ValueError(
                "workspace_id must be set for workspace-scoped resource type "
                f"'{self.type}'"
            )

        if not resource_type.is_workspace_scoped() and self.workspace_id:
            raise ValueError(
                "workspace_id must not be set for global resource type "
                f"'{self.type}'"
            )

        return self

    model_config = ConfigDict(frozen=True)
