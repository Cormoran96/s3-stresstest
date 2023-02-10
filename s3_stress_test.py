import boto3
import os
import argparse
import matplotlib.pyplot as plt
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Create an S3 client
s3 = boto3.client('s3', endpoint_url='https://s3.example.com',
                  aws_access_key_id='XXXXXXXXXXXXXXXXXx',
                  aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# Define the object prefix
object_prefix = 'stress-test/'

# Generate random data
def generate_data(size):
    return os.urandom(size)

# Upload object to S3
def upload_object(bucket_name, object_key, data):
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)

# Parse the command-line arguments
parser = argparse.ArgumentParser(description='s3 Stress Test')
parser.add_argument('-n', '--num_objects', type=int, default=50, help='Number of objects to upload')
parser.add_argument('-b', '--bucket_name', type=str, default='testnmg', help='Name of the S3 bucket')
parser.add_argument('-r', '--ratio', type=int, default=2, help='Ratio by which the object size will be multiplied with each iteration')
args = parser.parse_args()

# Upload objects in parallel
sizes = []
times = []
object_size = 1024 * 1024 * 5 # 5 MB
executor = ThreadPoolExecutor(max_workers=5)
futures = []
for i in range(args.num_objects):
    object_key = f'{object_prefix}{i}'
    data = generate_data(object_size)
    start_time = time.time()
    futures.append(executor.submit(upload_object, args.bucket_name, object_key, data))
    end_time = time.time()
    sizes.append(object_size)
    times.append((end_time - start_time))
    object_size *= args.ratio

# Wait for all the futures to complete
for future in tqdm(futures, total=args.num_objects, desc="Upload Progress"):
    future.result()

# Calculate transfer rates in MB/s
transfer_rates = [size / (time * 1024 * 1024) for size, time in zip(sizes, times)]

# Calculate average transfer rate
avg_transfer_rate = np.mean(transfer_rates)

# Plot the results
plt.plot(transfer_rates)
plt.axhline(y=avg_transfer_rate, color='r', linestyle='--')
plt.xlabel('Object Index')
plt.ylabel('Transfer Rate (MB/s)')
plt.title('s3 Stress Test Results')
plt.show()

