import uuid
from gradio_client import Client, handle_file
from utils.logger import timed
import logging
import boto3

INFER_DIR= "inference"
s3 = boto3.resource('s3')
s3Client = boto3.client("s3", region_name='eu-north-1',
                  config=boto3.session.Config(signature_version='s3v4', s3={'signature_version': 's3v4', 'use_accelerate_endpoint': False}))
client = Client("foryahasake/replica",download_files=INFER_DIR)
logger = logging.getLogger(__name__)
    

    
@timed
def hf_inference_img(imgFile):
    result = client.predict(
            image_url="",
            image=handle_file(imgFile),
            min_score=0.4,
            api_name="/find")
    # Upload a new file to s3 
    try:
        f =open(result, 'rb')
    except FileNotFoundError as e:
        print(f'error {e}')
    else:
        with f:
            try:
                filename = result.split("/")[-2]
                s3.Bucket('baseerv2bucket').put_object(Key=f'inference/{filename}.jpeg', Body=f)
                surl = s3Client.generate_presigned_url( ClientMethod='get_object', Params={
                'Bucket': 'baseerv2bucket',
                'Key': f'inference/{filename}.jpeg'},  
                 ExpiresIn=3600 # one hour in seconds, increase if needed
                ,)
                return  surl
            except Exception as ex:
                print(f"exception {ex}")
    return None
        
    
@timed
def hf_inference_vid(video_path):
    print("video inference")
    
    result = client.predict(
        video_path={"video":handle_file(video_path)},
        api_name="/vid"
    )
    # Upload a new file to s3 
    try:
        f =open(result.get('video'), 'rb')
    except FileNotFoundError as e:
        print('error')
        print(e)
    else:
        with f:
            try:
                filename = result.get('video').split("/")[-2]
                s3.Bucket('baseerv2bucket').put_object(Key=f'inference/{filename}.mp4', Body=f)
                surl = s3Client.generate_presigned_url( ClientMethod='get_object', Params={
                'Bucket': 'baseerv2bucket',
                'Key': f'inference/{filename}.mp4'},  
                 ExpiresIn=3600 # one hour in seconds, increase if needed
                ,)
                return  surl
            except Exception as ex:
                logger.info(f'Exception had occured{ex}')
    return None
        
    
    
    
