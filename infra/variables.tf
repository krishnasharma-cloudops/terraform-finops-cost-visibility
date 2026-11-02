variable "subscription_id" {
  type        = string
  description = "Azure subscription ID"
}
variable "location" {
  type    = string
  default = "centralindia"
}
variable "storage_account_name" {
  type        = string
  description = "Globally unique Azure Storage Account name, 3-24 lowercase letters and numbers."
  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "Provide a 3-24 character lowercase alphanumeric name."
  }
}
