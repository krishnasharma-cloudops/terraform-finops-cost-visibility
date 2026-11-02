# FinOps interview discussion

1. **Shift-left cost:** Estimate Terraform changes with Infracost *before* `terraform apply`.
2. **Kubernetes cost attribution:** OpenCost aggregates costs of Kubernetes workloads by namespace/pod/deployment on an existing cluster.
3. **Tags/labels:** Cloud tags and Kubernetes labels help associate costs with teams/environments.
4. **Trend analysis:** Compare consistent periods with real measurements; avoid mixing estimated monthly spend and 7-day cluster allocation.
5. **Optimization:** Discuss idle resources and SKU selection only after verifying real utilization data.

The repository demonstrates the interface/reporting flow, not validated production cost savings.
