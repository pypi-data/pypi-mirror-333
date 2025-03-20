from dataclasses import dataclass, field
from typing import TypedDict

from colppy.helpers.formatters import BaseModel


class FilterItem(TypedDict):
    field: str
    op: str
    value: str | int


class OrderItem(TypedDict):
    field: str
    dir: str


@dataclass(init=False)
class Proveedor(BaseModel):
    id_proveedor: int = field(metadata={"alias": "idProveedor", "field_name": "id_colppy", "unique": True}, default=None)  #
    razon_social: str = field(metadata={"alias": "RazonSocial"}, default=None)  #
    nombre_fantasia: str = field(metadata={"alias": "NombreFantasia"}, default=None)  #
    fecha_alta: str = field(metadata={"alias": "FechaAlta", "to_sql": False}, default=None)
    dir_postal: str = field(metadata={"alias": "DirPostal", "to_sql": False}, default=None)
    dir_postal_ciudad: str = field(metadata={"alias": "DirPostalCiudad", "to_sql": False}, default=None)
    dir_postal_codigo_postal: str = field(metadata={"alias": "DirPostalCodigoPostal", "to_sql": False}, default=None)
    dir_postal_provincia: str = field(metadata={"alias": "DirPostalProvincia", "to_sql": False}, default=None)
    dir_postal_pais: str = field(metadata={"alias": "DirPostalPais", "to_sql": False}, default=None)
    dir_fiscal: str = field(metadata={"alias": "DirFiscal", "to_sql": False}, default=None)
    dir_fiscal_ciudad: str = field(metadata={"alias": "DirFiscalCiudad", "to_sql": False}, default=None)
    dir_fiscal_codigo_postal: str = field(metadata={"alias": "DirFiscalCodigoPostal", "to_sql": False}, default=None)
    dir_fiscal_provincia: str = field(metadata={"alias": "DirFiscalProvincia", "to_sql": False}, default=None)
    dir_fiscal_pais: str = field(metadata={"alias": "DirFiscalPais", "to_sql": False}, default=None)
    telefono: str = field(metadata={"alias": "Telefono", "to_sql": False}, default=None)
    activo: int = field(metadata={"alias": "Activo", "to_sql": False}, default=0)
    id_condicion_pago: int = field(metadata={"alias": "idCondicionPago", "to_sql": False}, default=0)
    id_condicion_iva: int = field(metadata={"alias": "idCondicionIva", "to_sql": False}, default=0)
    cuit: str = field(metadata={"alias": "CUIT", "to_sql": False}, default=None)
    producto: str = field(metadata={"alias": "Producto", "to_sql": False}, default=None)
    certificado_exclusion: str = field(metadata={"alias": "CertificadoExclusion", "to_sql": False}, default=None)
    id_plan_cuenta: int = field(metadata={"alias": "idPlanCuenta", "to_sql": False}, default=0)
    nro_cuenta: str = field(metadata={"alias": "NroCuenta", "to_sql": False}, default=None)
    cbu: str = field(metadata={"alias": "CBU", "to_sql": False}, default=None)
    banco: str = field(metadata={"alias": "Banco", "to_sql": False}, default=None)
    des_banco: str = field(metadata={"alias": "DesBanco", "to_sql": False}, default=None)
    porcentaje_iva: float = field(metadata={"alias": "porcentajeIVA", "to_sql": False}, default=0.0)
    id_ret_ganancias: int = field(metadata={"alias": "idRetGanancias", "to_sql": False}, default=0)
    email: str = field(metadata={"alias": "Email", "to_sql": False}, default=None)
    saldo: float = field(metadata={"alias": "Saldo", "to_sql": False}, default=0.0)


