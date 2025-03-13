import sys
import io
import builtins
import os
from pydantic import BaseModel, Field
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent, RunContext
from utils import to_markdown
from dotenv import load_dotenv

load_dotenv()

# Get the API key from environment variable or use a placeholder
# You should set this environment variable before running the script
# export OPENAI_API_KEY="your-api-key"
api_key = os.environ.get("OPENAI_API_KEY", "")

# 1. Configure the OpenAIModel to talk to OpenAI
ollama_model = OpenAIModel(
    model_name="gpt-4o-mini",
    api_key=api_key
    # provider=OpenAIProvider(base_url='http://localhost:11434/v1'),
)

# 2. Define the output schema for your AI responses
class GameResult(BaseModel):
    code: str = Field(
        examples=["def example():\n    return('Hello World')"],
        description="The Python code for the generated game."
    )
    difficulty: str = Field(
        examples=["Easy", "Medium", "Hard", "Very Easy"],
        description="Difficulty level of the game."
    )
    keywords: list[str] = Field(
        description="List of keywords representing main concepts learned."
    )
    response: str = Field(description="Output of the executed code given by the tool")
    walkthrough: str = Field(description="Explain how the code works")

# 3. Define your user details
class UserDetails(BaseModel):
    userId: int
    userName: str
    userExperience: int  # 0-5 scale
    userSkillset: list[str]

# 4. Create the Pydantic-AI Agent
agent = Agent(
    model=ollama_model,
    deps_type=UserDetails,
    result_type=GameResult,
    system_prompt=(
        "You are an expert Python game developer specializing in INTERACTIVE games.\n"
        "Your goal is to generate a JSON object matching this schema:\n"
        "{\n"
        '  "code": "Fully executable Python code with MULTIPLE input statements for user interaction",\n'
        '  "difficulty": "Easy/Medium/Hard/Very Easy",\n'
        '  "keywords": ["list of relevant concepts"],\n'
        '  "response": "Output of the executed code, including user interactions",\n'
        '  "walkthrough": "Explanation of what happens in the code, including how the keywords are implemented and how user inputs affect the game.",\n'
        "}\n"
        "IMPORTANT: The code MUST be interactive and contain multiple input() statements to get user input.\n"
        "The game should have the user make choices or provide data that affects the game's outcome.\n"
        "DO NOT create a demonstration or tutorial - create an actual interactive game that requires user participation.\n"
        "The run_code tool will execute your game code and allow real-time user interaction.\n"
        "Do not include markdown formatting. Do not include extra keys or text.\n"
        "Only return valid JSON!\n"
        "Use the tool to execute the code.\n\n"
        "Here's an example of what your response should look like:\n\n"
        "{\n"
        '  "code": "import random\\n\\ndef number_guessing_game():\\n    print(\\"Welcome to the Number Guessing Game!\\")'
        '\\n    print(\\"I\'m thinking of a number between 1 and 20.\\")'
        '\\n    secret_number = random.randint(1, 20)\\n    attempts = 0\\n    max_attempts = 5'
        '\\n\\n    while attempts < max_attempts:\\n'
        '        try:\\n            guess = int(input(\\"Enter your guess (1-20): \\"))\\n'
        '            attempts += 1\\n\\n'
        '            if guess < secret_number:\\n                print(\\"Too low! Try again.\\")\\n'
        '            elif guess > secret_number:\\n                print(\\"Too high! Try again.\\")\\n'
        '            else:\\n                print(f\\"Congratulations! You guessed the number in {attempts} attempts!\\")\\n'
        '                return\\n\\n'
        '            print(f\\"Attempts left: {max_attempts - attempts}\\")\\n'
        '        except ValueError:\\n            print(\\"Please enter a valid number!\\")\\n\\n'
        '    print(f\\"Game over! The secret number was {secret_number}.\\")\\n\\n'
        'number_guessing_game()",\n'
        '  "difficulty": "Easy",\n'
        '  "keywords": ["loops", "conditionals", "user input", "random numbers", "error handling"],\n'
        '  "response": "Welcome to the Number Guessing Game!\\nI\'m thinking of a number between 1 and 20.\\nEnter your guess (1-20): 10\\nToo high! Try again.\\nAttempts left: 4\\nEnter your guess (1-20): 5\\nToo low! Try again.\\nAttempts left: 3\\nEnter your guess (1-20): 7\\nCongratulations! You guessed the number in 3 attempts!",\n'
        '  "walkthrough": "This code creates a simple number guessing game that demonstrates several programming concepts. It uses a while loop to allow multiple guesses up to a maximum number of attempts. The random module generates a secret number between 1 and 20. User input is collected using the input() function, and error handling with try/except blocks prevents the program from crashing if the user enters non-numeric values. Conditionals (if/elif/else) are used to check if the guess is too high, too low, or correct. The game keeps track of the number of attempts and provides appropriate feedback after each guess. This interactive game teaches the basics of loops while creating an engaging experience for the user."\n'
        "}\n"
    ),
    result_retries=3
)

# 5. Dependency Resolver (if needed)
@agent.system_prompt
async def get_user_details(ctx: RunContext[UserDetails]) -> UserDetails:
    """Simply return the user details as structured data."""
    return f"{to_markdown(ctx.deps)}"

# 6. Provide some user info
user_1 = UserDetails(
    userId=1,
    userName="John Doe",
    userExperience=0,
    userSkillset=["Python", "Data Structures"]
)

@agent.tool
def run_code(ctx: RunContext, code: str) -> str:
    """
    Executes Python code and allows real user interaction.
    This will run the game and let the user play it directly.
    The function will capture all output and user inputs to show the full interactive experience.
    """
    backup_stdout = sys.stdout
    output_buffer = io.StringIO()
    
    # Create a special input function that both captures inputs and responses
    original_input = builtins.input
    
    def interactive_input(prompt):
        # Show the prompt to the real user
        print(prompt, end='', flush=True)
        # Get input from the real user
        user_input = original_input()
        # Echo the input back to the screen so user can see what they typed
        print(user_input)
        # Add both prompt and input to our output buffer
        output_buffer.write(f"{prompt}{user_input}\n")
        # Return the user's input to the game
        return user_input
    
    # Create a custom stdout that writes to both the console and our buffer
    class TeeStdout:
        def write(self, data):
            backup_stdout.write(data)
            output_buffer.write(data)
            
        def flush(self):
            backup_stdout.flush()
    
    sys.stdout = TeeStdout()
    
    # Replace the built-in input function with our interactive version
    builtins.input = interactive_input
    
    try:
        print("\n=== GAME STARTING - Please interact below ===\n")
        # Execute the code with our custom input function
        exec(code, {})
        print("\n=== GAME COMPLETED ===\n")
    except Exception as e:
        print(f"Error while running code: {e}")
    finally:
        # Restore the original input function and stdout
        builtins.input = original_input
        sys.stdout = backup_stdout
    
    # Return the captured output including user interactions
    return output_buffer.getvalue()

@agent.tool
def debug_model_output(ctx: RunContext, output: str) -> str:
    """Debug what the model is trying to output."""
    print(f"Model attempted to output: {output}")
    return "Debugging information received"

# 7. Run your Agent with a user prompt
def run_agent():
    print("\n=== Python Game Learning Agent ===\n")
    print("This agent will create an interactive game to help you learn Python concepts.")
    print("Currently optimized for teaching about the random module and other Python concepts.")
    print("\nPlease enter your learning request (e.g., 'Create a game that teaches how the random module works'):")
    
    user_prompt = input("user: ")
    
    print("\nGenerating your interactive game... This may take a moment.\n")
    
    results = agent.run_sync(
        user_prompt=user_prompt,
        deps=user_1
    )
    
    # 8. Access the result
    if results:
        print("=== Generated Game ===")
        print("Code:\n", results.data.code,"\n\n")
        print("Difficulty:\n", results.data.difficulty,"\n\n")
        print("Keywords:\n", results.data.keywords,"\n\n")
        print("Response: \n", results.data.response, "\n\n")
        print('Walkthrough: \n', results.data.walkthrough, '\n\n')
    else:
        print("No valid response from the AI model.")

if __name__ == "__main__":
    run_agent()
