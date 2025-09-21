import azure.functions as func
import json
def UserMessageError(Message, statuscode):
    return func.HttpResponse(
        json.dumps({"error": Message}),
        status_code=statuscode,
        mimetype="application/json"
)

def SystemError(Error):
    return func.HttpResponse(
        json.dumps({"error": str(Error)}),
        status_code=500,
        mimetype="application/json"
    )