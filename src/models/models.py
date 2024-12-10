from pydantic import BaseModel, field_validator, Field
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base


# otro estilo de validacion
class ValModel(BaseModel):
    j: int
    
    @field_validator('j')
    def val(cls, value):
        if value == 0:
            raise ValueError('No puede tener largo 0')
        return value


# tipos de esquemas 
class FirstModel(BaseModel):
    n: int
    m: int
    
    
# esquemas pero validados usando pydantic.Field
class FirstModelValidate(BaseModel):
    n: int = Field(gt=0, lt=100, default=1) # gt(>) lt(<) ge(>=) le(<=) default(valor por defecto)
    m: str = Field(min_length=1, max_length=5)
    
    # json de modificacion de BaseModel
    model_config = {
        'json_schema_extra': {
            'example': {
                'm': "Hola"
            }
        }
    }


Base = declarative_base()

class Thing(Base):
    __tablename__ = "things"
    id = Column(String, primary_key=True, unique=True, index=True)
    ints = Column(Integer, nullable=True)
    floats = Column(Float, nullable=True)
    strings = Column(String, nullable=True)
    