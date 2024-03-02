from robyn import Robyn

from backend.views.auth.views import auth_router

app = Robyn(__file__)
app.include_router(auth_router)


@app.get("/health")
async def health_check(*args, **kwargs):
    return "ok"

app.set_response_header("content-type", "application/json")
app.start(host="0.0.0.0", port=8000)
