# S3 Stress Test

A script to perform a stress test on an S3 bucket. The script generates random data of increasing size, uploads it to the S3 bucket, and measures the transfer rate for each object. The results are then plotted as a graph showing the transfer rate for each object.

## Requirements

The following packages are required to run the script:

- boto3
- tqdm
- matplotlib

These packages can be installed using `pip` by running the following command:

You can install these packages by running the following command in your terminal:
```bash
pip install -r requirements.txt
```

## Running the Stress Test

To run the stress test, you will need to provide your AWS access key ID and secret access key as well as the name of the S3 bucket you wish to use. The number of objects to upload and the ratio by which the object size will be multiplied with each iteration can also be specified.

Here is an example of how to run the stress test:

```bash
python3 stress_test.py -n 50 -b test-bucket -r 2
```

This will upload 50 objects to the `test-bucket` S3 bucket, with the object size increasing by a factor of 2 with each iteration.

## Results

The stress test will produce a graph showing the transfer rates for each object. The average transfer rate will be shown as a red dashed line on the graph.

## Contributing

This project is open to contributions and improvements. If you have any ideas or suggestions, feel free to submit a pull request. Your contributions are always welcome and appreciated. Thank you for your interest in this project!

## Copyright

Copyright (c) 2023 Lucas Dousse.
