# Upload only this repository to GitHub

1. Visit https://github.com/new and create an empty **public** repository named `terraform-finops-cost-visibility` under `krishnasharma-cloudops`.
2. Extract this project to its own folder. Open PowerShell **inside that folder** (where `README.md` is).
3. Run:

```powershell
git init -b main
git add .
git status
git commit -m "Initial commit: terraform-finops-cost-visibility"
git remote add origin https://github.com/krishnasharma-cloudops/terraform-finops-cost-visibility.git
git push -u origin main
```

**If Git complains about author identity:**

```powershell
git config --global user.name "Krishna Sharma"
git config --global user.email "krishna.sharma.cloud.ops@gmail.com"
```

**Do not run these commands inside your existing portfolio, EV PULSE or PayPilot AI folders.** Never commit cloud passwords/state files. Deploying Terraform is optional and separate from GitHub upload.
