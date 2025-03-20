job "grafana-rpc-server" {
  datacenters = ["stat"]
  type        = "service"
  reschedule {
    unlimited      = true
    delay          = "30s"
    delay_function = "constant"
  }
  group "grafana-rpc-server" {
    network {
      mode = "bridge"

      port "grpc" {
        static       = "50051"
        host_network = "external"
      }

      port "metrics" {
        static       = "8000"
        host_network = "station"
      }
    }

    service {
      name = "rpc"
      port = "grpc"
    }

    service {
      tags = ["scrape"]
      name = "rpc-metrics"
      port = "metrics"

      meta {
        metrics_path = "/"
      }
    }

    task "grafana-rpc-server" {
      driver = "docker"

      config {
        image      = "git.astron.nl:5000/lofar2.0/opah/opah:[[ $.image_tag ]]"
        entrypoint = [""]
        command    = "l2ss-opah-grafana-rpc-server"
        args       = [
          "--port", "${NOMAD_PORT_rpc}",
          "--metrics-port", "${NOMAD_PORT_metrics}",
          "--stations", "localhost"
        ]
      }

      resources {
        cpu    = 25
        memory = 512
      }
    }
  }
}
