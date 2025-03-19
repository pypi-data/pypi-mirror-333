# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0
"""The command schemas describe the API for the command model.

These are used internally by the platform and users typically won't encounter them.
"""

from __future__ import annotations

from typing import Any, Literal, Optional, Union

import pydantic

from .base import DyffSchemaBaseModel, Null
from .platform import (
    DyffEntityType,
    EntityKindLiteral,
    FamilyMember,
    FamilyMembers,
    LabelKeyType,
    LabelValueType,
    SchemaVersion,
    Status,
    TagNameType,
    summary_maxlen,
    title_maxlen,
)

# ----------------------------------------------------------------------------


# mypy gets confused because 'dict' is the name of a method in DyffBaseModel
_ModelAsDict = dict[str, Any]


class _JsonMergePatchSemantics(DyffSchemaBaseModel):
    """Explicit None values will be output as json 'null', and fields that are not set
    explicitly are not output.

    In JSON Merge Patch terms, None means "delete this field", and not setting a value
    means "leave this field unchanged".
    """

    def dict(self, *, by_alias: bool = True, **kwargs) -> _ModelAsDict:
        return super().dict(
            by_alias=by_alias, exclude_unset=True, exclude_none=False, **kwargs
        )

    def json(self, *, by_alias: bool = True, **kwargs) -> str:
        return super().json(
            by_alias=by_alias, exclude_unset=True, exclude_none=False, **kwargs
        )


# class _NoneMeansUndefined(DyffSchemaBaseModel):
#     """Fields with the value None will not be emitted in the JSON output."""

#     # TODO: (DYFF-223) This should perhaps be the default for all schema
#     # objects.
#     def dict(self, *, exclude_none=True, **kwargs) -> _ModelAsDict:
#         return super().dict(exclude_none=True, **kwargs)

#     def json(self, *, exclude_none=True, **kwargs) -> str:
#         return super().json(exclude_none=True, **kwargs)


class EntityIdentifier(DyffSchemaBaseModel):
    """Identifies a single entity."""

    @staticmethod
    def of(entity: DyffEntityType) -> EntityIdentifier:
        """Create an identifier that identifies the given entity."""
        return EntityIdentifier(kind=entity.kind, id=entity.id)

    id: str = pydantic.Field(description="The .id of the entity.")
    kind: Optional[EntityKindLiteral] = pydantic.Field(
        default=None,
        description="The .kind of the entity. This is optional because"
        " sometimes you need to send a command without knowing the kind,"
        " but it should be set whenever possible.",
    )


class FamilyIdentifier(EntityIdentifier):
    """Identifies a single Family entity."""

    kind: Literal["Family"] = "Family"


class Command(SchemaVersion, DyffSchemaBaseModel):
    """Base class for Command messages.

    Commands define the API of the "command model" in our CQRS architecture.
    """

    command: Literal[
        "CreateEntity",
        "EditEntityDocumentation",
        "EditEntityLabels",
        "EditFamilyMembers",
        "ForgetEntity",
        "UpdateEntityStatus",
    ]


# ----------------------------------------------------------------------------


class CreateEntity(Command):
    """Create a new entity."""

    command: Literal["CreateEntity"] = "CreateEntity"

    data: DyffEntityType = pydantic.Field(
        description="The full spec of the entity to create."
    )


# ----------------------------------------------------------------------------


class EditEntityDocumentationPatch(_JsonMergePatchSemantics):
    """Same properties as DocumentationBase, but assigning None to a field is
    interpreted as a command to delete that field.

    Fields that are assigned explicitly remain unchanged.
    """

    title: Optional[Union[pydantic.constr(max_length=title_maxlen()), Null]] = (  # type: ignore
        pydantic.Field(
            default=None,
            description='A short plain string suitable as a title or "headline".'
            " Providing an explicit None value deletes the current value.",
        )
    )

    summary: Optional[Union[pydantic.constr(max_length=summary_maxlen()), Null]] = (  # type: ignore
        pydantic.Field(
            default=None,
            description="A brief summary, suitable for display in"
            " small UI elements. Providing an explicit None value deletes the"
            " current value.",
        )
    )

    fullPage: Optional[Union[str, Null]] = pydantic.Field(
        default=None,
        description="Long-form documentation. Interpreted as"
        " Markdown. There are no length constraints, but be reasonable."
        " Providing an explicit None value deletes the current value.",
    )


class EditEntityDocumentationAttributes(DyffSchemaBaseModel):
    """Attributes for the EditEntityDocumentation command."""

    documentation: EditEntityDocumentationPatch = pydantic.Field(
        description="Edits to make to the documentation."
    )


class EditEntityDocumentationData(EntityIdentifier):
    """Payload data for the EditEntityDocumentation command."""

    attributes: EditEntityDocumentationAttributes = pydantic.Field(
        description="The command attributes"
    )


class EditEntityDocumentation(Command):
    """Edit the documentation associated with an entity.

    Setting a documentation field to null/None deletes the corresponding value. To
    preserve the existing value, leave the field *unset*.
    """

    command: Literal["EditEntityDocumentation"] = "EditEntityDocumentation"

    data: EditEntityDocumentationData = pydantic.Field(description="The edit data.")


# ----------------------------------------------------------------------------


class EditEntityLabelsAttributes(_JsonMergePatchSemantics):
    """Attributes for the EditEntityLabels command."""

    labels: dict[LabelKeyType, Optional[Union[LabelValueType, Null]]] = pydantic.Field(
        default_factory=dict,
        description="A set of key-value labels for the resource."
        " Existing label keys that are not provided in the edit remain unchanged."
        " Providing an explicit None value deletes the corresponding key.",
    )


class EditEntityLabelsData(EntityIdentifier):
    """Payload data for the EditEntityLabels command."""

    attributes: EditEntityLabelsAttributes = pydantic.Field(
        description="The command attributes"
    )


class EditEntityLabels(Command):
    """Edit the labels associated with an entity.

    Setting a label field to null/None deletes the corresponding value. To preserve the
    existing value, leave the field *unset*.
    """

    command: Literal["EditEntityLabels"] = "EditEntityLabels"

    data: EditEntityLabelsData = pydantic.Field(description="The edit data.")


# ----------------------------------------------------------------------------


class EditFamilyMembersAttributes(_JsonMergePatchSemantics):
    """Attributes for the EditFamilyMembers command."""

    members: dict[TagNameType, Optional[Union[FamilyMember, Null]]] = pydantic.Field(
        description="Mapping of names to IDs of member resources.",
    )


class EditFamilyMembersData(FamilyMembers, FamilyIdentifier):
    """Payload data for the EditFamilyMembers command."""

    attributes: EditFamilyMembersAttributes = pydantic.Field(
        description="The command attributes"
    )


class EditFamilyMembers(Command):
    """Edit the labels associated with an entity.

    Setting a tag value to null/None deletes the corresponding value. To preserve the
    existing value, leave the field *unset*.
    """

    command: Literal["EditFamilyMembers"] = "EditFamilyMembers"

    data: EditFamilyMembersData = pydantic.Field(description="The edit data.")


# ----------------------------------------------------------------------------


class ForgetEntity(Command):
    """Forget (permanently delete) an entity."""

    command: Literal["ForgetEntity"] = "ForgetEntity"

    data: EntityIdentifier = pydantic.Field(description="The entity to forget.")


# ----------------------------------------------------------------------------


class UpdateEntityStatusAttributes(_JsonMergePatchSemantics):
    """Attributes for the UpdateEntityStatus command."""

    status: str = pydantic.Field(
        description=Status.__fields__["status"].field_info.description
    )

    reason: Optional[Union[str, Null]] = pydantic.Field(
        description=Status.__fields__["reason"].field_info.description
    )


class UpdateEntityStatusData(EntityIdentifier):
    """Payload data for the UpdateEntityStatus command."""

    attributes: UpdateEntityStatusAttributes = pydantic.Field(
        description="The command attributes"
    )


class UpdateEntityStatus(Command):
    """Update the status fields of an entity."""

    command: Literal["UpdateEntityStatus"] = "UpdateEntityStatus"

    data: UpdateEntityStatusData = pydantic.Field(description="The status update data.")


# ----------------------------------------------------------------------------


DyffCommandType = Union[
    CreateEntity,
    EditEntityDocumentation,
    EditEntityLabels,
    EditFamilyMembers,
    ForgetEntity,
    UpdateEntityStatus,
]


__all__ = [
    "Command",
    "CreateEntity",
    "DyffCommandType",
    "EditEntityDocumentation",
    "EditEntityDocumentationAttributes",
    "EditEntityDocumentationData",
    "EditEntityDocumentationPatch",
    "EditEntityLabels",
    "EditEntityLabelsAttributes",
    "EditEntityLabelsData",
    "EditFamilyMembers",
    "EditFamilyMembersAttributes",
    "EditFamilyMembersData",
    "EntityIdentifier",
    "FamilyIdentifier",
    "ForgetEntity",
    "UpdateEntityStatus",
    "UpdateEntityStatusAttributes",
    "UpdateEntityStatusData",
]
