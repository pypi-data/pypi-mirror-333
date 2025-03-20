#  Copyright (C) 2023 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import SimpleStorageServiceS3BucketWithObjects
from diagrams.digitalocean.compute import Docker
from diagrams.onprem.compute import Server

with Diagram("Infrastructure", show=False, direction="LR"):
    with Cluster("Central"):
        central_minio = SimpleStorageServiceS3BucketWithObjects("MinIO")

    with Cluster("Station"):
        minio = SimpleStorageServiceS3BucketWithObjects("MinIO")
        sd = Server("statistics devices")
        statistics_container = Docker("statistics writers")
        sd >> Edge(label="statistics packets") >> statistics_container >> Edge(label="write blocks of 5m") >> minio
        minio >> Edge(label="replicate") >> central_minio


