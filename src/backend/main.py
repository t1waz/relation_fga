from robyn import Robyn

from backend.repositories import user_repository
from backend.views.auth.views import auth_router


async def create_indexes() -> None:
    await user_repository.create_indexes()

    from backend.core.entites import User
    root_user = User(email="root@example.com", password="root")
    await user_repository.save(user=root_user)


app = Robyn(__file__)
app.include_router(auth_router)
app.startup_handler(create_indexes)
app.set_response_header("content-type", "application/json")


@app.get("/health")
async def health_check(*args, **kwargs):
    return "ok"


app.start(host="0.0.0.0", port=8000)
