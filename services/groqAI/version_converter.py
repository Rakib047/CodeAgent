from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
from langchain.memory import ConversationBufferMemory

def load_prompt_template(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# def convert_python_version(code: str, instruction: str, model_name: str, memory):
def convert_python_version(
    code: str,
    instruction: str,
    memory,
    model: str,
    memory_length: int,
    temperature: float,
    top_p: float,
    max_tokens: int,
    streaming: bool
):
    prompt_str = load_prompt_template("prompts/prompt_template.txt")
    prompt = PromptTemplate(
        input_variables=["instruction", "code"],
        template=prompt_str,
    )

    groq_chat = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name=model,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        streaming=streaming
    )
    memory = ConversationBufferMemory()

    chain = LLMChain(llm=groq_chat, prompt=prompt)
    response = chain.run({
        "instruction": instruction,
        "code": code
    })

    return response