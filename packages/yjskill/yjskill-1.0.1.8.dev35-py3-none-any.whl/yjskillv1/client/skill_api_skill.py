# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""

import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

skill_name_regex = re.compile(
    r"^workspaces/(?P<workspace_id>.+?)/skills/(?P<local_name>.+?)$"
)


class Skill(BaseModel):
    """
    Skill model.

    """

    name: str = Field(alias="name")
    local_name: str = Field(alias="localName")
    display_name: str = Field(alias="displayName")
    description: str = Field(alias="description")
    workspace_id: str = Field(alias="workspaceID")

    kind: str = Field(alias="kind")
    create_kind: str = Field(alias="createKind")
    from_kind: str = Field(alias="fromKind")

    tags: Optional[dict] = Field(default=None, alias="tags")
    image_uri: Optional[str] = Field(default=None, alias="imageURI")
    accelerators: Optional[list] = Field(default=None, alias="accelerators")
    model_type: Optional[str] = Field(default=None, alias="modelType")
    status: str = Field(alias="status")

    graph: Optional[dict] = Field(default=None, alias="graph")
    debug: Optional[dict] = Field(default=None, alias="debug")

    artifact_count: int = Field(alias="artifactCount")
    released_version: int = Field(alias="releasedVersion")

    org_id: str = Field(alias="orgID")
    user_id: str = Field(alias="userID")

    default_level: int = Field(alias="defaultLevel")
    alarm_configs: Optional[list] = Field(default=None, alias="alarmConfigs")

    create_at: Optional[datetime] = Field(default=None, alias="createAt")
    update_at: Optional[datetime] = Field(default=None, alias="updateAt")


class SkillName(BaseModel):
    """
    Skill name, e.g. workspaces/:ws/skills/:localName
    """

    workspace_id: str
    local_name: str


def parse_skill_name(name: str) -> Optional[SkillName]:
    """
    Parse skill name to SkillName object.

    Args:
        name: str, skill name, e.g. workspaces/:ws/skills/:localName
    Returns:
        SkillName, 解析成功返回SkillName对象，否则返回None
    """

    match = skill_name_regex.match(name)
    if match:
        return SkillName(**match.groupdict())
    return None


class GetSkillRequest(BaseModel):
    """
    Request for get skill.
    """

    workspace_id: str = Field(alias="workspaceID")
    local_name: str = Field(alias="localName")
    version: str = Field(alias="version")


class CreateSkillRequest(BaseModel):
    """
    Request for create skill.
    """

    class Config(ConfigDict):
        """
        Configuration for the request model.
        """

        arbitrary_types_allowed = True

    workspace_id: str = Field(alias="workspaceID")
    local_name: str = Field(alias="localName")
    display_name: str = Field(alias="displayName")
    description: Optional[str] = Field(default=None, alias="description")
    kind: str = Field(alias="kind")
    crerate_kind: str = Field(alias="createKind")
    from_kind: str = Field(alias="fromKind")
    tags: Optional[dict] = Field(default=None, alias="tags")
    graph: Optional[dict] = Field(default=None, alias="graph")
    image_uri: Optional[str] = Field(default=None, alias="imageURI")
    default_level: int = Field(default=4, alias="defaultLevel")
    alarm_configs: Optional[list] = Field(default=None, alias="alarmConfigs")
