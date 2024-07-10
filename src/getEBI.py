import boto3
from boto3.dynamodb.conditions import Key
# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EBITable')

def get_ebi(session_id):
    try:
        response = table.scan(
            FilterExpression=Key('SessionId').eq(session_id)
        )
        return response["Items"]
    except:
        return ""
    
if __name__=="__main__":
    print(get_ebi('2'))