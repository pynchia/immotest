from app import models, schemas
from app.crud.base import CRUDBase


class CRUDArtist(CRUDBase[models.Artist, schemas.ArtistCreate, schemas.ArtistUpdate]):
    pass


artist = CRUDArtist(models.Artist)
