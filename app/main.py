from fastapi import  FastAPI 
from app.core.database import Base, engine
from app.models.user import User
from app.models import *
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





Base.metadata.create_all(bind =engine)

app = FastAPI()

app.include_router(user_router)
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




@app.get("/")
def home():
    return {"message": "Backend is running"}