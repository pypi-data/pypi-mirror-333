job "statistics-bucket-replication" {
  datacenters = ["stat"]
  type        = "batch"

  periodic {
    crons            = ["*/5 * * * * *"]
    prohibit_overlap = true
  }
  group "batch" {
    count = 1

    network {
      mode = "bridge"
    }

    task "mc" {
      driver = "docker"
      config {
        image = "minio/mc:[[.object_storage.mc.version]]"

        entrypoint = ["mc", "batch", "start", "local", "/local/statistics.yaml" ]

        mount {
          type   = "bind"
          source = "local/mc"
          target = "/root/.mc"
        }
      }

      env {
        MINIO_ROOT_USER     = "[[.object_storage.user.name]]"
        MINIO_ROOT_PASSWORD = "[[.object_storage.user.pass]]"
      }

      resources {
        cpu    = 10
        memory = 512
      }

      template {
        destination     = "local/mc/config.json"
        change_mode     = "noop"
        data = <<EOF
{
  "aliases": {
    "local": {
      "url": "http://s3.service.consul:9000",
      "accessKey": "[[.object_storage.user.name]]",
      "secretKey": "[[.object_storage.user.name]]",
      "api": "s3v4",
      "path": "on"
    }
  }
}
EOF
      }
      template {
        destination     = "local/statistics.yaml"
        change_mode     = "noop"
        data = <<EOF
replicate:
  apiVersion: v1
  source:
    type: minio
    bucket: statistics
    prefix: ""
  target:
    type: minio
    bucket: central-statistics
    endpoint: "https://s3.lofar.net"
    credentials:
      accessKey: [[.object_storage.user.name]]
      secretKey: [[.object_storage.user.name]]
  flags:
    filter:
      newerThan: "10m"
      EOF
      }
    }
  }
}
