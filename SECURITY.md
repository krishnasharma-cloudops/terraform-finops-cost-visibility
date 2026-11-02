# Security guidance

- Never commit cloud access keys, Azure service-principal secrets, GCP service-account JSON, tokens, `.tfstate`, `.tfvars`, Terraform plan binaries, or `.env`.
- Use short-lived identity federation / Azure CLI credentials when possible.
- `terraform plan` is a preview; `terraform apply` creates billable resources. Review it carefully.
- These repositories are educational and portfolio starter implementations. Harden before production usage.
- Check `git status` before pushing and rotate any credential that was accidentally committed.
