job "cryptocoryne-certbot" {
  datacenters = ["nl-north"]
  type        = "batch"
  namespace   = "infrastructure"

  periodic {
    cron             = "*/5 * * * * *"
    prohibit_overlap = true
  }

  group "cryptocoryne" {
    count = 1

    network {
      mode = "bridge"
    }

    vault {
      policies = ["default"]
    }

    task "certbot" {
      driver = "docker"
      config {
        image = "git.astron.nl:5000/lofar2.0/cryptocoryne/cryptocoryne:[[$.image_tag]]"

        entrypoint = [
            "l2ss-cryptocoryne-certbot"
        ]
      }

      env {
        CONSUL_HTTP_ADDR = "consul.central.lofar.net:8500"
        VAULT_ADDR = "https://vault.lofar.net"
        VAULT_TOKEN =  "${VAULT_TOKEN}"
      }

      resources {
        cpu    = 256
        memory = 512
      }
    }
  }
}
