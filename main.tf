# Create a VPC
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "MyVPC"
  }
}

# Create an internet gateway and associate it with the VPC
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id
}

# Associate the main route table with the VPC
resource "aws_main_route_table_association" "my_route_table_association" {
  vpc_id          = aws_vpc.my_vpc.id
  route_table_id  = aws_vpc.my_vpc.main_route_table_id
}

# Create a route to the internet gateway in the main route table
resource "aws_route" "internet_gateway_route" {
  route_table_id         = aws_vpc.my_vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.my_igw.id
}

# Create subnets in different availability zones
resource "aws_subnet" "subnet_az1" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "subnet_az2" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1b"
}

# Create a security group allowing inbound traffic on port 80
resource "aws_security_group" "instance_sg" {
  vpc_id = aws_vpc.my_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create EC2 instances
resource "aws_instance" "instances" {
  count         = 2
  ami           = "ami-007855ac798b5175e"  # Replace with your desired AMI ID
  instance_type = "t2.micro"
  subnet_id     = count.index % 2 == 0 ? aws_subnet.subnet_az1.id : aws_subnet.subnet_az2.id  # Alternate between the two subnets

  vpc_security_group_ids = [aws_security_group.instance_sg.id]

  # Add any other desired EC2 instance configuration options
}

# Create a load balancer
resource "aws_lb" "my_lb" {
  name               = "my-load-balancer"
  internal           = false
  load_balancer_type = "application"
  subnets            = [aws_subnet.subnet_az1.id, aws_subnet.subnet_az2.id]  # Use the two subnets from different availability zones

  security_groups = [aws_security_group.lb_sg.id]  # Attach security group for the load balancer
}

# Attach instances to the load balancer
resource "aws_lb_target_group" "lb_target_group" {
  name     = "my-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.my_vpc.id
}

resource "aws_lb_target_group_attachment" "attachment" {
  count            = length(aws_instance.instances)
  target_group_arn = aws_lb_target_group.lb_target_group.arn
  target_id        = aws_instance.instances[count.index].id
}
#Create a security group for the load balancer
resource "aws_security_group" "lb_sg" {
vpc_id = aws_vpc.my_vpc.id

ingress {
from_port = 80
to_port = 80
protocol = "tcp"
security_groups = [aws_security_group.instance_sg.id]
}
}