from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from docling.document_converter import DocumentConverter
import tempfile
import os

app = FastAPI(title="Docling API on Amvera")

@app.get("/")
def read_root():
    return {"status": "Docling API is running on Amvera"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/convert")
async def convert_document(file: UploadFile = File(...)):
    """
    Загрузите документ (PDF, DOCX и т.п.) и получите распарсенный текст
    """
    try:
        # Сохраняем загруженный файл во временный
        suffix = os.path.splitext(file.filename)[1] or ".bin"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Конвертируем документ через Docling
        converter = DocumentConverter()
        result = converter.convert(tmp_path)

        # Удаляем временный файл
        os.unlink(tmp_path)

        # Возвращаем результат (например, markdown-текст)
        return JSONResponse({
            "filename": file.filename,
            "text": result.document.export_to_markdown(),
            "status": "success"
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
