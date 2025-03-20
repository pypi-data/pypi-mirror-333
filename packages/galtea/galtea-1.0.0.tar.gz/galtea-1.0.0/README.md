# Galtea Evaluation Task Creator

Streamline your evaluation process with Galtea's powerful evaluation SDK

## Setting Up the Development Environment

#### Prerequisites:

Before starting, make sure you have [Poetry](https://python-poetry.org/docs/main/) installed. Poetry is a tool for dependency management and packaging in Python.

1. Clone the repository:

   ```bash
   git clone https://github.com/Galtea-AI/galtea.git
   cd galtea-sdk
   ```

2. To install the project dependencies, run:

   ```bash
   poetry install
   ```

3. To active the virtual environmennt created by Poetry run:

   ```bash
   poetry shell
   ```

4. Set up your environment variables:
   Create a `.env` file in your project root directory with the following content:
   ```
   API_URL=STATIC_API_URL
   API_KEY=GALTEA_API_KEY
   ```

## Creating Evaluation Tasks

1. Create your evaluation task:
   In your `main.py` file, use the following code to create a simple ab testing evaluation task:

   ```python
      from dotenv import load_dotenv
      load_dotenv()

      import galtea


      def main():
         with galtea.Evaluation() as pipeline:

            pipeline.create_evaluation(
                  ...
                  ...
                  ...
            )

      if __name__ == "__main__":
         main()
   ```

2. Launch your evaluation task:
   Run the script to create your task:
   ```
   python main.py
   ```
