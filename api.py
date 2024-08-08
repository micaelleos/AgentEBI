from typing import Annotated
from pydantic import BaseModel, Field

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from mangum import Mangum
import uvicorn

from src.agent import EBIagent
from src.getSession import get_all_keys
from src.getEBI import get_ebi

from src.description import description

description = """
A API EBIagent é como seu guia de inteligência artificial para criar estudos bíblicos indutivos. Ela te ajuda a ter conversas inteligentes sobre a Bíblia e ainda monta estudos personalizados com base no papo que vocês tiveram.

**O que essa API faz?**

*  **Bate-papo com o Agente de IA:** Com essa API, você pode bater um papo com o EBIagent, que entende suas perguntas e responde com insights bíblicos. É como ter um amigo que manja muito da Bíblia, sempre pronto para trocar uma ideia.

*  **Criação de Estudos Bíblicos Indutivos:** Enquanto vocês conversam, o EBIagent também monta estudos bíblicos indutivos personalizados, direto no contexto da conversa. Perfeito para quem quer se aprofundar mais no que está sendo discutido.

*  **Histórico de Conversas:** Precisa lembrar de algo que discutiu antes? A API permite que você recupere o histórico das suas sessões de conversa, assim você pode revisar e refletir a qualquer momento.

*  **Lista de Sessões:** Quer ver todas as sessões de bate-papo que já rolou? A API te mostra todas as conversas, para você nunca perder nada.

*  **Acesso aos Estudos Bíblicos:** Além disso, você pode puxar os estudos bíblicos que o EBIagent criou durante uma sessão específica. Isso facilita muito na hora de estudar ou refletir depois.

Se você está criando uma aplicação e quer incluir uma interação bíblica com inteligência artificial, essa API é uma ótima opção para deixar a experiência bem mais interessante e personalizada.

"""

app = FastAPI(title="EBIagent",
            description=description)

handler=Mangum(app)

class Prompt(BaseModel):
    user_message: str = Field(default=None,title="user message")

@app.post("/session/{chat_session}")
async def chat(chat_session: str, prompt: Annotated[Prompt, Body(embed=True)]):
    chat = EBIagent(session_id=chat_session)
    try:
        response = chat.chat_agent(query=prompt.user_message)
    except:
       return {"Ai_response": "", "ChatId":"", "EBI":"","status":"errror"}
    
    ebi = get_ebi(chat_session)
    results = {"Ai_response": response["output"], "EBI": ebi, "status":"sucsses"}
    return results

#@app.post("/session/{chat_session}/stream")
#async def chat_stream(chat_session: str, prompt: Annotated[Prompt, Body(embed=True)]):
#    chat = EBIagent(session_id=chat_session)
#
#    try:
#        response = chat.chat_agent_stream(query=prompt.user_message)
#        return StreamingResponse(response)
#    except:
#       return {"Agentchain_response": "","status":"errror"}
    


@app.get('/session/{chat_session}/history')
def chat_history(chat_session:str):
   history = EBIagent(session_id=chat_session).message_history.messages
   return {'chat_session':chat_session,"history":history}

@app.get('/session/list')
def chat_list():
   list = get_all_keys()
   return {'Session_ids':list}

@app.get('/session/{chat_session}/ebi')
def chat_ebi(chat_session:str):
   ebi = get_ebi(chat_session)
   return {'EBI':ebi}

if __name__=="__main__":
  uvicorn.run(app,host="0.0.0.0",port=8080)