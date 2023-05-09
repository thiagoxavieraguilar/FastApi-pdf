Sure, here's a README file for the GitHub repository:

# FastAPI PDF API

This project is a FastAPI-based API for merging and splitting PDF files. It includes two endpoints: `/join_pdf` for merging PDF files and `/split_pdf` for splitting a single PDF file into separate pages.

## Requirements
requirements.txt

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/fastapi-pdf-api.git
```

2. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

3. Start the API:

```bash
cd fastapi-pdf-api
uvicorn main:app --reload
```

4. Open your web browser and navigate to `http://localhost:8000/` to access the API homepage.

## Usage

### Merging PDF files

To merge multiple PDF files, make a POST request to the `/join_pdf` endpoint with the PDF files attached as form data. The output file name can be specified using the `output_file_name` parameter (default is `out.pdf`).



### Splitting a PDF file

To split a single PDF file into separate pages, make a POST request to the `/split_pdf` endpoint with the PDF file attached as form data. The output file name can be specified using the `output_file_name` parameter (default is `out.zip`).

