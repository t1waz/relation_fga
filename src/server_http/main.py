from robyn import Robyn
from stores.views import stores_router


app = Robyn(__file__)
app.include_router(stores_router)


@app.get("/health_check")
async def health_check(*args, **kwargs):
    return "ok"


app.start(host="0.0.0.0", port=8000)
