import boto3
import os
import argparse
import matplotlib.pyplot as plt
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Create an S3 client
s3 = boto3.resource('s3', endpoint_url='https://s3.example.com',
                  aws_access_key_id='XXXXXXXXXXXXXXXXXx',
                  aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')


# Define the object prefix
object_prefix = 'stress-test/'

# Generate random data
def generate_data(size):
    return os.urandom(size)

# Upload object to S3
def upload_object(bucket, object_key, object_content):
    start = time.time()
    size = len(object_content)
    bucket.put_object(Key=object_key, Body=object_content)
    end = time.time()
    duration = end - start
    return size, duration

# Parse the command-line arguments
parser = argparse.ArgumentParser(description='s3 Stress Test')
parser.add_argument('-n', '--num_objects', type=int, default=50, help='Number of objects to upload')
parser.add_argument('-b', '--bucket_name', type=str, default='testnmg', help='Name of the S3 bucket')
parser.add_argument('-r', '--ratio', type=int, default=2, help='Ratio by which the object size will be multiplied with each iteration')
args = parser.parse_args()

bucket = s3.Bucket(args.bucket_name)

# Upload objects in parallel
sizes = []
times = []
object_size = 1024 * 1024 * 5 # 5 MB
executor = ThreadPoolExecutor(max_workers=5)
futures = []
for i in range(args.num_objects):
    object_key = f'{object_prefix}{i}'
    data = generate_data(object_size)
    futures.append(executor.submit(upload_object, bucket, object_key, data))
    sizes.append(object_size)
    object_size *= args.ratio

# Wait for all the futures to complete
for future, size in tqdm(zip(futures, sizes), total=args.num_objects, desc="Upload Progress"):
    size, duration = future.result()
    transfer_rate = size / (duration * 1024 * 1024)
    times.append(duration)
    print(f"Uploaded object of size {size / 1024 / 1024:.2f} MB in {duration:.2f} seconds with transfer rate {transfer_rate:.2f} MB/s")

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
plt.savefig("transfer_rates.png")
