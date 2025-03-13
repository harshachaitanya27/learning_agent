# Learning Agent

An AI-powered interactive game generator that creates customized Python games to help users learn programming concepts.

## Features

- Creates interactive Python games based on user requests
- Tailors game difficulty to the user's experience level
- Captures real-time user interactions during gameplay
- Provides explanations of programming concepts used in the game
- Supports learning various Python concepts through hands-on games

## Requirements

- Python 3.6+
- OpenAI API key (for GPT models)
- Required packages:
  - pydantic
  - pydantic-ai
  - python-dotenv

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/harshachaitanya27/learning_agent.git
   cd learning_agent
   ```

2. Install dependencies:
   ```bash
   pip install pydantic pydantic-ai python-dotenv
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Learning Agent

### Step 1: Make sure your environment is set up
- Verify your OpenAI API key is correctly set in the `.env` file
- Make sure you have all dependencies installed

### Step 2: Run the agent
```bash
python agents.py
```

### Step 3: Enter your learning request
When prompted, enter what you'd like to learn about. For example:
- "I want to understand how for loops work in Python"
- "Help me learn about dictionaries through a game"
- "Create a game that teaches me about the random module"

### Step 4: Interact with the generated game
- The agent will generate a custom game based on your request
- Follow the prompts in the game to interact with it
- Learn the programming concepts through hands-on play

### Step 5: Review the explanation
After playing, the agent will provide:
- The complete game code
- Difficulty level
- Key programming concepts covered
- A walkthrough explaining how the code works

### Troubleshooting
- If you encounter an "Invalid API key" error, check your `.env` file
- If dependencies are missing, run `pip install -r requirements.txt`
- For macOS/Linux users: ensure you have proper permissions to execute the script

## Example Output

Here's an example of using the agent to learn about for loops:

```
=== Python Game Learning Agent ===

This agent will create an interactive game to help you learn Python concepts.
Currently optimized for teaching about the random module and other Python concepts.

Please enter your learning request (e.g., 'Create a game that teaches how the random module works'):
user: I want to make a interactive game to understand for loops

Generating your interactive game... This may take a moment.


=== GAME STARTING - Please interact below ===

Welcome to the For Loop Adventure!
You need to cross a mysterious forest with 5 magical creatures.
You encounter a friendly dragon. Would you like to (talk) to it, (ignore) it, or (run) away? run 
You ran away from the a friendly dragon!
You encounter a mischievous fairy. Would you like to (talk) to it, (ignore) it, or (run) away? ignore
The a mischievous fairy looks sad as you walk past...
You encounter a wise old owl. Would you like to (talk) to it, (ignore) it, or (run) away? talk
You had a great conversation with the a wise old owl!
You encounter a sneaky fox. Would you like to (talk) to it, (ignore) it, or (run) away? run
You ran away from the a sneaky fox!
You encounter a gentle unicorn. Would you like to (talk) to it, (ignore) it, or (run) away? talk
You had a great conversation with the a gentle unicorn!
Your adventure ends with a score of 2/5. Thank you for playing!

=== GAME COMPLETED ===

=== Generated Game ===
Code:
 def for_loop_adventure():
    print("Welcome to the For Loop Adventure!")
    print("You need to cross a mysterious forest with 5 magical creatures.")
    creatures = ['a friendly dragon', 'a mischievous fairy', 'a wise old owl', 'a sneaky fox', 'a gentle unicorn']
    score = 0
    
    for creature in creatures:
        action = input(f"You encounter {creature}. Would you like to (talk) to it, (ignore) it, or (run) away? ").lower()
        if action == 'talk':
            print(f"You had a great conversation with the {creature}!")
            score += 1
        elif action == 'ignore':
            print(f"The {creature} looks sad as you walk past...")
        elif action == 'run':
            print(f"You ran away from the {creature}!")
        else:
            print("That's not a valid action. You missed your chance!")

    print(f"Your adventure ends with a score of {score}/5. Thank you for playing!")

for_loop_adventure() 


Difficulty: Easy 

Keywords: ['for loops', 'user input', 'conditionals', 'game logic'] 

Walkthrough: This code creates an interactive game called "For Loop Adventure" where the player encounters five magical creatures in a forest. It uses a for loop to iterate through a list of creatures. For each creature, the player can choose to talk, ignore, or run away, influencing the game's outcome. The score is incremented by one for each successful conversation (when the player chooses to talk). The game uses conditionals to assess the player's input and respond accordingly. Invalid inputs prompt a miss, providing an opportunity for user interaction and making the experience engaging while illustrating the concept of for loops.
```

## More Examples

Here are some additional example prompts you can try:
- "Create a game that teaches how the random module works in Python"
- "I want to learn about loops through an interactive game"
- "Help me understand dictionaries with a fun game"
- "Create a game that explains how lists work"
