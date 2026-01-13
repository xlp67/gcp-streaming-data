data "google_secret_manager_secret_version" "latest" {
  project = var.project_id
  secret  = var.token_secret_id
}

resource "google_cloudbuildv2_connection" "this" {
  location = var.region
  name     = var.cloudbuild_connection_name

  github_config {   
    authorizer_credential {
      oauth_token_secret_version = data.google_secret_manager_secret_version.latest.id
      # exemplo do valor gerado:
      # projects/carbon-hulling-480701-e8/secrets/github/versions/latest
    }
  }
}

# resource "google_cloudbuild_trigger" "this" {
#   name     = "trigger-on-src-change-only"
#   location = var.region

#   repository_event_config {
#     repository = google_cloudbuildv2_repository.this.id
#     push {
#       branch = "^main$" 
#     }
#   }
#   included_files = [
#     "src/**",           
#     "requirements.txt",  
#     "Dockerfile",      
#     "setup.py"       
#   ]

#   ignored_files = [
#     "infra/**",
#     "README.md",
#     "tests/**"
#   ]

#   git_file_source {
#     path      = "cloudbuild.yaml"
#     uri       = google_cloudbuildv2_repository.my_repo.remote_uri
#     repo_type = "GITHUB"
#   }

#   substitutions = {
#     _BUCKET_TEMPLATES = var.bucket_name
#     _REPO_NAME        = var.artifact_repo_name
#     _REGION           = var.region
#   }
# }
