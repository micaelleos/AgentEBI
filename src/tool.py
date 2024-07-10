from typing import Optional, Type, List
from pydantic import  Field
import boto3
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain.agents import tool


class ExibirEBI(BaseModel):
    title: str = Field(description="Título do EBI resumido em poucas palavras")
    plaintext_base: str = Field(description="Texto base corrido, com versículos e referências")
    description: str = Field(description="10 Perguntas de observação, interpretação e aplicação, listadas em ordem numérica")
    footer: str = Field(description="Versículos de reflexão final")


#class ExibirEBI(BaseTool):
#    name = "exibir_ebi"
#    description = "utilize essa função para exibir o estudo bíblico indutivo (EBI) ao usuário"
#    args_schema: Type[BaseModel] = ExibirEBIformat
#    return_direct: bool = True
#
#    def _run(self, **dict_info:ExibirEBIformat) -> str:
#        """Use the tool."""
#        return "exibido com sucesso"
    
def generate_tools_for_user(session_id: str) -> List[BaseTool]:
    """Generate a set of tools that have a user id associated with them."""

    @tool(args_schema=ExibirEBI)
    def exibir_ebi(**dict_info:ExibirEBI) -> dict:
        """Chame essa função para exibir o EBI ao usuário"""
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('EBITable')
        try:
            response = table.put_item(
                Item={'SessionId':f'{session_id}',"title":dict_info["title"],"base":dict_info["plaintext_base"],"description":dict_info["description"],"footer":dict_info["footer"]})
            return "exibido com sucesso"
        except:
            return "aconteceu um erro ao exibir o EBI"
    
    return exibir_ebi

if __name__=="__main__":
    exibir_ebi = generate_tools_for_user('2')
    print(exibir_ebi.args_schema.schema_json())