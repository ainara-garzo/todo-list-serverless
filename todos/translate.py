import os
import json
import boto3
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')

def get(event, context):
    
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    target_language = event["pathParameters"]['lang']
    
    task_to_translate = result['Item']['text']
    
    try:
        source_language = comprehend.detect_dominant_language(
            Text = task_to_translate,
            LanguageCode='es')
    except: 
        source_language = "auto"
    
    task_translated = translate.translate_text(Text = task_to_translate, 
                                        SourceLanguageCode = source_language, 
                                        TargetLanguageCode = target_language)
    
    result['Item']['text'] = task_translated['TranslatedText']
    
    #create response
    response = {
        
        'statusCode': 200,
        'body': json.dumps(result['Item'], cls = decimalencoder.DecimalEncoder)
    }
    
    return response