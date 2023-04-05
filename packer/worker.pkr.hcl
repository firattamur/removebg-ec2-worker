packer {

  required_plugins {

    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }

  }

}

locals {
  timestamp = regex_replace(timestamp(), "[- TZ:]", "")
}

variable "ami_prefix" {
  type    = string
  default = "removebg-worker"
}

source "amazon-ebs" "ubuntu" {

  ami_name      = "${var.ami_prefix}-${local.timestamp}"
  instance_type = "g5.xlarge"
  region        = "us-east-1"
  source_ami    = "ami-0a4caa099fc23090f"
  ssh_username  = "ubuntu"

}

variable "APP_AWS_REGION" {
  type = string
  sensitive = true
}

variable "APP_AWS_ACCESS_KEY_ID" {
  type = string
  sensitive = true
}

variable "APP_AWS_SECRET_ACCESS_KEY" {
  type = string
  sensitive = true
}

variable "APP_AWS_S3_BUCKET" {
  type = string
  sensitive = true
}

variable "APP_AWS_SQS_QUEUE_URL" {
  type = string
  sensitive = true
}

variable "APP_AWS_SNS_TOPIC_ARN" {
  type = string
  sensitive = true
}


build {

  name    = "removebg-worker"
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "file" {
    source      = "../"
    destination = "/home/ubuntu/removebg-worker"
  }

  provisioner "file" {
    source      = "../setup.sh"
    destination = "/tmp/setup.sh"
  }

  provisioner "file" {
    source      = "../startup.sh"
    destination = "/home/ubuntu/startup.sh"
  }

  provisioner "shell" {
    inline = [

      "echo 'APP_AWS_ACCESS_KEY_ID=${var.APP_AWS_ACCESS_KEY_ID}'          | sudo tee -a /etc/environment",
      "echo 'APP_AWS_SECRET_ACCESS_KEY=${var.APP_AWS_SECRET_ACCESS_KEY}'  | sudo tee -a /etc/environment",
      "echo 'APP_AWS_DEFAULT_REGION=${var.APP_AWS_DEFAULT_REGION}'        | sudo tee -a /etc/environment",
      "echo 'APP_AWS_BUCKET_NAME=${var.APP_AWS_BUCKET_NAME}'              | sudo tee -a /etc/environment",
      "echo 'APP_AWS_SQS_QUEUE_URL=${var.APP_AWS_SQS_QUEUE_URL}'          | sudo tee -a /etc/environment",
      "echo 'APP_AWS_SNS_TOPIC_ARN=${var.APP_AWS_SNS_TOPIC_ARN}'          | sudo tee -a /etc/environment",

      "chmod +x /tmp/setup.sh",
      "/tmp/setup.sh",

      "chmod +x /home/ubuntu/startup.sh",
      "sudo cp /home/ubuntu/startup.sh /etc/init.d/startup_script",
      "sudo ln -s /etc/init.d/startup_script /etc/rc2.d/S99startup_script",
      "if [ -e /etc/rc.local ]; then",
      "  sudo sed -i '/^exit 0/i \\/etc/init.d/startup_script' /etc/rc.local",
      "fi"

    ]

  }

}