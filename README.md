# LLM-powered Code Generator

This project implements an LLM-powered code generation system using the Groq API. It creates a Flask REST API for task management based on user-provided specifications.

## Features

- Generates Python code for a Flask REST API with CRUD operations
- Uses SQLAlchemy for database operations
- Implements proper error handling
- Saves generated code to a file

## Prerequisites

- Python 3.7+
- Groq API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ghsaboias/special-agent.git
   cd special-agent
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Groq API key as an environment variable:
   ```
   export GROQ_API_KEY='your_api_key_here'
   ```

## Usage

Run the main script:

```
python main.py
```

This will:
1. Create an LLMAgent instance
2. Generate code for a Flask REST API based on the specified task
3. Save the generated code to `output/app.py`
4. Display the generated code in the console

## Project Structure

- `main.py`: Contains the main logic for code generation and file creation
- `requirements.txt`: Lists the required Python packages
- `output/`: Directory where generated code files are saved

## Customization

To modify the code generation task, edit the `task` variable in the `main()` function of `main.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.