# Infrastructure Cost Analysis & FinOps — Terraform, Infracost, OpenCost

**Portfolio implementation** of the FinOps skills listed on my resume. It demonstrates:

1. Terraform Azure resources for **pre-deployment cost estimation with Infracost**.
2. Python reporting for **Infracost and OpenCost API JSON** using no external dependencies.
3. OpenCost API integration with an **existing Kubernetes/OpenCost installation**.

**Important:** Sample cost values are **synthetic examples**, **not real bills**, actual savings, or deployment results. An OpenCost cluster is **not** provisioned by this repository; setting one up is optional and may cost money.

## Run immediately (no cloud login needed)

```powershell
python scripts/cost_report.py --infracost samples/infracost-example.json --opencost samples/opencost-example.json
python scripts/cost_report.py --infracost samples/infracost-example.json --opencost samples/opencost-example.json --markdown reports/cost-report.md
python -m unittest discover -s tests -v
```

## Real Infracost analysis (requires Infracost API key)

```powershell
infracost auth login
infracost breakdown --path infra --format json --out-file local-infracost.json
python scripts/cost_report.py --infracost local-infracost.json
```

`local-infracost.json` might reveal resource configuration/cost estimates and should not be committed. Infracost estimates are not provider invoices; usage-dependent costs may require additional inputs.

## Azure resource demo (optional, billable)

```powershell
az login
cd infra
Copy-Item terraform.tfvars.example terraform.tfvars
# Set your subscription ID and a globally unique storage account name
terraform init
terraform plan -out=deploy.tfplan
terraform apply deploy.tfplan
# After validating the demo:
terraform destroy
```

## OpenCost from an existing Kubernetes cluster (optional)

Follow [OpenCost installation](https://opencost.io/docs/installation/install/) for an existing cluster. Example API usage:

```powershell
kubectl -n opencost port-forward deployment/opencost 9003:9003
# In a second terminal, if your deployment exposes this endpoint:
Invoke-WebRequest 'http://localhost:9003/allocation/compute?window=7d&aggregate=namespace' -OutFile local-opencost.json
python scripts/cost_report.py --opencost local-opencost.json
```

OpenCost services and route names vary by version/install; verify the official [API documentation](https://opencost.io/docs/integrations/api/).

## CI
GitHub Actions runs Python unit tests and Terraform format+validation; it does **not** apply Azure resources or fetch cost secrets. Never commit a real Infracost API key.

**Author:** Krishna Sharma · FinOps portfolio implementation
