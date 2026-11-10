from utils.agents_related import get_ollama_llm, get_agent, get_inference_client, get_inference_chat_client
from typing import Literal
from prompts.architect_prompt import prompt

class Architect:
    def __init__(self, model, llm_type: Literal["ollama", "huggingface"] = "ollama"):
        self.prompt = prompt()
        self.type = llm_type
        if llm_type == "ollama":
            self.client = get_ollama_llm(model = model, 
                                  temperature = 0.3)
        else:
            self.client = get_inference_client()
            

    def agent_node(self, raw_text: str, cloud_infra : str):
        print("Creating the architecture...")
        #Ollma Execution
        if self.type == "ollama":
            agent = get_agent(
                llm = self.client,
                prompt = self.prompt
            )

            user_content = raw_text + "\n\n" + "Cloud Infrastructure: " + cloud_infra
            response = agent.invoke(
                {
                    "messages" : [
                        {
                            "role" :"user",
                            "content" : user_content
                        }
                    ]
                }
            )

            architecture = response["messages"][1].content
            print("Done....")
            return architecture

if __name__ == "__main__":
    architect = Architect(model = "qwen3:1.7b", llm_type = "ollama")
    raw_text = """## 1. Problem Summary  
A B2B payments agentic system is needed to automate transaction processing, enforce compliance, and optimize payment workflows. The goal is to design AI agents that handle payment processing, fraud detection, reconciliation, and customer communication, ensuring scalability, accuracy, and compliance with financial regulations.  

## 2. Assumptions and Open Items  
- **Assumptions**:  
  - The system will integrate with existing payment gateways (e.g., Stripe, PayPal).  
  - Compliance requirements (e.g., GDPR, PCI DSS) are already in place.  
  - Stakeholders agree on the scope (e.g., processing, fraud, reconciliation).  
- **Placeholders**:  
  - `[INSERT: Payment gateway integration details]`  
  - `[INSERT: Compliance thresholds]`  
- **Risks if assumptions are wrong**:  
  - Integration failures or non-compliance penalties.  

## 3. Recommended Approach  
**Multi-agent workflow**:  
Agent A (Payment Processing) → Agent B (Fraud Detection) → Agent C (Reconciliation & Reporting)  

## 4. Agent Prompt(s)  
```python
## Agent A (Payment Processing)  
Role: AI agent for processing B2B payments  
Context: Automates transaction validation, currency conversion, and payment initiation.  
Objective: Process [INSERT: payment transactions] using [INSERT: payment gateway integration].  
Inputs: Payment data, transaction rules, compliance thresholds.  
Task Instructions:  
1. Validate transactions against [INSERT: compliance thresholds].  
2. Map currencies to [INSERT: target currency].  
3. Route payments to [INSERT: payment gateway integration].  
Constraints and Rules:  
- Only process [INSERT: valid payment methods].  
- Enforce [INSERT: fraud detection rules].  
Output Format: JSON with transaction details, status, and timestamps.  
Quality Criteria: Ensure 99.9% accuracy and compliance.  
Edge Cases: Handle [INSERT: error scenarios] gracefully.  

## Agent B (Fraud Detection)  
Role: AI agent for detecting fraudulent transactions.  
Context: Enforces security rules to prevent unauthorized payments.  
Objective: Flag suspicious transactions.  
Inputs: Agent A’s output, [INSERT: fraud detection rules].  
Task Instructions:  
1. Compare transactions to [INSERT: fraud detection rules].  
2. Flag anomalies with confidence level [INSERT: confidence threshold].  
3. Generate alerts for [INSERT: stakeholders].  
Constraints and Rules:  
- Only trigger alerts for [INSERT: high-risk transactions].  
- Maintain [INSERT: data retention period].  
Output Format: CSV with transaction ID, status, and risk score.  
Quality Criteria: 95% accuracy in detecting fraud.  
Edge Cases: Handle [INSERT: edge cases] like multi-factor authentication.  

## Agent C (Reconciliation & Reporting)  
Role: AI agent for reconciling payments and generating reports.  
Context: Ensure accuracy and provide insights for decision-making.  
Objective: Reconcile payments with invoices and generate reports.  
Inputs: Agent B’s alerts, [INSERT: financial data].  
Task Instructions:  
1. Match payments to invoices using [INSERT: matching algorithm].  
2. Generate [INSERT: report type] (e.g., monthly, quarterly).  
3. Flag discrepancies with [INSERT: resolution steps].  
Constraints and Rules:  
- Only process [INSERT: valid invoices].  
- Maintain [INSERT: data integrity].  
Output Format: Excel with reconciliation details and trends.  
Quality Criteria: 99% accuracy in reconciliation.  
Edge Cases: Handle [INSERT: data inconsistencies] manually.  
```  

## 5. Handoff Notes (Multi-agent only)  
- Agent A passes transaction data to Agent B.  
- Agent B passes flagged transactions to Agent C for reconciliation.  
- Agent C generates reports for [INSERT: stakeholders].  

## 6. Success Check  
- [INSERT: Agent A’s output meets compliance thresholds].  
- [INSERT: Agent B’s alerts are actionable and correctly flagged].  
- [INSERT: Agent C’s reconciliation reports are accurate and timely].  
- [INSERT: System handles edge cases without errors].  
```  

## 7. Legal Note  
This prompt assumes compliance with [INSERT: relevant regulations]. Human review is required for final deployment."""
    cloud_infra = "AWS"
    architecture = architect.agent_node(raw_text, cloud_infra)

    with open("architect_output.txt", "w", encoding="utf-8") as f:
        f.write(architecture)