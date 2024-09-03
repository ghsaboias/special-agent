import os
import uuid
import logging
from groq import Groq
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMAgent:
    def __init__(self, name: str, model: str = "llama-3.1-70b-versatile"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.model = model
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def generate_code(self, task: str) -> str:
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert Python programmer. Generate only the Python code for the given task, without any explanations or markdown formatting."},
                    {"role": "user", "content": task}
                ],
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return None

    def create_file(self, filename: str, content: str) -> str:
        try:
            safe_filename = os.path.basename(filename)
            os.makedirs('output', exist_ok=True)
            file_path = os.path.join('output', safe_filename)
            
            # Strip any potential non-code content
            code_lines = [line for line in content.split('\n') if not line.strip().startswith('```')]
            clean_code = '\n'.join(code_lines)
            
            with open(file_path, 'w') as file:
                file.write(clean_code)
            logger.info(f"File created: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error creating file: {str(e)}")
            return None

def main():
    coder = LLMAgent("Coder")
    
    task = """
    Create a Flask REST API that allows users to create, read, update, and delete (CRUD) tasks. 
    Each task should have a title, description, and status. 
    Use SQLAlchemy for database operations and include proper error handling.
    Provide only the Python code, without any explanations or markdown formatting.
    """

    code = coder.generate_code(task)
    if code:
        file_path = coder.create_file("app.py", code)
        if file_path:
            print(f"{Fore.GREEN}Code saved to: {file_path}{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}Generated Code:{Style.RESET_ALL}")
            print(code)
        else:
            print(f"{Fore.RED}Failed to save the code to a file.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Failed to generate code.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()