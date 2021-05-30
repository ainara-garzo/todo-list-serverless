import os
import json
import boto3
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    translate = boto3.client(service_name = 'translate', 
                            region_name = 'eu-east-1', 
                            use_ssl = True)
    
    task2translate = result['Item']['text']
    
    try:
        review_id = event["pathParameters"]['id']
    except:
        review_id = "1"
    
    target_language = event["pathParameters"]['lang']
    
    try:
        review = event["queryStringParameters"]['review']
    except:
        review = "An error has happened"
    
    trask_tranlated = translate.translate_text(Text = review, 
                                        SourceLanguageCode = "auto", 
                                        TargetLanguageCode = target_language)
    
    result['Item']['tex'] = trask_tranlated['TranslatedText']
    
    #create response
    response = {
        
        'statusCode': 200,
        'body': json.dumps(result['Item'])
    }
    
    return response
    



# def identify_lang(task):
#     response = comprehend
    
#     return response
    
# def translate_task(task, source, target):
    
#     response = translate
    
#     return response
    
# def get(event, context):
#     table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

#     # fetch todo from the database
#     result = table.get_item(
#         Key={
#             'id': event['pathParameters']['id']
#         }
#     )
    
#     target = event['pathParameters']['lang']
    
#     task = result['Item']['text']
    
#     source_result = identify_lang(task)
    
#     source = source_result['Languages'][0]['LanguageCode']
    
#     task_translated = translate_task(task, source, target)
#     result['Item']['text'] = task_translated['TranslatedText']
    
#     # create a response
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(result['Item'], cls=decimalencoder.DecimalEncoder)
#     }
    
#     return response