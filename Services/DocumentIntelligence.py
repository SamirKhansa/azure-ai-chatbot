def extract_text_with_read(DIClient, file_path: str, locale: str | None = None) -> str:
    with open(file_path, "rb") as f:
        poller = DIClient.begin_analyze_document(
            model_id="prebuilt-read",
            body=f,
            locale=locale,          
        )
    result = poller.result()
    
    return result.content or ""

# document_text = extract_text_with_read(DIClient,"../Documents/PDF Documents/Chess opening.pdf", locale="en")