#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2023/8/8 15:30
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : artifact_client.py
# @Software: PyCharm
"""
import json
import os
import re
from typing import List, Optional, Dict, Any

from baidubce.http import http_content_types
from baidubce.http import http_methods
from bceinternalsdk.client.bce_internal_client import BceInternalClient
from bceinternalsdk.client.paging import PagingRequest
from bceinternalsdk.client.validator import parse_object_name
from windmillcomputev1.client.compute_client import ComputeClient
from windmillcomputev1.filesystem import download_by_filesystem, upload_by_filesystem

from .artifact_api_artifact import parse_artifact_name, LocationStyle


class ArtifactClient(BceInternalClient):
    """
    A client class for interacting with the Artifact service. Initializes with default configuration.

    This client provides an interface to interact with the Artifact service using BCE (Baidu Cloud Engine) API.
    It supports operations related to creating and retrieving artifacts within a specified workspace.
    """

    def create_artifact(
        self,
        uri: str,
        object_name: Optional[str] = "",
        alias: Optional[List] = None,
        tags: Optional[Dict] = None,
        metadata: Optional[Any] = None,
        description: Optional[str] = None,
        source_name: Optional[str] = None,
        source_display_name: Optional[str] = None,
    ):
        """
        Create a new artifact.

        Args:
            uri (str): 版本文件路径, example:"s3://aiqa/store/workspaces/ws1/modelstores/ms1/models/model1/1"
            object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"`
            alias (Optional[List]): 版本别名，如default, latest
            tags (Optional[Dict]): 版本标签
            metadata (Optional[Any]): 版本基本信息
            description (Optional[str]): 版本描述
            source_name (Optional[str]): 版本来源名称
            source_display_name (Optional[str]): 版本来源显示名称

        Returns:
            dict: The response containing information about the created artifact.
        """
        body = {
            "uri": uri,
            "alias": alias,
            "tags": tags,
            "metadata": metadata,
            "description": description,
            "objectName": object_name,
            "sourceName": source_name,
            "sourceDisplayName": source_display_name,
        }
        return self._send_request(
            http_method=http_methods.POST,
            path=b"/v1/versions",
            params={"objectName": object_name},
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def get_artifact(
        self,
        name: Optional[str] = "",
        object_name: Optional[str] = "",
        version: Optional[str] = "",
    ):
        """
        Get details of an artifact.

        Args:
            name (str): artifact name, example:"workspaces/ws1/modelstores/ms1/models/model1/versions/1"
            version (str): 版本, example:"1"
            object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"`

        Returns:
            dict: The response containing details of the requested artifact.
        """
        if name != "":
            artifact_name = parse_artifact_name(name=name)
            object_name = artifact_name.object_name
            version = artifact_name.version
        return self._send_request(
            http_method=http_methods.GET,
            path=bytes("/v1/versions/" + version, encoding="utf-8"),
            params={"objectName": object_name},
        )

    def list_artifact(
        self,
        object_name: Optional[str] = "",
        page_request: Optional[PagingRequest] = PagingRequest(),
        tags: Optional[dict] = None,
    ):
        """
        List artifacts based on the specified parameters.

        Args:
            object_name (str): 数据完整名称，example:"workspaces/ws1/modelstores/ms1/models/model1"
            page_request (PagingRequest, optional): Paging request configuration. Default is PagingRequest().
            tags (dict, optional): Tags to filter artifacts by. Default is None.

        Returns:
            dict: Response from the service containing a list of artifacts.
        """
        params = {
            "objectName": object_name,
            "pageNo": str(page_request.get_page_no()),
            "pageSize": str(page_request.get_page_size()),
            "order": page_request.order,
            "orderBy": page_request.orderby,
            "tags": json.dumps(tags if tags is not None else {}),
        }

        return self._send_request(
            http_method=http_methods.GET,
            path=bytes("/v1/versions", encoding="utf-8"),
            params=params,
        )

    def update_artifact(
        self,
        name: Optional[str] = "",
        object_name: Optional[str] = "",
        version: Optional[str] = "",
        alias: Optional[list] = None,
        tags: Optional[dict] = None,
        metadata: Optional[Any] = None,
        description: Optional[str] = None,
    ):
        """
        Update details of an artifact.

        Args:
            object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"
            version (str): 版本 example:"1"
            alias (Optional[List]):  版本别名，如default, latest.
            tags (Optional[Dict]): 版本标签 [key:value]
            metadata (Optional[Any]): 版本基本信息
            description (str): 版本描述, example:"artifact description"

        Returns:
            dict: The response containing information about the updated artifact.
        """
        if name != "":
            artifact_name = parse_artifact_name(name=name)
            object_name = artifact_name.object_name
            version = artifact_name.version

        body = {
            "alias": alias,
            "tags": tags,
            "description": description,
            "metadata": metadata,
            "objectName": object_name,
            "version": version,
        }
        return self._send_request(
            http_method=http_methods.PUT,
            path=bytes("/v1/versions/" + version, encoding="utf-8"),
            params={"objectName": object_name},
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def delete_artifact(
        self,
        object_name: Optional[str] = "",
        version: Optional[str] = "",
        force: Optional[bool] = False,
    ):
        """
        Delete an artifact.

        Args:
        object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"
        version (str): 版本，如["1", "default"]

        Returns:
        dict: The response indicating the success of the deletion.
        """
        return self._send_request(
            http_method=http_methods.DELETE,
            path=bytes("/v1/versions/" + version, encoding="utf-8"),
            params={"objectName": object_name, "force": force},
        )

    def download_artifact(
        self,
        name: Optional[str] = "",
        object_name: Optional[str] = "",
        version: Optional[str] = "",
        output_uri: Optional[str] = ".",
    ):
        """
        Download an artifact.

        Args:
        version (str): 版本, example:"1"
        object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"`
        output_uri (str): 下载路径, example:"./"
        """
        if name != "":
            artifact_name = parse_artifact_name(name=name)
            object_name = artifact_name.object_name
            version = artifact_name.version

        resp = self.get_artifact(object_name=object_name, version=version)
        filesystem = ComputeClient(
            config=self.config, context=self.context
        ).suggest_first_filesystem(
            workspace_id=resp.workspaceID, guest_name=resp.parentName
        )
        download_by_filesystem(
            filesystem=filesystem, file_path=resp.uri, dest_path=output_uri
        )

    def create_location_with_uri(
        self,
        uri,
        object_name: Optional[str] = "",
        style: Optional[str] = LocationStyle.DEFAULT.value,
        source_filesystem: Optional[dict] = None,
    ):
        """
        create location and upload artifact
        Args:
        uri (str): 版本文件路径, example:"/home/store/workspaces/ws1/modelstores/ms1/models/model1/1"
        object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"`
        style (str): location的style, example:"Default"
        source_filesystem (dict, optional): 源文件系统配置,
            example:{"kind":"s3","host":"s3.bcebos.com","endpoint":"windmill/"}
        """
        naming = parse_object_name(object_name)
        filesystem = ComputeClient(
            self.config, context=self.context
        ).suggest_first_filesystem(
            workspace_id=naming.workspace_id, guest_name=naming.parent_name
        )

        location = uri
        if self.is_upload_required(location, filesystem, source_filesystem):
            resp = self.create_location(object_name=object_name, style=style)
            location = resp.location
            # 如果直接存储在磁盘, 没必要保存多个同版本的模型文件夹
            if filesystem["kind"] == "file":
                location = self._strip_location_timestamp(location)

            if os.path.isfile(uri):
                filename = os.path.basename(uri)
                location = location + "/" + filename
            upload_by_filesystem(
                filesystem=filesystem,
                file_path=uri,
                dest_path=location,
                source_filesystem=source_filesystem,
            )

        return location

    @staticmethod
    def is_upload_required(uri, filesystem, source_filesystem):
        """
        is_upload_required
        reference: artifact-go/command/artifact.go:CheckUri
        """
        if source_filesystem is None:
            if uri.startswith(filesystem["kind"]):
                return False

            # need enum filesystem.kind
            if filesystem["kind"] == "file" and uri.startswith("s3"):
                return False

            return True

        # TODO: 支持 s3 之间直接 copy
        if (filesystem["kind"] == source_filesystem["kind"]) and (
            filesystem["kind"] == "s3"
        ):
            return False
        return True

    def create_location(
        self,
        object_name: Optional[str] = "",
        style: Optional[str] = LocationStyle.DEFAULT.value,
    ):
        """
        Create a new location.

        Args:
            object_name (str): 数据完整名称, example:"workspaces/ws1/modelstores/ms1/models/model1"
            style (str): 版本文件路径风格, binding:"omitempty,oneof=Default Triton" default:"Default""

        Returns:
            dict: The response containing information about the created location.
        """
        body = {"style": style, "objectName": object_name}
        return self._send_request(
            http_method=http_methods.POST,
            path=b"/v1/locations",
            params={"objectName": object_name},
            headers={b"Content-Type": http_content_types.JSON},
            body=json.dumps(body),
        )

    def get_path(self, filesystem, artifact_uri) -> str:
        """
        get file path from artifact uri

        Args:
            filesystem (dict): fs
            artifact_uri (str): 版本文件路径
                example: "s3://windmill/store/workspaces/default/modelstores/default/models/default/versions/1"

        Returns:
            str: file path, example: "workspaces/default/modelstores/default/models/default/versions/1"
        """
        base_uri = ComputeClient(
            config=self.config, context=self.context
        ).build_base_uri(filesystem=filesystem)

        if filesystem["workspaceID"] == "public":
            base_uri = base_uri.rsplit("/", 1)[0]
            return os.path.relpath(artifact_uri, base_uri).rstrip("/")
        return os.path.relpath(artifact_uri, base_uri).rstrip("/")

    @staticmethod
    def _strip_location_timestamp(location):
        """
        修正location
        e.g. "/data/model/workspaces/wsvykgec/modelstores/ms-4B6vVufC/models/model1/1-1735485337987"
          => "/data/model/workspaces/wsvykgec/modelstores/ms-4B6vVufC/models/model1/1"
        """
        location_dir = os.path.dirname(location)
        location_basename = os.path.basename(location)
        pattern = r"^(\d+)-(\d{10,})$"

        parts = re.match(pattern, location_basename)

        if parts:
            return os.path.join(location_dir, parts.group(1))
        else:
            return location
