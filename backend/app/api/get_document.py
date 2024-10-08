from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse
from app.models.get_request_data import get_request_data_all
import os
from firebase_admin import storage
import tempfile

router = APIRouter()

@router.post("/get-document/{request_id}/", response_class=FileResponse)
async def get_document(
    request_id: str,
    file_id: str = Body(..., embed=True)  # Acepta el file_id en el cuerpo de la solicitud
):
    """
    Returns a document from a request.
    Receives the request ID and the file_id of the document to download.

    {
        "file_id": "ID"
    }
    """
    try:
        # Obtener datos del request desde Firestore
        request_data = get_request_data_all(request_id)
        if not request_data:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Verificar la estructura de los datos recuperados
        documents = request_data.get("documents", {})
        if not documents:
            raise HTTPException(status_code=404, detail="No documents found for this request")

        # Buscar el documento que coincide con el file_id
        document_content = next(
            (doc for doc in documents.values() if doc.get("file_id") == file_id), 
            None
        )
        if not document_content:
            raise HTTPException(status_code=404, detail=f"Document with file_id '{file_id}' not found")

        # Obtener la URL del archivo desde Firebase Storage
        file_url = document_content.get("file_url")
        if not file_url:
            raise HTTPException(status_code=404, detail="File URL not found")

        # Descargar el archivo desde Firebase Storage a un archivo temporal local
        bucket = storage.bucket()
        blob = bucket.blob(f"{request_id}/{file_id}")
        
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            local_file_path = temp_file.name
            blob.download_to_filename(local_file_path)

        # Devolver el archivo como respuesta de descarga
        return FileResponse(local_file_path, media_type="application/pdf", filename=document_content["filename"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
