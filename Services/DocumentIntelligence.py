import io

def extract_text_with_read(DIClient, uploaded_file: bytes, locale: str | None = None) -> str:
    print("entering document intelligence")
    try:
        file_stream = io.BytesIO(uploaded_file)

        poller = DIClient.begin_analyze_document(
            model_id="prebuilt-read",
            body=file_stream,
            locale=locale,          
        )
        print("Problem is with Document Intelligence")
        result = poller.result()
        return result.content or ""
    except Exception as e:
        print("Error in document intellignece ",e)
        return ""