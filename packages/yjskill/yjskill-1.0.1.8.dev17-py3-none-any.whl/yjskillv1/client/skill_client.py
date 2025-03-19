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

    def export_skill(self, skill_name: str, output_artifact_path: str):
        """
        export skill template
        :return:
        """

        try:
            model_artifact_names = []
            logger.info("ExportSkill start ")
            artifact = parse_artifact_name(skill_name)
            skill_name = parse_skill_name(artifact.object_name)
            skill = self.get_skill(req=GetSkillRequest(
                workspaceID=skill_name.workspace_id,
                localName=skill_name.local_name,
                version=artifact.version))

            if skill.graph:
                graph_content = GraphContent(nodes=skill.graph["nodes"], )
                nodes = graph_content.get_nodes("ObjectDetectOperator")
                logger.info(f"ExportSkill get ObjectDetectOperator nodes {str(nodes)}")

                for node in nodes:
                    model = node.get_property("modelName")
                    if model:
                        model_artifact_names.append(model.value)
            else:
                raise ValueError(f"Invalid skill graph content. job: {self.config.job_name}, "
                                 f"skill_name:{skill_name},"
                                 f"skill: {skill}")


            # 确保目录存在
            if not os.path.exists(os.path.join(output_artifact_path)):
                os.makedirs(os.path.join(output_artifact_path))
            skill_file_path = os.path.join(output_artifact_path, 'skill.json')
            models_artifact_path = os.path.join(output_artifact_path, 'artifact.txt')

            # 将 skill 写入 skill.json
            with open(skill_file_path, 'w', encoding='utf-8') as file:
                file.write(skill.raw_data)
            logger.info(f"ExportSkill write skill json {str(skill)}")

            # 将模型名称写入 artifact.txt
            model_artifact_string = ",".join(model_artifact_names)
            with open(models_artifact_path, 'w', encoding='utf-8') as file:
                file.write(model_artifact_string)

            logger.info(f"ExportSkill write model names {str(model_artifact_string)}")

            return skill
        except Exception as e:
            logger.error(f"Failed to export skill: {str(e)}")
            return
