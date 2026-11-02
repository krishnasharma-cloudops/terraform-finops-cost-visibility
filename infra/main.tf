resource "azurerm_resource_group" "finops" {
  name     = "rg-ks-finops-demo"
  location = var.location
  tags = {
    ManagedBy   = "Terraform"
    Project     = "finops-portfolio-demo"
    Environment = "dev"
  }
}

resource "azurerm_storage_account" "example" {
  name                            = var.storage_account_name
  resource_group_name             = azurerm_resource_group.finops.name
  location                        = azurerm_resource_group.finops.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  public_network_access_enabled   = false
  tags = {
    ManagedBy   = "Terraform"
    Project     = "finops-portfolio-demo"
    Environment = "dev"
  }
}

output "storage_account_name" {
  value = azurerm_storage_account.example.name
}
