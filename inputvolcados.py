from sqlalchemy import Column, String, Integer, BigInteger, Date, JSON, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import json
import pandas as pd

import requests

Base = declarative_base()

# Clase para manejar la estructura de comercio de la tabla ayc_comercio
# Sirve de base para las llamadas de volcado
class Comercio(Base):
    __tablename__ = 'ayc_comercio'
    __table_args__ = {'schema': 'afiliacionycontrato'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    commerce_rut = Column(String(13), unique=True, name="rut_comercio")
    commerce_mail = Column(String(100), nullable=False, name="mail_comercio")
    social_reason = Column(String(200), nullable=False, name="razon_social")
    fantasy_name = Column(String(200), name="nombre_fantasia")
    direction = Column(String(200), name="direccion")
    giro = Column(BigInteger, name="giro")
    comuna = Column(BigInteger, name="comuna")
    region = Column(BigInteger, name="region")

    commerce_status = Column(JSONB, name="estado_comercio")
    commerce_contact = Column(JSONB, name="contacto_comercio")
    legal_representatives = Column(JSONB, name="representante_legal")
    bank_account = Column(JSONB, name="cuenta_bancaria")
    identity_validation = Column(JSONB, name="validacion_identidad")
    dump_information = Column(JSONB, name="informacion_volcados")
    uaf = Column(JSONB, name="uaf")

    created = Column(Date, default=datetime.utcnow, name="fecha_creacion")
    status = Column(Integer, name="estado")
    last_update = Column(Date, default=datetime.utcnow, name="fecha_ultima_modificacion", nullable=True)

    validity_address = Column(Boolean, default=False, name="direccion_validada")
    validity_commerce = Column(Boolean, default=False, name="validacion_plutto")

    origin = Column(String(30), name="origen")
    phone = Column(String(10), name="telefono")

    additional_information = Column(JSONB, name="informacion_adicional", nullable=True)
    active_promotion = Column(String, name="promocion_activa")
    temp_code = Column(JSONB, name="codigo_temporal")

    executive_rut = Column(String, default="5-1", nullable=False, name="rut_ejecutivo")
    canal = Column(String, default="AUTOAFILIACION_KLAP", nullable=False, name="canal")

    configuration_type = Column(String, nullable=False, name="tipo_despacho")

    def __repr__(self):
        return f"<Comercio(id={self.id}, commerce_rut={self.commerce_rut}, commerce_mail={self.commerce_mail})>"

# Clase para manejar la estructura de la tabla ayc_sucursal
# Sirve de base para la información del volcado
class Sucursal(Base):
    __tablename__ = 'ayc_sucursal'
    __table_args__ = {'schema': 'afiliacionycontrato'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    commerce_id = Column(BigInteger, name="id_comercio")
    terminals = Column(JSONB, name="terminales")
    services = Column(JSONB, name="servicios")
    accounts_settings = Column(JSONB, name="configuracion_cuentas")
    mcc = Column(BigInteger, nullable=False, name="mcc")
    id_giro = Column(BigInteger, nullable=False, name="id_giro")
    state = Column(BigInteger, nullable=False, name="estado")
    economic_activity_code = Column(BigInteger, nullable=False, name="codigo_actividad_economica")
    delivery_date_pos = Column(Date, name="fecha_entrega_pos")

    def __repr__(self):
        return f"<Sucursal(id={self.id}, commerce_id={self.commerce_id}, state={self.state})>"


# Clase que contiene toda la información, tanto de comercio como sucursales
# Sigue la misma estructura que la encontrada en el consumer volcado
# Esta clase envía toda la información de la base de datos
# Tiene los datos generales del comercio, y una lista de sucursales
# Los terminales van internos en las sucursales, casi todo lo demás en comercio

# Por el momento no estamos considerando desarmarla en otras entidades

class VolcadoComercio:
    def __init__(self, comercio, sucursales):
        self.comercio = comercio
        self.sucursales = sucursales

    def to_json(self):
        return json.dumps({
            "comercio": self.comercio.__dict__,
            "sucursales": [s.__dict__ for s in self.sucursales]
        }, default=str, indent=4)
    
    @staticmethod
    def from_excel(file_path):
        column_mapping_comercio = {
            "rut_comercio": "commerce_rut",
            "mail_comercio": "commerce_mail",
            "razon_social": "social_reason",
            "nombre_fantasia": "fantasy_name",
            "direccion": "direction",
            "giro": "giro",
            "comuna": "comuna",
            "region": "region",
            "estado_comercio": "commerce_status",
            "contacto_comercio": "commerce_contact",
            "representante_legal": "legal_representatives",
            "cuenta_bancaria": "bank_account",
            "validacion_identidad": "identity_validation",
            "informacion_volcados": "dump_information",
            "uaf": "uaf",
            "fecha_creacion": "created",
            "estado": "status",
            "fecha_ultima_modificacion": "last_update",
            "direccion_validada": "validity_address",
            "validacion_plutto": "validity_commerce",
            "origen": "origin",
            "telefono": "phone",
            "informacion_adicional": "additional_information",
            "promocion_activa": "active_promotion",
            "codigo_temporal": "temp_code",
            "rut_ejecutivo": "executive_rut",
            "canal": "canal",
            "tipo_despacho": "configuration_type"
        }
        
        column_mapping_sucursal = {
            "id_comercio": "commerce_id",
            "terminales": "terminals",
            "servicios": "services",
            "configuracion_cuentas": "accounts_settings",
            "mcc": "mcc",
            "id_giro": "id_giro",
            "estado": "state",
            "codigo_actividad_economica": "economic_activity_code",
            "fecha_entrega_pos": "delivery_date_pos"
        }
        
        xls = pd.ExcelFile(file_path)
        df_comercio = pd.read_excel(xls, sheet_name="Comercio").rename(columns=column_mapping_comercio).fillna("")
        df_sucursal = pd.read_excel(xls, sheet_name="Sucursal").rename(columns=column_mapping_sucursal).fillna("")
        
        comercio_data = df_comercio.iloc[0].to_dict()
        comercio = Comercio(**comercio_data)
        
        sucursales = [Sucursal(**row.to_dict()) for _, row in df_sucursal.iterrows()]
        
        return VolcadoComercio(comercio, sucursales)


    