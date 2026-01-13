# resource "google_secret_manager_secret" "github-token-secret" {
#   secret_id = "github-token-secret"

#   replication {
#     auto {}
#   }
# }

# resource "google_secret_manager_secret_version" "github-token-secret-version" {
#   secret = google_secret_manager_secret.github-token-secret.id
#   secret_data = file("my-github-token.txt")
# }

# data "google_iam_policy" "p4sa-secretAccessor" {
#   binding {
#     role = "roles/secretmanager.secretAccessor"
#     members = ["serviceAccount:service-123456789@gcp-sa-cloudbuild.iam.gserviceaccount.com"]
#   }
# }

# resource "google_secret_manager_secret_iam_policy" "policy" {
#   secret_id = google_secret_manager_secret.github-token-secret.secret_id
#   policy_data = data.google_iam_policy.p4sa-secretAccessor.policy_data
# }

