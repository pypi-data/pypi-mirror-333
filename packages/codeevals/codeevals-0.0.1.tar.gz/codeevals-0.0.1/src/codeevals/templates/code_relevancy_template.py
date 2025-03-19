class CodeRelevancyTemplate:
    @staticmethod
    def generate_code_relevancy_percentage_template(ground_truth_code: str, llm_generated_code: str):
        return f"""
            You are tasked with evaluating and comparing two pieces of code: a ground truth code and an LLM-generated code. Your goal is to determine the match percentage between these two codes from a logical perspective.
            
            Here is the ground truth code:
            <ground_truth_code>
            {ground_truth_code}
            </ground_truth_code>
            
            Here is the LLM-generated code:
            <llm_generated_code>
            {llm_generated_code}
            </llm_generated_code>
            
            To evaluate the match percentage, follow these steps:
            
            1. Analyze both pieces of code carefully, focusing on their logical structure and functionality rather than syntax or formatting.
            
            2. Compare the following aspects of the code:
               a. Overall algorithm and approach
               b. Key functions and their purposes
               c. Control flow (loops, conditionals, etc.)
               d. Data structures used
               e. Input/output handling
               f. Error handling and edge cases (if applicable)
            
            3. For each matching aspect, assign a percentage based on how closely the LLM-generated code matches the ground truth code in terms of logic and functionality.
            
            4. Calculate the overall match percentage by averaging the percentages from step 3.
            
            5. Provide a brief explanation for your evaluation, highlighting the main similarities and differences between the two codes.
            
            Present your evaluation in the following JSON format without any additional details:
            
            {{
            "match_percentage": "X%",
            "reason": "Your explanation for the match percentage, including key similarities and differences"
            }}
            
            Remember to focus on the logical equivalence of the code rather than exact syntactical matches. Two pieces of code can be logically equivalent even if they use different variable names or slightly different implementations.
        """
