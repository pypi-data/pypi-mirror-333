class SyntaxRelevancyTemplate:
    @staticmethod
    def generate_code_syntax_relevancy_percentage_template(ground_truth_code: str, llm_generated_code: str):
        return f"""
            You are tasked with evaluating and comparing two pieces of code: a ground truth code and an LLM-generated code. Your goal is to determine the match percentage (syntax relevancy) between these two codes from a syntactical perspective.
            
            Here is the ground truth code:
            <ground_truth_code>
            {ground_truth_code}
            </ground_truth_code>
            
            Here is the LLM-generated code:
            <llm_generated_code>
            {llm_generated_code}
            </llm_generated_code>
            
            To evaluate the syntax relevancy, follow these steps:
            
            1. Analyze both pieces of code carefully, focusing on their syntactical structure, naming conventions, and code style rather than overall functionality.
            
            2. Compare the following aspects of the code:
               a. Variable and function naming patterns
               b. Code organization and structure
               c. Syntactic elements (brackets, semicolons, indentation, etc.)
               d. Use of language-specific syntax features
               e. Comment style and placement
               f. Whitespace usage and formatting
            
            3. For each matching aspect, assign a percentage based on how closely the LLM-generated code matches the ground truth code in terms of syntax and style.
            
            4. Calculate the overall match percentage (syntax relevancy) by averaging the percentages from step 3.
            
            5. Provide a brief explanation for your evaluation, highlighting the main syntactic similarities and differences between the two codes.
            
            Present your evaluation in the following JSON format without any additional details:
            
            {{
            "syntax_relevancy_score": "X%",
            "reason": "Your explanation for the match percentage, including key syntax similarities and differences"
            }}
            
            Remember to focus on the syntactical aspects of the code rather than logical equivalence. Two pieces of code can perform the same function but have very different syntax patterns, variable naming conventions, and code organization.
        """