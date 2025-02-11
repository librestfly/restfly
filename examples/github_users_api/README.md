# RESTfly Examples

This directory contains examples to help you get started with RESTfly.

## Pre-requisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- `restfly` library

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
   pip install restfly
   ```

3. **Run the Example**

   Navigate to the `examples` directory and run the `main.py` file:
   ```bash
   python main.py --log-level=debug --token=<GITHUB_TOKEN>
   ```
   **Note**:
   - The default log level is `INFO`.
   - The GitHub token can be set using the environment variable `GITHUB_TOKEN`.
     if you do not want to pass it as a command line argument.

## Additional Information

For more details and advanced usage, refer to the [RESTfly documentation](https://restfly.readthedocs.io).
