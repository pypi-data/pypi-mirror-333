# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authors: duanshichao(duanshichao@baidu.com)
Date: 2025/03/09
"""
import json
import os
import traceback
from argparse import ArgumentParser

import bcelogger as logger
from jobv1.client.job_api_event import EventKind
from jobv1.client.job_api_job import parse_job_name, GetJobRequest, UpdateJobRequest
from jobv1.client.job_api_metric import MetricLocalName, MetricKind, CounterKind, DataType
from jobv1.client.job_client import (
    JobClient
)
from jobv1.tracker.tracker import Tracker
from pygraphv1.client.graph_api_graph import GraphContent
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.filesystem import upload_by_filesystem
from yjskillv1.client.skill_api_skill import parse_skill_name, Skill
from yjskillv1.client.skill_client import SkillClient

EXPORT_SKILL = "Export/Skill"
EXPORT_SKILL_TASK = "export-skill"
DATA_TYPE_SKILL_TEMPLATE = "SkillTemplate"


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--skill_name", required=True, type=str, default="")
    parser.add_argument("--data_type", required=True, type=str, default="")

    args, _ = parser.parse_known_args()
    return args


def run():
    """
    Export skill.
    """
    global tracker

    try:
        logger.info("Starting export skill")
        args = parse_args()
        skill_version_name = args.skill_name
        artifact_name = parse_artifact_name(skill_version_name)
        skill_name = parse_skill_name(artifact_name.object_name)
        data_type = args.data_type

        org_id = os.getenv("ORG_ID", "")
        user_id = os.getenv("USER_ID", "")
        job_name = parse_job_name(os.getenv("JOB_NAME", ""))

        windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
        vistudio_endpoint = os.getenv("VISTUDIO_ENDPOINT", "")
        output_artifact_path = os.getenv(
            "PF_OUTPUT_ARTIFACT_OUTPUT_URI", "./output_uri"
        )

        job_client = JobClient(endpoint=windmill_endpoint, context={"OrgID": org_id, "UserID": user_id}, )
        windmill_client = WindmillClient(endpoint=windmill_endpoint, context={"OrgID": org_id, "UserID": user_id}, )
        skill_client = SkillClient(endpoint=vistudio_endpoint, context={"OrgID": org_id, "UserID": user_id})

        tracker = Tracker(
            client=job_client,
            workspace_id=job_name.workspace_id,
            job_name=job_name.local_name,
            task_name=""
        )

        # 上报job总数
        tracker.log_metric(
            local_name=MetricLocalName.Total,
            kind=MetricKind.Counter,
            counter_kind=CounterKind.Cumulative,
            data_type=DataType.Int,
            value=[str(1)])

        # 上报task总数
        tracker.log_metric(
            local_name=MetricLocalName.Total,
            kind=MetricKind.Counter,
            counter_kind=CounterKind.Cumulative,
            data_type=DataType.Int,
            value=[str(1)],
            task_name=EXPORT_SKILL_TASK
        )

        skill = skill_client.export_skill(args.skill_name, output_artifact_path)

        job = job_client.get_job(
            GetJobRequest(
                workspace_id=job_name.workspace_id,
                local_name=job_name.local_name,
            )
        )
        # 检查并初始化tags
        if job.tags is None:
            job.tags = {}

        # 向tags字典中添加内容
        job.tags['skillName'] = skill.name
        job.tags['skillDisplayName'] = skill.displayName
        job.tags['outputFileFormat'] = "tar"
        job.tags['outputFileName'] = f"{skill.localName}_{str(artifact_name.version)}.tar"
        # 向tags字典中添加内容


        # 提取模型名称
        nodes = GraphContent(nodes=skill.graph["nodes"]).get_nodes("ObjectDetectOperator")
        model_artifact_names = [
            model.value for node in nodes
            if (model := node.get_property("modelName"))
        ] if nodes else []

        # 写入模型清单
        models_path = os.path.join(output_artifact_path, 'artifact.txt')
        with open(models_path, 'w', encoding='utf-8') as f:
            f.write(','.join(sorted(model_artifact_names)))
            logger.info("Exported %d models to: %s",
                        len(model_artifact_names), models_path)

        logger.info("Found %d ObjectDetectOperator nodes with %d models",
                    len(nodes) if nodes else 0,
                    len(model_artifact_names)
                    )

        job_client.update_job(request=UpdateJobRequest(
            workspace_id=job.workspace_id, local_name=job.local_name,
            tags=job.tags,
        ))

        report_success(skill, artifact_name.version, tracker)
        logger.info("ExportSkill End")
    except Exception as e:
        logger.error(f"StackTrace: {traceback.format_exc()}")
        if tracker is not None:
            tracker.log_event(
                kind=EventKind.Failed,
                reason=f"系统内部错误，技能导出任务失败",
                message=f"{str(e)[:500]}",
            )
            tracker.log_metric(
                local_name=MetricLocalName.Failed,
                kind=MetricKind.Gauge,
                counter_kind=CounterKind.Cumulative,
                data_type=DataType.Int,
                value=[str(1)],
            )
        logger.error("ExportSkill failed")
        raise ValueError(f"ExportSkillError {str(e)}")


def report_success(skill: Skill, version: str, tracker: Tracker):
    # 上报task成功
    tracker.log_metric(
        local_name=MetricLocalName.Success,
        kind=MetricKind.Counter,
        counter_kind=CounterKind.Cumulative,
        data_type=DataType.Int,
        value=[str(1)],
        task_name=EXPORT_SKILL_TASK
    )

    tracker.log_event(
        kind=EventKind.Succeed,
        reason=f"技能名称(版本)：{str(skill.displayName)}(v{str(version)}) \n技能ID：{str(skill.name)}",
        message=f"技能名称(版本)：{str(skill.displayName)}(v{str(version)}) \n技能ID：{str(skill.name)}",
    )

    pass


if __name__ == "__main__":
    run()
