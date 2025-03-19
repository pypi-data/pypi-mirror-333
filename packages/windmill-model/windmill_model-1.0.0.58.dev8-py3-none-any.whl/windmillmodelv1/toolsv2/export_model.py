#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
export_model.py
Authors: zhoubohan(zhoubohan@baidu.com)
Date:    2025/03/10
"""
import os
import shutil
import tarfile
import traceback
from argparse import ArgumentParser

import bcelogger
from jobv1.client.job_api_event import EventKind
from jobv1.client.job_api_job import parse_job_name, UpdateJobRequest, GetJobRequest
from jobv1.client.job_api_metric import (
    MetricLocalName,
    MetricKind,
    CounterKind,
    DataType,
)
from jobv1.client.job_api_task import UpdateTaskRequest
from jobv1.client.job_client import JobClient
from jobv1.tracker.tracker import Tracker
from windmillartifactv1.client.artifact_api_artifact import parse_artifact_name
from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.filesystem import blobstore, upload_by_filesystem
from windmillmodelv1.client.model_api_model import parse_model_name

EXPORT_MODEL_TASK_DISPLAY_NAME = "模型导出"
EXPORT_MODEL_TASK_NAME = "export-model"
EXPORT_SKILL_JOB_KIND = "Export/Skill"


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--artifact_names", required=False, type=str, default="")
    parser.add_argument("--output_uri", required=False, type=str, default=".")
    parser.add_argument("--output_file_name", required=False, type=str, default="model.tar")

    args, _ = parser.parse_known_args()
    return args


def run():
    """
    export model.
    """
    args = parse_args()
    org_id = os.getenv("ORG_ID")
    user_id = os.getenv("USER_ID")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT")
    job_name = os.getenv("JOB_NAME")
    job_kind = os.getenv("JOB_KIND")
    file_name = args.output_file_name
    output_uri = args.output_uri

    job_success = True

    windmill_client = WindmillClient(
        endpoint=windmill_endpoint, context={"OrgID": org_id, "UserID": user_id}
    )

    job_client = JobClient(
        endpoint=windmill_endpoint, context={"OrgID": org_id, "UserID": user_id}
    )

    parsed_job_name = parse_job_name(job_name)
    tracker = Tracker(
        client=job_client,
        job_name=parsed_job_name.local_name,
        workspace_id=parsed_job_name.workspace_id,
        task_name=EXPORT_MODEL_TASK_NAME,
    )

    job_client.update_task(
        UpdateTaskRequest(
            workspace_id=parsed_job_name.workspace_id,
            job_name=parsed_job_name.local_name,
            local_name=EXPORT_MODEL_TASK_NAME,
            display_name=EXPORT_MODEL_TASK_DISPLAY_NAME,
        )
    )

    job_detail = job_client.get_job(
        GetJobRequest(
            workspace_id=parsed_job_name.workspace_id,
            local_name=parsed_job_name.local_name,
        )
    )

    if len(job_kind) == 0:
        job_kind = job_detail.kind

    if job_detail.tags is None or len(job_detail.tags) == 0:
        job_detail.tags = {}

    artifact_names = args.artifact_names.split(",")
    if job_kind == EXPORT_SKILL_JOB_KIND:
        last_output_artifact = os.getenv("PF_INPUT_ARTIFACT_MODEL_DATA")
        if last_output_artifact is not None:
            artifact_name_path = os.path.join(last_output_artifact, "artifact.txt")
            if os.path.exists(artifact_name_path):
                with open(artifact_name_path) as f:
                    artifact_names = f.read().split(",")

            skill_json_path = os.path.join(last_output_artifact, "skill.json")
            dest_skill_json_path = os.path.join(output_uri, "skill.json")
            if os.path.exists(skill_json_path):
                shutil.copyfile(skill_json_path, dest_skill_json_path)


    if len(artifact_names) == 0:
        exit(1)

    # log model task total
    tracker.log_metric(
        local_name=MetricLocalName.Total,
        kind=MetricKind.Gauge,
        counter_kind=CounterKind.Cumulative,
        data_type=DataType.Int,
        value=[str(len(artifact_names))],
    )

    for a_name in artifact_names:
        try:
            windmill_client.dump_models(artifact_name=a_name, output_uri=output_uri)
            if not os.path.exists(os.path.join(output_uri, "apply.yaml")):
                raise ValueError(f"模型导出失败({a_name})：apply.yaml未生成！")

            artifact_name = parse_artifact_name(a_name)
            model_name = parse_model_name(artifact_name.object_name)
            model_list = windmill_client.get_model_manifest(
                model_name.workspace_id,
                model_name.model_store_name,
                model_name.local_name,
                artifact_name.version,
            )
            for item in model_list.subModels:
                k = f"{model_name.local_name}.{item['localName']}"
                job_detail.tags[k] = str(item["artifact"]["version"])
        except Exception as e:
            bcelogger.error(
                f"Export model {job_name} failed: {traceback.format_exc()}"
            )
            job_success = False
            tracker.log_metric(
                local_name=MetricLocalName.Failed,
                kind=MetricKind.Counter,
                counter_kind=CounterKind.Monotonic,
                data_type=DataType.Int,
                value=["1"],
            )
            tracker.log_event(
                kind=EventKind.Failed,
                reason=f"模型导出失败({a_name})：系统错误",
                message=str(e)[:500],
            )

            if job_kind == EXPORT_SKILL_JOB_KIND:
                tracker.log_event(
                    kind=EventKind.Failed,
                    reason=f"模型导出失败({a_name})：系统错误",
                    message=str(e)[:500],
                    task_name="",
                )
            continue

        # log model task success
        tracker.log_metric(
            local_name=MetricLocalName.Success,
            kind=MetricKind.Counter,
            counter_kind=CounterKind.Monotonic,
            data_type=DataType.Int,
            value=["1"],
        )

    try:
        with tarfile.open(file_name, "w:") as tar:
            tar.add(output_uri, arcname=os.path.basename(output_uri))

        filesystem = windmill_client.suggest_first_filesystem(
            workspace_id=parsed_job_name.workspace_id,
            guest_name=job_name,
        )

        bs = blobstore(filesystem=filesystem)
        job_path = bs.build_url(os.path.join(filesystem.endpoint, job_name))
        upload_uri = os.path.join(job_path, file_name)

        upload_by_filesystem(filesystem, file_name, upload_uri)
        bcelogger.info(f"Uploaded {file_name} to {upload_uri}")
    except Exception as e:
        bcelogger.error(
            f"Upload model {job_name} failed: {traceback.format_exc()}"
        )
        job_success = False
        tracker.log_event(
            kind=EventKind.Failed,
            reason=f"模型压缩包上传失败：系统错误",
            message=str(e)[:500],
        )

        if job_kind == EXPORT_SKILL_JOB_KIND:
            tracker.log_event(
                kind=EventKind.Failed,
                reason=f"文件上传失败：系统错误",
                message=str(e)[:500],
                task_name="",
            )

    job_detail.tags["outputUri"] = upload_uri

    job_client.update_job(
        UpdateJobRequest(
            workspace_id=parsed_job_name.workspace_id,
            local_name=parsed_job_name.local_name,
            tags=job_detail.tags,
        )
    )

    if job_kind == EXPORT_SKILL_JOB_KIND:
        if job_success:
            tracker.log_metric(
                local_name=MetricLocalName.Success,
                kind=MetricKind.Counter,
                counter_kind=CounterKind.Monotonic,
                data_type=DataType.Int,
                value=["1"],
                task_name="",
            )
        else:
            tracker.log_metric(
                local_name=MetricLocalName.Failed,
                kind=MetricKind.Counter,
                counter_kind=CounterKind.Monotonic,
                data_type=DataType.Int,
                value=["1"],
                task_name="",
            )


if __name__ == "__main__":
    run()
