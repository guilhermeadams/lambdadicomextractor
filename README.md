# DICOM Metadata Extraction

This code is designed to extract specific metadata from DICOM files and store them in DynamoDB using AWS Lambda and Boto3. DICOM (Digital Imaging and Communications in Medicine) is a standard format used for medical imaging.

## Prerequisites
- Python 3.6 or above
- AWS SDK for Python (Boto3) library
- PyDICOM library

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/guilhermeadams/lambdadicomextractor
   ```

2. Install the required dependencies:

   ```
   pip install boto3 pydicom
   ```

## Configuration

Before running the code, make sure you have the necessary AWS credentials configured on your system. This can be done by either setting environment variables or using the AWS CLI.

## Usage

1. Import the required libraries:

   ```python
   import boto3
   import pydicom
   from io import BytesIO
   ```

2. Instantiate the Boto3 clients for S3 and DynamoDB:

   ```python
   s3 = boto3.client('s3')
   dynamodb = boto3.resource('dynamodb')
   ```

3. Define the Lambda handler function:

   ```python
   def lambda_handler(event, context):
       # Get bucket name and file key from the S3 event
       bucket_name = event['Records'][0]['s3']['bucket']['name']
       file_key = event['Records'][0]['s3']['object']['key']
   
       # Get the DICOM file from S3
       dicom_object = s3.get_object(Bucket=bucket_name, Key=file_key)
       dicom_data = dicom_object['Body'].read()
   
       # Load DICOM file with pydicom
       dicom_file = pydicom.dcmread(BytesIO(dicom_data))
   
       # Extract the specific DICOM headers
       headers = ['PatientID', 'PatientName', 'ReferringPhysicianName', 'StudyDate', 'StudyDescription']
       extracted_headers = {header: str(dicom_file.data_element(header).value) if dicom_file.data_element(header) else None for header in headers}
   
       # Write the extracted headers to DynamoDB
       table = dynamodb.Table('DicomMetadata')
       table.put_item(Item={'s3_key': file_key, **extracted_headers})
   
       return {
           'statusCode': 200,
           'body': f'Successfully processed file {file_key}'
       }
   ```

4. Customize the `headers` list to specify the DICOM headers you want to extract.

5. Update the `DynamoDB` table name in the `table` variable to match your desired table.

6. Deploy the code to AWS Lambda.

## Limitations

- This code assumes that the DICOM files are stored in an S3 bucket and are triggering the Lambda function through an S3 event.
- The code extracts specific DICOM headers based on the `headers` list provided. Modify the list according to your requirements.

## Contributing

Contributions are welcome! If you find any issues or have suggestions, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
