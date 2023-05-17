def lambda_handler(event):
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
