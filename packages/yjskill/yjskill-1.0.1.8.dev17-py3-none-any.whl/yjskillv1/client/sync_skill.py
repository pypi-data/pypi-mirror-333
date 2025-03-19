"""
distribute_skill.py
Authors: leibin01(leibin01@baidu.com)
Date: 2024/12/10
"""
import bcelogger
import traceback
import os
import json
from argparse import ArgumentParser
from typing import Optional, List

from baidubce.exception import BceHttpClientError
from .skill_client import SkillClient
from .skill_api_skill import CreateSkillRequest, GetSkillRequest
from devicev1.client.device_client import DeviceClient
from devicev1.client.device_api import UpdateDeviceRequest, InvokeMethodHTTPRequest, ListDeviceRequest
from jobv1.client.job_api_event import EventKind
from jobv1.client.job_api_metric import (
    MetricKind, CounterKind, MetricLocalName, DataType)
from jobv1.client.job_client import (
    JobClient,
    CreateJobRequest, CreateTaskRequest, CreateEventRequest, UpdateJobRequest,
    CreateMetricRequest, GetJobRequest, DeleteMetricRequest, DeleteJobRequest
)


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--workspace_id", required=True, type=str, default="")
    parser.add_argument("--skill_name",
                        required=True, type=str, default="")
    parser.add_argument("--version", required=True, type=str, default="")
    parser.add_argument("--edge_names", required=True, type=str, default="")
    parser.add_argument("--device_config", required=True, type=str, default="")

    args, _ = parser.parse_known_args()
    return args


def run():
    """
    sync skill.
    """

    bcelogger.info("SyncSkill Start")

    args = parse_args()
    bcelogger.info("SyncSkill Args: %s", args)

    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")

    job_name = os.getenv("SKILL_SYNC_JOB_NAME", "")
    skill_task_name = os.getenv("SKILL_SYNC_TASK_NAME", "")
    model_task_name = os.getenv("MODEL_SYNC_TASK_NAME", "")

    skill_endpoint = os.getenv("SKILL_ENDPOINT", "")
    job_endpoint = os.getenv("JOB_ENDPOINT", "")
    device_endpoint = os.getenv("DEVICE_ENDPOINT", "")
    bcelogger.info("SyncSkill envs, \n \
                   org_id: %s, \n \
                   user_id: %s, \n \
                   job_name: %s, \n \
                   skill_task_name: %s, \n \
                   model_task_name: %s, \n \
                   skill_endpoint: %s, \n \
                   job_endpoint: %s, \n \
                   device_endpoint: %s", org_id, user_id,
                   job_name, skill_task_name, model_task_name,
                   skill_endpoint, job_endpoint, device_endpoint)

    skill_client = SkillClient(endpoint=skill_endpoint,
                               context={"OrgID": org_id, "UserID": user_id})
    job_client = JobClient(endpoint=job_endpoint,
                           context={"OrgID": org_id, "UserID": user_id})
    device_client = DeviceClient(endpoint=device_endpoint,
                                 context={"OrgID": org_id, "UserID": user_id})

    skill = {}
    tags = {}
    try:
        get_skill_req = GetSkillRequest(
            workspaceID=args.workspace_id,
            localName=args.skill_name,
            version=args.version)
        skill = skill_client.get_skill(req=get_skill_req)
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error("SyncSkillGetSkill %s Failed: %s",
                        args.skill_name,
                        traceback.format_exc())
        # TODO 更新job状态？
        return
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "内部服务错误！"
        }
        bcelogger.error("SyncSkillGetSkill %s Failed: %s",
                        args.skill_name,
                        traceback.format_exc())
        # TODO 更新job状态？
        return

    # 技能下发到盒子
    # 1. 盒子状态检查
    # 2. 盒子硬件信息匹配检查
    edge_msg = "{}（{}）{}"  # id（中文名）成功/失败原因
    edges, tags = list_devices(
        device_client=device_client,
        workspace_id=args.workspace_id,
        selects=args.edge_names)
    if tags["errorCode"] != "0":
        # TODO 更新job状态？
        return

    # TODO skill适配的硬件信息从哪取？
    # 要从Artifact的tag取，因为下发是指定了技能的版本

    succeed_count = 0
    failed_count = 0
    device_config = json.loads(args.device_config)
    skill_metric_display_name = "技能下发"
    for edge in edges:
        edge_local_name = edge["localName"]
        edge_workspace = edge["workspaceID"]
        edge_msg = edge_msg.format(
            edge_local_name, edge["displayName"], "成功")

        # TODO 初期联调时，暂时不做硬件信息检查
        # ok, msg = check_edge(skill_tag=skill["tag"]["accelerator"],
        #                      device_config=device_config,
        #                      edge=edge)
        # if not ok:
        #     failed_count += 1
        #     bcelogger.error(
        #         f"SyncSkillCheckEdgeFailed: {msg}, edge:{edge_local_name}")
        #     tags = {
        #         "errorCode": "400",
        #         "errorMessage": edge_msg.format(edge_local_name, edge["displayName"], msg)
        #     }

        #     # metric and event
        #     create_event(
        #         job_client=job_client,
        #         workspace_id=edge_workspace,
        #         job_name=job_name,
        #         task_name=skill_task_name,
        #         kind=EventKind.Failed,
        #         reason=msg,
        #         message=edge_msg.format(
        #             edge_local_name, edge["displayName"], msg),
        #     )
        #     create_metric(
        #         job_client=job_client,
        #         workspace_id=edge_workspace,
        #         job_name=job_name,
        #         display_name=skill_metric_display_name,
        #         local_name=MetricLocalName.Failed,
        #         kind=MetricKind.Gauge,
        #         data_type=DataType.Int,
        #         value=[str(failed_count)])
        #     continue

        # TODO 下发模型

        # 修改graph中的workspaceID
        graph = build_graph(
            origin_graph=skill["graph"],
            replace={skill["workspaceID"]: edge["workspaceID"]})

        create_skill_req = CreateSkillRequest(
            workspaceID=edge["workspaceID"],
            localName=skill["localName"],
            displayName=skill["displayName"],
            description=skill["description"],
            kind="Video",
            fromKind="System",
            createKind="Sync",
            tags=skill["tags"],
            graph=graph,
            imageURI=skill["imageURI"],
            defaultLevel=skill["defaultLevel"],
            alarmConfigs=skill["alarmConfigs"],
        )
        tags = create_skill(
            device_hub_name=edge["deviceHubName"],
            device_name=edge["localName"],
            client=skill_client,
            req=create_skill_req)
        if tags["errorCode"] != "0":
            failed_count += 1
            bcelogger.error("SyncSkillUpdateDevice skill=%s,device=%s",
                            args.skill_name,
                            edge['localName'])

            # metric and event
            create_event(
                job_client=job_client,
                workspace_id=edge_workspace,
                job_name=job_name,
                kind=EventKind.Failed,
                reason=tags["errorMessage"],
                message=edge_msg.format(
                    edge["localName"], edge["displayName"], tags["errorMessage"]),
            )
            create_metric(
                job_client=job_client,
                workspace_id=edge_workspace,
                job_name=job_name,
                display_name=skill_metric_display_name,
                local_name=MetricLocalName.Failed,
                kind=MetricKind.Gauge,
                data_type=DataType.Int,
                value=[str(failed_count)])
            continue

        # metric and event
        succeed_count += 1
        create_event(
            job_client=job_client,
            workspace_id=edge_workspace,
            job_name=job_name,
            kind=EventKind.Succeed,
            reason="技能下发成功",
            message=edge_msg.format(
                edge["localName"], edge["displayName"], "技能下发成功"),
        )
        create_metric(
            job_client=job_client,
            workspace_id=edge_workspace,
            job_name=job_name,
            display_name=skill_metric_display_name,
            local_name=MetricLocalName.Success,
            kind=MetricKind.Gauge,
            data_type=DataType.Int,
            value=[str(succeed_count)])


def list_devices(
        device_client: DeviceClient,
        workspace_id: str,
        selects: Optional[list[str]] = None):
    """
    获取设备列表

    Args:
        device_client: DeviceClient 设备客户端
        workspace_id: str 工作空间ID
        selects: list[str] 设备名称列表,localName
    Returns:
        devices: list[dict] 设备列表
        tags: dict 返回结果
    """

    list_device_req = ListDeviceRequest(
        workspaceID=workspace_id,
        deviceHubName="default",
        pageSize=200,
        pageNo=1,
        selects=selects)
    try:
        total, current_count = 0, 0
        devices = []
        bcelogger.debug("origin req is %s",
                        list_device_req.model_dump(by_alias=True, exclude_defaults=True))

        resp = device_client.list_device(req=list_device_req)
        bcelogger.trace("SyncSkillListDevice: totalCount=%d pageNo=%d",
                        resp.totalCount,
                        list_device_req.page_no)
        total = resp.totalCount
        result = resp.result
        current_count = len(result)
        devices.extend(result)

        while current_count < total:
            list_device_req.__setattr__("page_no", list_device_req.page_no + 1)
            bcelogger.trace("SyncSkillListDevice: totalCount=%d pageNo=%d",
                            resp.totalCount, list_device_req.page_no)
            resp = device_client.list_device(req=list_device_req)
            result = resp.result
            bcelogger.trace("SyncSkillListDevice: pageNo=%d, result length=%d, totalCount=%d",
                            list_device_req.page_no, len(result), total)

            current_count += len(result)
            devices.extend(result)
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error("SyncSkillListDevice list_device_req=%s Failed: %s",
                        list_device_req.model_dump(by_alias=True),
                        traceback.format_exc())
        return [], tags
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "查询设备失败"
        }
        bcelogger.error("SyncSkillListDevice list_device_req=%s Failed: %s",
                        list_device_req.model_dump(by_alias=True),
                        traceback.format_exc())
        return [], tags

    tags = {
        "errorCode": "0",
        "errorMessage": "成功"
    }
    return devices, tags


def build_graph(
        origin_graph: dict,
        replace: dict):
    """
    构建graph

    Args:
        origin_graph: dict 原始图
        replace: dict 替换关系<old,new>
    """

    origin_graph_json = json.dumps(origin_graph)
    for old, new in replace.items():
        origin_graph_json = origin_graph_json.replace(old, new)
    return json.loads(origin_graph_json)


def create_metric(
        job_client: JobClient,
        workspace_id: str,
        job_name: str,
        display_name: str,
        local_name: MetricLocalName,
        kind: MetricKind,
        data_type: DataType,
        value: List[str],
        task_name: Optional[str] = None,
):
    """
    创建metric
    """

    create_metric_req = CreateMetricRequest(
        workspace_id=workspace_id,
        job_name=job_name,
        display_name=display_name,
        local_name=local_name,
        kind=kind,
        data_type=data_type,
        value=value,
    )
    if task_name is not None:
        create_metric_req.task_name = task_name
    try:
        create_metric_resp = job_client.create_metric(create_metric_req)
        bcelogger.debug("create_metric success, response is %s",
                        create_metric_resp.model_dump(by_alias=True))
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error("create_metric create_metric_req= %s Failed: %s",
                        create_metric_req.model_dump(by_alias=True),
                        traceback.format_exc())
        return [], tags
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "创建指标失败"
        }
        bcelogger.error("create_metric create_metric_req= %s, Failed: %s",
                        create_metric_req.model_dump(by_alias=True),
                        traceback.format_exc())
        return [], tags


def create_event(
    job_client: JobClient,
    workspace_id: str,
    job_name: str,
    kind: EventKind,
    reason: str,
    message: str,
    task_name: Optional[str] = None,
):
    """
    更新job和device的状态
    """

    create_event_req = CreateEventRequest(
        workspace_id=workspace_id,
        job_name=job_name,
        kind=kind,
        reason=reason,
        message=message)
    if task_name is not None:
        create_event_req.task_name = task_name
    try:
        create_skill_task_event_resp = job_client.create_event(
            create_event_req)
        bcelogger.debug("create_event success, response is %s",
                        create_skill_task_event_resp.model_dump(by_alias=True))
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error("create_event create_event_req= %s Failed: %s",
                        create_event_req.model_dump(by_alias=True),
                        traceback.format_exc())
        return [], tags
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "创建事件失败"
        }
        bcelogger.error("create_event create_event_req=%s Failed: %s",
                        create_event_req.model_dump(by_alias=True),
                        traceback.format_exc())
        return [], tags


def create_skill(
        device_hub_name: str,
        device_name: str,
        client: DeviceClient,
        req: CreateSkillRequest):
    """
    创建技能
    """

    try:
        # 通过BIE调用盒子的create skill HTTP接口
        device_url = f'/v1/workspaces/{req.workspace_id}/skills'
        invoke_method_req = InvokeMethodHTTPRequest(
            workspaceID=req.workspace_id,
            deviceHubName=device_hub_name,
            deviceName=device_name,
            uri=device_url,
            body=req.model_dump(by_alias=True),
        )
        invoke_method_resp = client.invoke_method_http(
            request=invoke_method_req)
        bcelogger.info('SyncSkillCreateSkill req=%s, resp=%s',
                       invoke_method_req, invoke_method_resp)
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error("SyncSkillCreateSkill device=%s Failed: %s",
                        device_name, traceback.format_exc())
        return tags
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "创建技能失败"
        }
        bcelogger.error("SyncSkillCreateSkill device=%s Failed: %s",
                        device_name, traceback.format_exc())
        return tags

    tags = {
        "errorCode": "0",
        "errorMessage": "成功"
    }
    return tags


def update_device_status(
        client: DeviceClient,
        workspace_id: str,
        device_hub_name: str,
        device_name: str,
        status: str):
    """
    更新设备状态
    """

    try:
        # TODO 第一阶段下发model时就改为下发中
        # 4. 更新device状态为下发中（这一步在创建pipeline之前就做完？）
        update_device_req = UpdateDeviceRequest(
            workspaceID=workspace_id,
            deviceHubName=device_hub_name,
            deviceName=device_name,
            # status="Processing",
            status=status,
        )
        update_device_resp = client.update_device(
            request=update_device_req)
        bcelogger.info('SyncSkillUpdateDevice req=%s, resp=%s',
                       update_device_req, update_device_resp)
    except BceHttpClientError as bce_error:
        tags = {
            "errorCode": str(bce_error.last_error.status_code),
            "errorMessage": bce_error.last_error.args[0]
        }
        bcelogger.error("SyncSkillUpdateDevice device=%s Failed: %s",
                        device_name, traceback.format_exc())
        return tags
    except Exception as e:
        tags = {
            "errorCode": "400",
            "errorMessage": "更新设备状态失败"
        }
        bcelogger.error("SyncSkillGetSkill device=%s Failed: %s",
                        device_name, traceback.format_exc())
        return tags

    tags = {
        "errorCode": "0",
        "errorMessage": "成功"
    }
    return tags


def check_edge(
        skill_tag: dict,
        device_config: dict,
        edge: dict,
):
    """
    检查技能是否能下发到盒子

    Args:
        skill_tag (dict): 技能标签
        device_config (dict): 设备配置
        edge (dict): 盒子
    """

    if edge["status"] == "Disconnected":
        return False, "设备已断开连接"

    # 下发中，认为失败
    if edge["status"] == "Processing":
        return False, "设备正在下发中"

    if edge["kind"] not in device_config:
        return False, "未找到设备的硬件信息"

    return check_accelerators(
        skill_accelerator=skill_tag["accelerator"], device_accelelator=device_config[edge["kind"]])


def check_accelerators(
        skill_accelerator: str,
        device_accelelator: str,
):
    """
    检查硬件是否匹配

    Args:
        skill_accelerator(str): 技能硬件信息(tag['accelerator'])
        device_accelelator(str): 设备硬件型号
    """

    if skill_accelerator == "":
        return True, ""

    if device_accelelator == "":
        return False, "设备硬件不适配"

    # 将技能硬件信息转换为列表
    skill_accelerators = json.loads(skill_accelerator)
    device_accelerators = [device_accelelator]

    for sac in skill_accelerators:
        if sac not in device_accelerators:
            return False, "设备硬件不适配"

    return True, ""


if __name__ == "__main__":
    run()
