from utils.agents_related import get_ollama_llm, get_agent, get_inference_client, get_inference_chat_client
from typing import Literal
from prompts.svg_maker_prompt import prompt, validate_svg_prompt

class Renderer:
    def __init__(self, model, llm_type: Literal["ollama", "huggingface"] = "ollama"):
        self.prompt = prompt()
        self.type = llm_type
        if llm_type == "ollama":
            self.client = get_ollama_llm(model = model, 
                                  temperature = 0.7)
        else:
            self.client = get_inference_client()

    def validate_svg(self, svg_content: str) -> bool|str:
        # Basic validation: Check if the content starts with <svg> and ends with </svg>
        if self.type == "ollama":
                    agent = get_agent(
                        llm = self.client,
                        prompt = validate_svg_prompt()
                    )
        
                    response = agent.invoke(
                        {
                            "messages" : [
                                {
                                    "role" :"user",
                                    "content" : svg_content
                                }
                            ]
                        }
                    )
        
                    validated_response = response["messages"][1].content
                    print(f"Validated Response: {validated_response}")
                    if validated_response == "True" or validated_response == True:
                        return True
                    return validated_response
        
    def agent_node(self, raw_text: str):
        #Ollma Execution
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

            svg = response["messages"][1].content
           
            return svg.replace("```xml","").replace("`","").replace(" & ", " and ").strip()

    def create_svg(self, raw_text: str) -> str:
        counter = 0
        validate = False
        correction = ""
        svg_content = ""
        while  True:
            print(f"Attempt {counter + 1}: Generating SVG...")
            svg_content = self.agent_node(raw_text + f"""\n\n<correction> {correction}</correction>""")
            validate = self.validate_svg(svg_content)
            if validate == True:
                 break
            if counter >= 3:
                 break
            counter += 1
        return svg_content

if __name__ == "__main__":
    renderer = Renderer(model = "qwen3:1.7b", llm_type = "ollama")
    raw_text = ""
    with open("architect_output.txt", "r") as f:
        raw_text = f.read()
    svg = renderer.create_svg(raw_text)
    with open("architect_output.svg", "w", encoding = "utf-8") as f:
        f.write(svg)