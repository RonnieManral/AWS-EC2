import boto3
from datetime import datetime, timedelta
from operator import itemgetter

AccessKey = "AKIATBKX7DBGYUKS4PR"
SecretKey = "DSoozXlrXxxGAmePhHztum7G5uaMTjX/q4qH5cd"


now = datetime.utcnow()  # Now time in UTC format
past = now - timedelta(minutes=60)  # Minus 60 minutes

# Amazon Cloud Watch connection
client_cw = boto3.client(
    'cloudwatch',
    aws_access_key_id = AccessKey,
    aws_secret_access_key = SecretKey,

)

# Amazon EC2 connection
client_ec2 = boto3.client(
    'ec2',
    aws_access_key_id = AccessKey,
    aws_secret_access_key = SecretKey,

)

response = client_ec2.describe_instances()  # Get all instances from Amazon EC2

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:

        # This will print output the value of the Dictionary key 'InstanceId'
        print(instance["InstanceId"])

        # Get CPU Utilization for each InstanceID
        CPUUtilization = client_cw.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance["InstanceId"]}],
            StartTime=past,
            EndTime=now,
            Period=600,
            Statistics=['Average'])

        datapoints = CPUUtilization['Datapoints']                               # CPU Utilization results
        last_datapoint = sorted(datapoints, key=itemgetter('Timestamp'))[-1]    # Last result
        utilization = last_datapoint['Average']                                 # Last utilization
        load = round((utilization / 100.0), 3)                                  # Last utilization in %
        timestamp = str(last_datapoint['Timestamp'])                            # Last utilization timestamp
        print("{0} load at {1}".format(load, timestamp))

        # Send mail if CPU load more than 50%
        if load > 0:
            print("load above 60%")

