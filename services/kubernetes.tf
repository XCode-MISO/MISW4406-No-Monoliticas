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

        container {
          name  = "seguridad"
          image = "us-central1-docker.pkg.dev/nomonoliticas-452502/saludtech/seguridad:latest"

          
          liveness_probe {
            http_get {
              path = "/"
              port = 5000
            }
            initial_delay_seconds = 10
          }

          env {
            name  = "BROKER_HOST"
            value = "34.171.186.238"
          }

          env {
            name  = "DB_HOSTNAME"
            value = "35.223.246.149"
          }

          port {
            container_port = 5000
          }
          
          resources {
            limits = {
              cpu    = "0.5"
              memory = "256Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
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
    }

    type = "ClusterIP"  # Change to "LoadBalancer" if needed
  }
}
resource "kubernetes_deployment" "autorizacion" {
  metadata {
    name = "autorizacion"
    labels = {
      app = "autorizacion"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "autorizacion"
      }
    }

    template {
      metadata {
        labels = {
          app = "autorizacion"
        }
      }

      spec {

        container {
          name  = "autorizacion"
          image = "us-central1-docker.pkg.dev/nomonoliticas-452502/saludtech/autorizacion:latest"

          liveness_probe {
            http_get {
              path = "/"
              port = 5000
            }
            initial_delay_seconds = 10
          }

          env {
            name  = "BROKER_HOST"
            value = "34.171.186.238"
          }

          env {
            name  = "DB_HOSTNAME"
            value = "35.223.246.149"
          }

          port {
            container_port = 5000
          }
          resources {
            limits = {
              cpu    = "0.5"
              memory = "256Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }
        }

        restart_policy = "Always"
      }
    }
  }
}

resource "kubernetes_service" "autorizacion" {
  metadata {
    name = "autorizacion"
    labels = {
      app = "autorizacion"
    }
  }

  spec {
    selector = {
      app = "autorizacion"
    }

    port {
      name        = "http"
      port        = 5000      # Service port
    }

    type = "ClusterIP"  # Change to "LoadBalancer" if needed
  }
}

resource "kubernetes_deployment" "bff" {
  metadata {
    name = "bff"
    labels = {
      app = "bff"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "bff"
      }
    }

    template {
      metadata {
        labels = {
          app = "bff"
        }
      }

      spec {
        container {
          name  = "bff"
          image = "us-central1-docker.pkg.dev/nomonoliticas-452502/saludtech/bff:latest"

          liveness_probe {
            http_get {
              path = "/"
              port = 8000
            }
            initial_delay_seconds = 10
          }

          env {
            name  = "BROKER_HOST"
            value = "34.171.186.238"
          }
          env {
            name  = "STA_ENV"
            value = "autorizacion.default.svc.cluster.local"
          }
          
          env {
            name  = "STA_PORT"
            value = "5000"
          }

          port {
            container_port = 8000
          }
          resources {
            limits = {
              cpu    = "0.5"
              memory = "256Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }
        }

        restart_policy = "Always"
      }
    }
  }
}

resource "kubernetes_service" "bff" {
  metadata {
    name = "bff"
    labels = {
      app = "bff"
    }
  }

  spec {
    selector = {
      app = "bff"
    }

    port {
      name        = "http"
      port        = 8000      # Service port
    }

    type = "LoadBalancer"  # Change to "LoadBalancer" if needed
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

        container {
          name  = "ingestion-datos"
          image = "us-central1-docker.pkg.dev/nomonoliticas-452502/saludtech/ingestion_datos:latest"

          liveness_probe {
            http_get {
              path = "/"
              port = 8000
            }
            initial_delay_seconds = 10
          }

          env {
            name  = "BROKER_HOST"
            value = "34.171.186.238"
          }

          port {
            container_port = 8000
          }
          resources {
            limits = {
              cpu    = "0.5"
              memory = "256Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
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
      port        = 8000      # Service port
    }

    type = "ClusterIP"  # Change to "LoadBalancer" if needed
  }
}