from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.models.user import User
from app.models import *
from app.middleware.refreshed_tokens import RefreshedTokenMiddleware
from app.routes.users import router as user_router
from app.routes.payment import router as payment_router
from app.routes.plan import router as plan_router
from app.routes.label import router as labels_router
from app.routes.packs import router as packs_router
from app.routes.songs import router as songs_router
from app.routes.genre import router as genre_router
from app.routes.genre_category import router as genre_category_router
from app.routes.notification_settings import router as notification_settings_router
from app.routes.presets import router as presets_router
from app.routes.instruments import router as instruments_router
from app.routes.faqs import router as faqs_router
from app.routes.payment_method import router as payment_method_router
from app.routes.auth import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Auth middleware first so it wraps responses after CORS
app.add_middleware(RefreshedTokenMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "X-Access-Token",
        "X-Access-Token-Expires-At",
        "X-Refresh-Token",
        "X-Refresh-Token-Expires-At",
        "X-Token-Refreshed",
    ],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(payment_router)
app.include_router(plan_router)
app.include_router(labels_router)
app.include_router(packs_router)
app.include_router(songs_router)
app.include_router(genre_router)
app.include_router(genre_category_router)
app.include_router(notification_settings_router)
app.include_router(presets_router)
app.include_router(instruments_router)
app.include_router(faqs_router)
app.include_router(payment_method_router)


@app.get("/")
def home():
    return {"message": "Backend is running"}
