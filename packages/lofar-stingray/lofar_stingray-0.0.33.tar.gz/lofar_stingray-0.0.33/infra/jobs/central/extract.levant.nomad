job "statistics-extract" {
  datacenters = ["nl-north"]
  type        = "batch"
  namespace   = "statistics"

  parameterized {
    payload       = "forbidden"
    meta_required = ["observation_id", "station", "antenna_field", "begin", "end", "source", "destination"]
    meta_optional = ["metadata_bst", "metadata_sst", "metadata_xst", "XST_subbands"]
  }

  [[ range $type := "bst xst sst" | split " " ]]
  group "aggregate-[[ $type ]]" {
    count = 1

    network {
      mode = "bridge"
    }

    ephemeral_disk {
      size = 110 # nomad wants 100 MiB for log storage, so provide at least that
    }

    task "stingray" {
      driver = "docker"
      config {
        image = "git.astron.nl:5000/lofar2.0/stingray/stingray:[[$.image_tag]]"

        entrypoint = [
            "l2ss-stingray-extract",
            "--endpoint", "s3.lofar.net",
            "--secure",
            "${NOMAD_META_station}",
            "${NOMAD_META_antenna_field}",
            "[[ $type ]]",
            "${NOMAD_META_begin}",
            "${NOMAD_META_end}",
            "${NOMAD_META_source}",
            "${NOMAD_META_destination}/L${NOMAD_META_observation_id}/[[ $type ]]/L${NOMAD_META_observation_id}_${NOMAD_META_station}_${NOMAD_META_antenna_field}_[[ $type ]].h5",
            "--user-metadata", "${NOMAD_META_metadata_[[ $type ]]}"
        ]
      }

      env {
        MINIO_ROOT_USER     = "[[$.object_storage.user.name]]"
        MINIO_ROOT_PASSWORD = "[[$.object_storage.user.pass]]"
      }

      resources {
        cpu    = 10
        memory = 512
        memory_max = 4096
      }
    }
  }
  [[ end ]]
}
