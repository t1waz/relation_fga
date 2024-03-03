from robyn import Robyn, ALLOW_CORS

from backend.repositories import user_repository, store_repository
from backend.views.auth.views import auth_router
from backend.views.stores.views import stores_router


async def create_indexes() -> None:
    await user_repository.create_indexes()
    await store_repository.create_indexes()

    from backend.core.entites import User, Store

    root_user = User(email="root@example.com", password="root")
    store_1 = Store(owner=root_user, name="store foo 1")
    store_2 = Store(owner=root_user, name="store foo 2")
    store_3 = Store(owner=root_user, name="store foo 3")
    # try:
    #     await user_repository.save(user=root_user)
    #     await store_repository.save(store=store_1)
    #     await store_repository.save(store=store_2)
    #     await store_repository.save(store=store_3)
    # except:
    #     pass


app = Robyn(__file__)
ALLOW_CORS(app, origins=["*"])

app.include_router(auth_router)
app.include_router(stores_router)

app.startup_handler(create_indexes)

app.set_response_header("content-type", "application/json")


@app.get("/health")
async def health_check(*args, **kwargs):
    return "ok"


app.start(host="0.0.0.0", port=8000)
