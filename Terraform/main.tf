provider "google" {
  project = "bootcampproject-5-465900"
  region  = "us-central1"
}

resource "google_cloud_run_service" "app" {
  name     = "bootcampproject-5-service-main"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/bootcampproject-5-465900/bootcampproject-5-repo/app-image:latest"
        ports {
          container_port = 8080
        }
        env {
          name  = "BRANCH_NAME"
          value = "main"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "invoker" {
  service  = google_cloud_run_service.app.name
  location = google_cloud_run_service.app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}