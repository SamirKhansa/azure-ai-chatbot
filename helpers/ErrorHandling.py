import azure.functions as func
import json
def UserMessageError():
    return func.HttpResponse(
        json.dumps({"error": "Please provide a 'message' in JSON"}),
        status_code=400,
        mimetype="application/json"
)

def SystemError(Error):
    return func.HttpResponse(
        json.dumps({"error": str(Error)}),
        status_code=500,
        mimetype="application/json"
    )