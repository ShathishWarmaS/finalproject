import boto3

def create_cloudwatch_alarm(instance_id):
    # Create a Boto3 client for CloudWatch
    client = boto3.client('cloudwatch')
    
    # Define the parameters for the CloudWatch alarm
    alarm_name = 'HighCPUAlarm'  # Name of the alarm
    alarm_description = 'Alarm triggered when CPU usage exceeds 80% for 5 consecutive minutes'  # Description of the alarm
    metric_name = 'CPUUtilization'  # Name of the metric to monitor (CPU usage)
    namespace = 'AWS/EC2'  # Namespace of the metric
    period = 60  # Length of time in seconds to evaluate the metric
    evaluation_periods = 5  # Number of consecutive periods the condition must be met to trigger the alarm
    threshold = 80.0  # Threshold value for the metric
    comparison_operator = 'GreaterThanOrEqualToThreshold'  # Comparison operator to determine when the alarm is triggered
    alarm_actions = ['ARN_OF_SNS_TOPIC']  # List of actions to perform when the alarm is triggered
    # Replace 'ARN_OF_SNS_TOPIC' with the ARN of your SNS topic where you want to send the alert
    
    # Create the CloudWatch alarm using the put_metric_alarm method
    response = client.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription=alarm_description,
        ActionsEnabled=True,
        AlarmActions=alarm_actions,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic='Average',  # Statistic to evaluate for the metric
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],  # Dimensions to filter the metric
        Period=period,
        EvaluationPeriods=evaluation_periods,
        Threshold=threshold,
        ComparisonOperator=comparison_operator
    )
    
    # Print a success message after creating the alarm
    print("CloudWatch alarm created successfully!")

# Replace 'YOUR_INSTANCE_ID' with the actual instance ID
create_cloudwatch_alarm('YOUR_INSTANCE_ID')
