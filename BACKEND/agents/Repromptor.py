from utils.agents_related import get_ollama_llm, get_agent, get_inference_client, get_inference_chat_client
from typing import Literal
from prompts.Repromptor_prompt import prompt

class Repromptor:
    def __init__(self, model, llm_type: Literal["ollama", "huggingface"] = "ollama"):
        self.prompt = prompt()
        self.type = llm_type
        if llm_type == "ollama":
            self.client = get_ollama_llm(model = model, 
                                  temperature = 0.7)
        else:
            self.client = get_inference_client()
            

    def agent_node(self, raw_text: str):
        #Ollma Execution
        print("Reprompting the prompt...")
        if self.type == "ollama":
            agent = get_agent(
                llm = self.client,
                prompt = self.prompt
            )

            response = agent.invoke(
                {
                    "messages" : [
                        {
                            "role" :"user",
                            "content" : raw_text
                        }
                    ]
                }
            )

            new_prompt = response["messages"][1].content
            print("Done....")
            return new_prompt

if __name__ == "__main__":
    repromptor = Repromptor(model = "qwen3:1.7b", llm_type = "ollama")
    raw_text = "CReate an agentic system for payments B2B"
    new_prompt = repromptor.agent_node(raw_text)
    print(new_prompt)