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




@app.get("/")
def home():
    return {"message": "Backend is running"}