from typing import Optional, Type, Field, List

import boto3
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, Tool


class ExibirEBI(BaseModel):
    title: str = Field(description="Título do EBI resumido em poucas palavras")
    base: str = Field(description="Texto base, com versículos e referências")
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
                Item={'SessionId':f'{session_id}',"title":dict_info["title"],"base":dict_info["base"],"description":dict_info["description"],"footer":dict_info["footer"]})
            return "exibido com sucesso"
        except:
            return "aconteceu um erro ao exibir o EBI"
    
    return exibir_ebi