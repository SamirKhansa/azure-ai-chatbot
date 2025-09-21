import io

def extract_text_with_read(DIClient, uploaded_file: bytes, locale: str | None = None) -> str:
    file_stream = io.BytesIO(uploaded_file)

    poller = DIClient.begin_analyze_document(
        model_id="prebuilt-read",
        body=file_stream,
        locale=locale,          
    )
    
    result = poller.result()
    return result.content or ""