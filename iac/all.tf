terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.20"
    }
  }
}

provider "aws" {
  region = local.region
}

data "aws_availability_zones" "available" {}

# External data source to get current IP
data "http" "my_ip" {
  url = "http://checkip.amazonaws.com/"
}


locals {
  name   = "data-workshop"
  region = "ap-northeast-2"
  my_ip = "${chomp(data.http.my_ip.body)}/32"

  vpc_cidr = "10.0.0.0/16"
  azs      = slice(data.aws_availability_zones.available.names, 0, 2)

  tags = {
    identifier = local.name
    terraform  = true
  }
}

################################################################################
# VPC Module
################################################################################

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = local.name
  cidr = local.vpc_cidr

  azs              = local.azs
  private_subnets  = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k)]
  public_subnets   = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k + 4)]
  database_subnets = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k + 8)]

  create_database_subnet_group  = true
  manage_default_network_acl    = false
  manage_default_route_table    = false
  manage_default_security_group = false

  enable_dns_hostnames = true
  enable_dns_support   = true

#   enable_nat_gateway = true
#   single_nat_gateway = true

  enable_dhcp_options        = true
  map_public_ip_on_launch    = true

  tags = local.tags
}

resource "aws_security_group" "common_sg" {
  name        = "${local.name}-common-sg"
  description = "${local.name}-common-sg"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "Allow all inbound traffic from self"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
  }

  ingress {
    description = "Allow SSH from current IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.my_ip]
  }


  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.tags
}


data "aws_iam_policy" "administrator_access" {
  arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

data "aws_iam_policy" "ssm_managed_instance_core" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role" "ec2_admin_role" {
  name = "${local.name}-ec2-admin-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ec2_admin_attach" {
  role       = aws_iam_role.ec2_admin_role.name
  policy_arn = data.aws_iam_policy.administrator_access.arn
}

resource "aws_iam_role_policy_attachment" "ssm_attach" {
  role       = aws_iam_role.ec2_admin_role.name
  policy_arn = data.aws_iam_policy.ssm_managed_instance_core.arn
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "${local.name}-ec2-instance-profile"
  role = aws_iam_role.ec2_admin_role.name
}

# Key Pair 생성
resource "tls_private_key" "private_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "deployer" {
  key_name   = "${local.name}-key.pem"
  public_key = tls_private_key.private_key.public_key_openssh
}

resource "local_file" "private_key" {
  content  = tls_private_key.private_key.private_key_pem
  filename = "${path.module}/${local.name}-key.pem"
}

# Bastion EC2 인스턴스 생성
resource "aws_instance" "bastion" {
  ami           = "ami-045f2d6eeb07ce8c0"  # Amazon Linux 2023 AMI
  instance_type = "m5.xlarge"
  subnet_id     = module.vpc.public_subnets[0]
  key_name      = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.common_sg.id]

  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name

  tags = merge(local.tags, {
    Name = "bastion&TestServer"
  })

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum -y install git jq
              sudo dnf -y localinstall https://dev.mysql.com/get/mysql80-community-release-el9-4.noarch.rpm
              sudo dnf -y install mysql mysql-community-client
              # docker install
              sudo yum -y install docker
              sudo service docker start
              sudo chkconfig docker on
              sudo usermod -a -G docker $USER
              cd /home/ec2-user
              git clone https://github.com/color275/new_datalake.git

              BASH_PROFILE_PATH="/home/ec2-user/.bash_profile"

              SECRET=$(aws secretsmanager get-secret-value --secret-id ${replace(module.aurora.cluster_master_user_secret[0].secret_arn, "!", "\\!")} --query SecretString --output text)
              DBUSER=$(echo $SECRET | jq -r .username)
              PASSWORD=$(echo $SECRET | jq -r .password)
              PRIMARY_HOST="${module.aurora.cluster_endpoint}"
              READONLY_HOST="${module.aurora.cluster_endpoint}"
              echo "export DBUSER=${DBUSER}" >> $BASH_PROFILE_PATH
              echo "export PASSWORD=${PASSWORD}" >> $BASH_PROFILE_PATH
              echo "export PRIMARY_HOST=${PRIMARY_HOST}" >> $BASH_PROFILE_PATH
              echo "export READONLY_HOST=${READONLY_HOST}" >> $BASH_PROFILE_PATH
              echo "export PRIMARY_PORT=3306" >> $BASH_PROFILE_PATH
              echo "export READONLY_PORT=3306" >> $BASH_PROFILE_PATH
              echo "export PRIMARY_DBNAME=ecommerce" >> $BASH_PROFILE_PATH
              echo "export READONLY_DBNAME=ecommerce" >> $BASH_PROFILE_PATH
              mysql -h ${module.aurora.cluster_endpoint} -u $DBUSER -p$PASSWORD < /home/ec2-user/new_datalake/src/ecommerce/sample_data.sql
              echo "alias ss='mysql -h ${module.aurora.cluster_endpoint} -u $DBUSER -p$PASSWORD'" >> $BASH_PROFILE_PATH

              EOF
  
  depends_on = [
    module.aurora
  ]

}


################################################################################
# Secret Manager 에 DB 접속 정보 저장
################################################################################
# resource "aws_secretsmanager_secret" "aurora_mysql_secret" {
#   name        = "aurora-mysql-secret"
#   description = "Aurora MySQL master user credentials"
# }

# resource "aws_secretsmanager_secret_version" "aurora_mysql_secret_version" {
#   secret_id     = aws_secretsmanager_secret.aurora_mysql_secret.id
#   secret_string = jsonencode({
#     username = "admin"
#     password = "Admin1234"
#   })
# }

################################################################################
# RDS Aurora Module
################################################################################
module "aurora" {
  source = "terraform-aws-modules/rds-aurora/aws"

  name            = local.name
  engine          = "aurora-mysql"
  engine_version  = "8.0"
  # master_username = jsondecode(aws_secretsmanager_secret_version.aurora_mysql_secret_version.secret_string).username
  # master_password = jsondecode(aws_secretsmanager_secret_version.aurora_mysql_secret_version.secret_string).password
  manage_master_user_password = true
  master_username = "admin"

  instances = {
    1 = {
      identifier     = "mysql-1"
      instance_class = "db.r5.large"
    }
    2 = {
      identifier     = "mysql-2"
      instance_class = "db.r5.large"
    }
  }

  vpc_id               = module.vpc.vpc_id
  db_subnet_group_name = module.vpc.database_subnet_group_name

  security_group_name = "${local.name}-db-sg"
  security_group_rules = {
    vpc_ingress = {
      cidr_blocks = module.vpc.private_subnets_cidr_blocks,
    },
    common_sg_ingress = {
      source_security_group_id = aws_security_group.common_sg.id,
      from_port                = 3306,
      to_port                  = 3306,
      protocol                 = "tcp"
    }
  }


  apply_immediately   = true
  skip_final_snapshot = true

  create_db_cluster_parameter_group      = true
  db_cluster_parameter_group_name        = local.name
  db_cluster_parameter_group_family      = "aurora-mysql8.0"
  db_cluster_parameter_group_description = "${local.name} example cluster parameter group"
  db_cluster_parameter_group_parameters = [
    {
      name         = "connect_timeout"
      value        = 120
      apply_method = "immediate"
      }, {
      name         = "innodb_lock_wait_timeout"
      value        = 300
      apply_method = "immediate"
      }, {
      name         = "log_output"
      value        = "FILE"
      apply_method = "immediate"
      }, {
      name         = "max_allowed_packet"
      value        = "67108864"
      apply_method = "immediate"
      }, {
      name         = "aurora_parallel_query"
      value        = "OFF"
      apply_method = "pending-reboot"
      }, {
      name         = "binlog_format"
      value        = "ROW"
      apply_method = "pending-reboot"
      }, {
      name         = "log_bin_trust_function_creators"
      value        = 1
      apply_method = "immediate"
      }, {
      name         = "tls_version"
      value        = "TLSv1.2"
      apply_method = "pending-reboot"
    },
    {
      name         = "lower_case_table_names"
      value        = "1"
      apply_method = "pending-reboot"
    },
    {
      name         = "time_zone"
      value        = "asia/seoul"
      apply_method = "pending-reboot"
    }
  ]

  create_db_parameter_group      = true
  db_parameter_group_name        = local.name
  db_parameter_group_family      = "aurora-mysql8.0"
  db_parameter_group_description = "${local.name}"
  db_parameter_group_parameters = [
    {
      name         = "connect_timeout"
      value        = 60
      apply_method = "immediate"
      }, {
      name         = "general_log"
      value        = 0
      apply_method = "immediate"
      }, {
      name         = "innodb_lock_wait_timeout"
      value        = 300
      apply_method = "immediate"
      }, {
      name         = "log_output"
      value        = "FILE"
      apply_method = "pending-reboot"
      }, {
      name         = "long_query_time"
      value        = 5
      apply_method = "immediate"
      }, {
      name         = "max_connections"
      value        = 2000
      apply_method = "immediate"
      }, {
      name         = "slow_query_log"
      value        = 1
      apply_method = "immediate"
      }, {
      name         = "log_bin_trust_function_creators"
      value        = 1
      apply_method = "immediate"
    }
  ]

  enabled_cloudwatch_logs_exports = ["audit", "error", "general", "slowquery"]

  tags = local.tags
}

################################################################################
# OUTPUT
################################################################################
# Public IP 출력
output "bastion_public_ip" {
  description = "The public IP of the bastion instance"
  value       = aws_instance.bastion.public_ip
}

output "connection_instructions" {
  description = "Instructions to connect to the Bastion instance"
  value       = "chmod 400 ${local.name}-key.pem; ssh -i ${local.name}-key.pem ec2-user@${aws_instance.bastion.public_ip}"
}

output "cluster_master_user_secret" {
  value = module.aurora.cluster_master_user_secret[0].secret_arn
}