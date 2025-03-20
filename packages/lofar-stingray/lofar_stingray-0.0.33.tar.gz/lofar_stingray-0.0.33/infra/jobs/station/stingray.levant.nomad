job "statistics" {
  datacenters = ["stat"]
  type        = "service"

  reschedule {
    unlimited = true
    delay = "30s"
    delay_function = "constant"
  }

  group "stingray-metadata" {
    count = 1

    network {
      mode = "bridge"
    }

      task "stingray-record-metadata" {
          driver = "docker"

          config {
              image = "git.astron.nl:5000/lofar2.0/stingray/stingray:[[$.image_tag]]"

              entrypoint = [
                  "l2ss-stingray-forward",
                  "--datatype=json",
                  "zmq+tcp://device-metadata.service.consul:6001/metadata?content-type=application%2Fjson",
                  "s3://statistics/[[$.station]]/metadata"
              ]
          }

          env {
              MINIO_ROOT_USER = "[[$.object_storage.user.name]]"
              MINIO_ROOT_PASSWORD = "[[$.object_storage.user.pass]]"
          }


          resources {
              cpu    = 10
              memory = 512
          }
      }
  }

  [[ range $af, $fields := $.stingray ]]
  [[ range $st, $ip := $fields ]]
  group "stingray-[[ $af ]]-[[ $st ]]" {
    count = 1

    network {
      mode = "cni/statistics"

      cni {
        args {
          IP = "[[ $ip ]]",
          GATEWAY = "10.99.250.250"
        }
      }
    }

    service {
        name = "statistics-[[ $af ]]-[[ $st ]]-zmq"
        port = 6001
        address_mode = "alloc"

        check {
            type = "tcp"
            interval = "20s"
            timeout = "5s"
            address_mode = "alloc"
        }
    }

    service {
        name = "statistics-[[ $af ]]-[[ $st ]]-udp"
        port = 5001
        address_mode = "alloc"
    }

    service {
        name = "stingray-[[ $af ]]-[[ $st ]]-publish-metrics"
        tags = ["scrape"]
        port = 8000
        address_mode = "alloc"
    }

    service {
        name = "stingray-[[ $af ]]-[[ $st ]]-record-metrics"
        tags = ["scrape"]
        port = 8001
        address_mode = "alloc"
    }

    task "stingray-publish-[[ $af ]]-[[ $st ]]" {
        driver = "docker"

        config {
            image = "git.astron.nl:5000/lofar2.0/stingray/stingray:[[ $.image_tag ]]"

            entrypoint = [
                "l2ss-stingray-publish",
                "[[ $.station ]]",
                "[[ $af ]]",
                "[[ $st ]]",
                "udp://0.0.0.0:5001",
                "--port=6001"
            ]
        }

        resources {
            cpu    = 10
            memory = 512
        }
    }

    task "stingray-record-[[ $af ]]-[[ $st ]]" {
        driver = "docker"

        config {
            image = "git.astron.nl:5000/lofar2.0/stingray/stingray:[[$.image_tag]]"

            entrypoint = [
                "l2ss-stingray-forward",
                "--datatype=json",
                "zmq+tcp://localhost:6001/[[ $st ]]/[[ $af ]]/",
                "s3://statistics/[[$.station]]/[[ $st ]]/[[ $af ]]",
                "--metrics-port=8001"
            ]
        }

        env {
            MINIO_ROOT_USER = "[[$.object_storage.user.name]]"
            MINIO_ROOT_PASSWORD = "[[$.object_storage.user.pass]]"
        }

        resources {
            cpu    = 10
            memory = 512
        }
    }
  }
  [[ end ]]
  [[ end ]]
}
