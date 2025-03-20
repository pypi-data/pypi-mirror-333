# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
import json
import os

import bcelogger as logger
from baidubce.http import http_methods
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from pygraphv1.client.graph_api_graph import GraphContent
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name

from .skill_api_skill import GetSkillRequest, parse_skill_name, Skill


class SkillClient(BceInternalClient):
    """
    A client class for interacting with the skill service. 
    """

    def get_skill(
            self,
            req: GetSkillRequest):
        """
        Get a skill.

        Args:
            workspace_id (str): 工作区 id，例如："ws01"
            skill_name (str): 技能系统名称，例如："skill01"
            version (str): 技能版本号，例如："1"
        Returns:
             HTTP request response
        """

        return self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                "/v1/workspaces/" + req.workspace_id + "/skills/" + req.local_name, encoding="utf-8"
            ),
            params=req.model_dump(by_alias=True),
        )

    def export_skill(self, skill_name: str, output_uri: str) -> Skill:
        """Export skill template """
        try:
            logger.info("Exporting skill: %s to %s", skill_name, output_uri)
            artifact = parse_artifact_name(skill_name)
            skill_name_obj = parse_skill_name(artifact.object_name)

            # 获取技能详情
            skill = self.get_skill(GetSkillRequest(
                workspaceID=skill_name_obj.workspace_id,
                localName=skill_name_obj.local_name,
                version=artifact.version
            ))

            # 处理技能图
            if not skill.graph:
                raise ValueError(f"Invalid skill graph - skill: {skill_name}")

            # 写入技能元数据
            skill_path = os.path.join(output_uri, 'skill.json')
            # 创建输出目录
            if not os.path.exists(os.path.join(output_uri)):
                os.makedirs(os.path.join(output_uri))

            with open(skill_path, 'w', encoding='utf-8') as f:
                f.write(skill.raw_data)
            logger.debug("Skill metadata saved to: %s", skill_path)

            return skill

        except Exception as e:
            logger.error("Skill export failed: %s [job: %s]",
                         str(e), getattr(self.config, 'job_name', 'unknown'))
            raise  # 重新抛出异常保持堆栈跟踪