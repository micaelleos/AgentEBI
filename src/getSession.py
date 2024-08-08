import boto3
from src.getEBI import get_ebi

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EBIsessionTable')

# Defina a chave primária da sua tabela (Partition Key e, se aplicável, Sort Key)
partition_key_name = 'SessionId'  # Substitua pelo nome da sua chave de partição

def get_all_keys():
    keys = []
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    for item in data:
        keys.append(item[partition_key_name])

    list_key_titles = []
    for key in keys:
        ebi = get_ebi(key)
        if isinstance(ebi,dict):
            list_key_titles.append({partition_key_name:key,"title":ebi["title"]})
        else:
            list_key_titles.append({partition_key_name:key,"title":None})
        
    return list_key_titles

if __name__=="__main__":
    print(get_all_keys())