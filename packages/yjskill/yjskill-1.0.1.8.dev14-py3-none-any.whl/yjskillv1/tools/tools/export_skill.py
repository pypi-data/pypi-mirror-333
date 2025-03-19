# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authors: duanshichao(duanshichao@baidu.com)
Date: 2025/03/09
"""
import os
import traceback
from argparse import ArgumentParser

import bcelogger as logger
from jobv1.client.job_api_event import EventKind
from jobv1.client.job_api_job import parse_job_name, GetJobRequest, UpdateJobRequest, JobName
from jobv1.client.job_api_metric import MetricLocalName, MetricKind, CounterKind, DataType
from jobv1.client.job_client import (
    JobClient
)
from jobv1.tracker.tracker import Tracker
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.filesystem import upload_by_filesystem

from yjskillv1.client.skill_api_skill import GetSkillRequest, parse_skill_name, Skill
from yjskillv1.client.skill_client import SkillClient

# import bcelogger

EXPORT_SKILL = "Export/Skill"
EXPORT_SKILL_TASK = "export-skill"
EXPORT_SKILL_KIND = "Skill"
EXPORT_SKILL_TEMPLATE_KIND = "SkillTemplate"


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--skill_name", required=True, type=str, default="")
    parser.add_argument("--export_kind", required=True, type=str, default="")
    parser.add_argument("--output_file_name", required=True, type=str, default="")

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
        export_kind = args.export_kind
        output_file_name = args.output_file_name

        org_id = os.getenv("ORG_ID","ab87a18d6bdf4fc39f35ddc880ac1989")
        user_id = os.getenv("USER_ID","7e0c86dd01ae4402aa0f4e003f3480fd")
        job_name = os.getenv("JOB_NAME","workspaces/wsgdessn/jobs/job-8q56053k")
        windmill_endpoint = os.getenv("WINDMILL_ENDPOINT","10.224.41.35:8340")
        vistudio_endpoint = os.getenv("VISTUDIO_ENDPOINT","10.224.41.35:8440")
        output_artifact_path = os.getenv(
            "PF_OUTPUT_ARTIFACT_SKILL_DATA", "./skill_data"
        )

        job_name: JobName = parse_job_name(job_name)

        if not job_name or not (job_name.local_name and job_name.workspace_id):
            raise ValueError(f"Invalid job name: {job_name}")

        job_client = JobClient(endpoint=windmill_endpoint, context={"OrgID": org_id, "UserID": user_id}, )
        windmill_client = WindmillClient(endpoint=windmill_endpoint, context={"OrgID": org_id, "UserID": user_id}, )
        skill_client = SkillClient(endpoint=vistudio_endpoint, context={"OrgID": org_id, "UserID": user_id})

        tracker = Tracker(
            client=job_client,
            workspace_id=job_name.workspace_id,
            job_name=job_name.get_name(),
            task_name=EXPORT_SKILL_TASK,
        )
        # 上报job总数
        tracker.log_metric(
            local_name=MetricLocalName.Total,
            kind=MetricKind.Counter,
            counter_kind=CounterKind.Cumulative,
            data_type=DataType.Int,
            task_name="",
            value=[str(1)])

        tracker.log_metric(
            local_name=MetricLocalName.Total,
            kind=MetricKind.Counter,
            counter_kind=CounterKind.Cumulative,
            data_type=DataType.Int,
            value=[str(1)],
        )

        artifact_name = parse_artifact_name(skill_version_name)
        skill_name = parse_skill_name(artifact_name.object_name)
        skill = skill_client.get_skill(req=GetSkillRequest(
            workspaceID=skill_name.workspace_id,
            localName=skill_name.local_name,
            version=artifact_name.version))

        skill_client.export_skill(args.skill_name, output_artifact_path)

        if not os.path.exists(os.path.join(output_artifact_path, "skill.json")):
            tracker.log_event(
                kind=EventKind.Failed,
                reason="技能导出错误：技能模板导出失败",
                message=f"技能导出失败：系统内部错误",
            )
            tracker.log_metric(
                local_name=MetricLocalName.Failed,
                kind=MetricKind.Gauge,
                counter_kind=CounterKind.Cumulative,
                data_type=DataType.Int,
                value=[str(1)],
                task_name=""
            )
            return

        tracker.log_event(
            kind=EventKind.Succeed,
            reason=f"技能名称(版本)：{str(skill.displayName)}(v{str(artifact_name.version)})",
            message=f"技能名称(版本)：{str(skill.displayName)}(v{str(artifact_name.version)})",
        )
        tracker.log_event(
            kind=EventKind.Succeed,
            reason=f"技能ID：{str(skill.name)}",
            message=f"技能ID：{str(skill.name)}"
        )

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
        job.tags['outputFileFormat'] = "json"
        job.tags['outputFileName'] = output_file_name

        if export_kind == EXPORT_SKILL_TEMPLATE_KIND:
            filesystem = windmill_client.suggest_first_filesystem(skill.workspaceID,
                                   guest_name=f"workspaces/{skill.workspaceID}")
            # 上传文件
            bucket = filesystem["endpoint"]
            output_uri = f"s3://{bucket}/{job.name}/export/{job.display_name}"
            job.tags['outputUri'] = output_uri


            skill_file = os.path.join(output_artifact_path, "skill.json")
            upload_by_filesystem(filesystem, skill_file, output_uri)

            # 模板导出记录成功指标
            tracker.log_metric(
                local_name=MetricLocalName.Success,
                kind=MetricKind.Counter,
                counter_kind=CounterKind.Cumulative,
                data_type=DataType.Int,
                value=[str(1)],
                task_name=""
            )

        job_client.update_job(request=UpdateJobRequest(
            workspace_id=job.workspace_id, local_name=job.local_name,
            tags=job.tags,
        ))
        logger.info("ExportSkill End")
    except Exception as e:
        logger.error(f"ExportSkill Error: {str(e)}")
        logger.error(f"StackTrace: {traceback.format_exc()}")
        if tracker is not None:
            tracker.log_metric(
                local_name=MetricLocalName.Failed,
                kind=MetricKind.Gauge,
                counter_kind=CounterKind.Cumulative,
                data_type=DataType.Int,
                value=[str(1)],
                task_name=""
            )
        logger.error("ExportSkill End")


def upload_skill_template(job_name, skill, output_artifact_path, job_client, windmill_client):
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

    filesystem = windmill_client.suggest_first_filesystem(job_name.workspace_id,
                                                          guest_name=f"workspaces/{job_name.workspace_id}")
    # 上传文件
    output_uri = f"s3://{filesystem.endpoint}/{job.name}/export/skill.json"
    job.tags['outputUri'] = output_uri

    skill_file = os.path.join(output_artifact_path, "skill.json")
    upload_by_filesystem(filesystem, skill_file, output_uri)

    job_client.update_job(request=UpdateJobRequest(
        workspace_id=job.workspace_id, local_name=job.local_name,
        tags=job.tags,
    ))
    pass


if __name__ == "__main__":
    run()
