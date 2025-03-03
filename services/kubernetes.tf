provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "seguridad" {
  metadata {
    name = "seguridad"
    labels = {
      app = "seguridad"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "seguridad"
      }
    }

    template {
      metadata {
        labels = {
          app = "seguridad"
        }
      }

      spec {
        hostname = "seguridad"

        container {
          name  = "seguridad"
          image = "us-central1-docker.pkg.dev/nomonoliticas-452502/saludtech/seguridad"

          env {
            name  = "BROKER_HOST"
            value = "pulsar-proxy.default.svc.cluster.local."
          }

          port {
            container_port = 5000
          }

          # Optional: Health checks
          readiness_probe {
            http_get {
              path = "/"
              port = 5000
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 5000
            }
            initial_delay_seconds = 15
            period_seconds        = 20
          }
        }

        restart_policy = "Always"
      }
    }
  }
}

resource "kubernetes_service" "seguridad" {
  metadata {
    name = "seguridad"
    labels = {
      app = "seguridad"
    }
  }

  spec {
    selector = {
      app = "seguridad"
    }

    port {
      name        = "http"
      port        = 5000      # Service port
      target_port = 5000      # Container port
    }

    type = "NodePort"  # Change to "LoadBalancer" if needed
  }
}

resource "kubernetes_deployment" "ingestion-datos" {
  metadata {
    name = "ingestion-datos"
    labels = {
      app = "ingestion-datos"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "ingestion-datos"
      }
    }

    template {
      metadata {
        labels = {
          app = "ingestion-datos"
        }
      }

      spec {
        hostname = "ingestion-datos"

        container {
          name  = "ingestion-datos"
          image = "us-central1-docker.pkg.dev/nomonoliticas-452502/saludtech/ingestion_datos"

          env {
            name  = "BROKER_HOST"
            value = "pulsar-proxy.default.svc.cluster.local."
          }

          port {
            container_port = 5000
          }

          # Optional: Health checks
          readiness_probe {
            http_get {
              path = "/"
              port = 5000
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 5000
            }
            initial_delay_seconds = 15
            period_seconds        = 20
          }
        }

        restart_policy = "Always"
      }
    }
  }
}

resource "kubernetes_service" "ingestion-datos" {
  metadata {
    name = "ingestion-datos"
    labels = {
      app = "ingestion-datos"
    }
  }

  spec {
    selector = {
      app = "ingestion-datos"
    }

    port {
      name        = "http"
      port        = 5000      # Service port
      target_port = 5000      # Container port
    }

    type = "NodePort"  # Change to "LoadBalancer" if needed
  }
}