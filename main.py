from io import BytesIO
import os
from typing import List
from fastapi import FastAPI, UploadFile, Form, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import fitz
import zipfile


app = FastAPI()

dirname = os.path.dirname(__file__)

app.mount("/assets", StaticFiles(directory=os.path.join(dirname, 'assets')), name="assets")

templates = Jinja2Templates(directory=os.path.join(dirname, 'templates'))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "titulo": "Api de PDFs"})

@app.get("/join_pdf", response_class=HTMLResponse)
async def join_pdf_page(request: Request):
    return templates.TemplateResponse("join_pdf.html", {"request": request})
    

@app.post("/join_pdf")
async def join_pdf(pdf_files: List[UploadFile], output_file_name:str = Form("out.pdf")) -> UploadFile:
    new_pdf = fitz.open()
    for pdf_file in pdf_files:
        pdf_stream = await pdf_file.read()
        try:
            pdf = fitz.open(None, pdf_stream, "pdf")
        except:
            raise HTTPException(status_code=400, detail=f"O arquivo {pdf_file.filename} não é um PDF válido.")
        new_pdf.insert_pdf(pdf)
    
    new_pdf_buffer = BytesIO(new_pdf.tobytes())

    headers = {
        'Content-Disposition': f'attachment; filename={output_file_name}'
    }

    return StreamingResponse(new_pdf_buffer, headers=headers, media_type="application/pdf")




@app.get("/split_pdf", response_class=HTMLResponse)
async def split_pdf_page(request: Request):
    return templates.TemplateResponse("split_pdf.html", {"request": request})
    


@app.post("/split_pdf")
async def split_pdf(pdf_file: UploadFile, output_file_name: str = Form("out.zip")) -> List[UploadFile]:
    
    pdf_file = await pdf_file.read()

    try:
        pdf = fitz.open(None, pdf_file, "pdf")
    except:
        raise HTTPException(status_code=400, detail=f"O arquivo {pdf_file.filename} não é um PDF válido.")
    
    # List to hold the bytes of each split PDF
    split_pdfs = []
    for page in range(pdf.page_count):
        # Get the page object
        pdf_page = pdf[page]

        # Create a new PDF document with just this one page
        new_pdf = fitz.open()
        new_pdf.insert_pdf(pdf, from_page=page, to_page=page)
        
        # Save the new PDF to a bytes object
        new_pdf_bytes = BytesIO()
        new_pdf.save(new_pdf_bytes)
        new_pdf_bytes.seek(0)

        split_pdfs.append(new_pdf_bytes.getvalue())

        # Close the new PDF document
        new_pdf.close()

    # Close the original PDF document
    pdf.close()

    zip_bytes = BytesIO()
    with zipfile.ZipFile(zip_bytes, "w") as zip_file:
        for index, pdf_bytes in enumerate(split_pdfs):
            filename = f"page_{index + 1}.pdf"
            zip_file.writestr(filename, pdf_bytes)

    headers = {
    'Content-Disposition': f'attachment; filename={output_file_name}.zip'
    }


    zip_bytes.seek(0)
    return StreamingResponse(zip_bytes, headers=headers, media_type="application/zip")
