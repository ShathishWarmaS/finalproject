import boto3

def create_cloudwatch_alarm(instance_id):
    client = boto3.client('cloudwatch')
    
    alarm_name = 'HighCPUAlarm'
    alarm_description = 'Alarm triggered when CPU usage exceeds 80% for 5 consecutive minutes'
    metric_name = 'CPUUtilization'
    namespace = 'AWS/EC2'
    period = 60
    evaluation_periods = 5
    threshold = 80.0
    comparison_operator = 'GreaterThanOrEqualToThreshold'
    alarm_actions = ['ARN_OF_SNS_TOPIC']  # Replace with the ARN of your SNS topic
    
    response = client.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription=alarm_description,
        ActionsEnabled=True,
        AlarmActions=alarm_actions,
        MetricName=metric_name,
        Namespace=namespace,
        Statistic='Average',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        Period=period,
        EvaluationPeriods=evaluation_periods,
        Threshold=threshold,
        ComparisonOperator=comparison_operator
    )
    
    print("CloudWatch alarm created successfully!")

# Replace 'YOUR_INSTANCE_ID' with the actual instance ID
create_cloudwatch_alarm('YOUR_INSTANCE_ID')
