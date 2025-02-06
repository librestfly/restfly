# RESTfly Examples

This directory contains examples to help you get started with RESTfly.

## Pre-requisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- `restfly` library
- `python-dotenv` library

## Steps to Run

Follow these steps to set up and run the examples:

1. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

2. **Install Dependencies**

   ```bash
   pip install restfly python-dotenv
   ```

3. **Configure Environment Variables**

   Update the `.env` file in the `examples` directory and add your GitHub API key:

   ```env
   GITHUB_URL=https://api.github.com
   GITHUB_TOKEN=your_github_token_here
   LOG_LEVEL=INFO  # Possible values are DEBUG, INFO, WARN, ERROR, CRITICAL
   ```

4. **Run the Example**

   Navigate to the `examples` directory and run the `main.py` file:
   ```bash
   python main.py
   ```

## Additional Information

For more details and advanced usage, refer to the [RESTfly documentation](https://restfly.readthedocs.io).
