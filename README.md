# Finance Buddy

Finance Buddy is a sophisticated Streamlit application designed to analyze P&L documents and answer financial queries using Google Generative AI. This tool is perfect for financial analysts, accountants, and anyone dealing with financial statements.


[Video of the task.webm](https://github.com/user-attachments/assets/34b80441-8719-40ba-896a-4e412f7e7a6f)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Using Docker](#using-docker)
  - [Local Setup](#local-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Document Upload**: Upload multiple P&L documents in PDF format.
- **Document Processing**: Process uploaded documents to extract and analyze financial data.
- **Query System**: Ask questions about your financial data and get accurate, professional responses.
- **Integration with Google Generative AI**: Leverage advanced AI capabilities for accurate and context-aware responses.

## Prerequisites

- Docker (for containerized deployment)
- Python 3.8+
- Streamlit
- Google Generative AI API Key

## Setup

### Using Docker

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd finance-buddy
    ```

2. **Build the Docker image:**

    ```sh
    docker build -t finance-buddy .
    ```

3. **Run the Docker container:**

    ```sh
    docker run -p 8501:8501 finance-buddy
    ```

4. **Access the application:**

    Open your browser and go to `http://localhost:8501`.

### Local Setup

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd finance-buddy
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file and add your Google API Key:**

    ```sh
    GOOGLE_API_KEY=your_google_api_key_here
    ```

5. **Run the Streamlit application:**

    ```sh
    streamlit run app.py
    ```

6. **Access the application:**

    Open your browser and go to `http://localhost:8501`.

## Usage

### Uploading and Processing Documents

1. **Upload P&L Documents:**

    Use the sidebar to upload your P&L documents in PDF format.

2. **Process Documents:**

    Click the "Process Documents" button to process the uploaded files.

### Asking Questions

1. **Enter Your Query:**

    Enter your financial queries in the input box.

2. **Get Responses:**

    The application will analyze the processed documents and provide accurate responses based on the financial data.

### Example Queries

- "What was the total revenue for the last quarter?"
- "How much did we spend on marketing last year?"
- "What is the net profit margin for the current fiscal year?"

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- Thanks to the Streamlit and Google Generative AI teams for their excellent tools and documentation.
- Special thanks to the open-source community for their contributions and support.

## Contact

For any questions or support, please open an issue or contact the maintainers directly.

---

Made ❤️ by Vikrant Kumar
