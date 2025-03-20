import os
import json
from multiprocessing.managers import Value

import httpx
from IPython.core.ultratb import count_lines_in_py_file

from colppy.helpers.logger import logger
from colppy.models.auth import LoginRequest, LoginResponse, LogoutRequest, LogoutResponse
from colppy.models.cobro_factura import CobroFacturaResponse, CobroFacturaRequest, CobroFactura
from colppy.models.compras_pago_details import ComprasPagoDetailsRequest
from colppy.operations.config import get_config
from colppy.response.compras_pago_details_response import ComprasPagoDetailsResponse
from colppy.models.comprobante_compra_details import ComprobanteCompraDetails
from colppy.request.comprobante_compra_details_request import ComprobanteCompraDetailsRequest
from colppy.response.comprobante_compra_details_response import ComprobanteCompraDetailsResponse
from colppy.models.comprobante_venta_details import ComprobanteVentaDetails
from colppy.request.comprobante_venta_details_request import ComprobateVentaDetailsRequest
from colppy.response.comprobante_venta_details_response import ComprobanteVentaDetailsResponse
from colppy.models.comprobantes_compra import ComprobanteCompra
from colppy.request.comprobantes_compra_request import ComprobanteCompraRequest
from colppy.response.comprobantes_compra_response import ComprobanteCompraResponse
from colppy.models.comprobantes_venta import ComprobanteVenta
from colppy.request.comprobantes_venta_request import ComprobanteVentaRequest
from colppy.response.comprobantes_venta_response import ComprobanteVentaResponse
from colppy.models.movimientos import Movimiento
from colppy.request.clientes_request import ClientesRequest
from colppy.request.movimientos_request import MovimientosRequest
from colppy.response.clientes_response import ClientesResponse
from colppy.response.movimientos_response import MovimientosResponse

from colppy.request.request import request_items, request_items_paginated, Request

from colppy.models.empresas import Empresa
from colppy.request.empresas_request import EmpresasRequest
from colppy.response.empresas_response import EmpresasResponse
from colppy.models.clientes import Cliente
from colppy.models.proveedores import Proveedor
from colppy.response.proveedores_response import ProveedoresResponse
from colppy.request.proveedores_request import ProveedoresRequest
from colppy.response.response import Response


class ColppyAPIClient:
    def __init__(self):
        config = get_config()
        self._base_url = config['ColppyAPI']['COLPPY_API_URI']
        self._auth_user = config['ColppyAPI']['COLPPY_AUTH_USER']
        self._auth_password = config['ColppyAPI']['COLPPY_AUTH_PASSWORD']
        self._params_user = config['ColppyAPI']['COLPPY_PARAMS_USER']
        self._params_password = config['ColppyAPI']['COLPPY_PARAMS_PASSWORD']
        self._token = None
        self._empresas = None

    async def get_token(self) -> str or None:
        login_request = LoginRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            params_password=self._params_password
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=login_request.to_dict())
                response.raise_for_status()
                login_response = LoginResponse(response.json())
                self._token = login_response.get_token()
                logger.debug(f"Token: {self._token}")
                return login_response.get_token()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error getting token: {e}")
                return None

    async def get_empresas(self, ) -> list[Empresa]:
        empresas_request = EmpresasRequest(
            colppy_session_token=self._token
        )

        empresas = await request_items(self._base_url, empresas_request, EmpresasResponse)

        self._empresas = [empresa for empresa in empresas if empresa.id_empresa != 11675]

        return self._empresas

    async def get_all_items_by_empresa(self, request:Request, response_class:Response, empresas=None, debug_use_paging=True):
        ret: list[Cliente] = []

        if empresas is None:
            if self._empresas is None:
                raise ValueError("No se proporcionaron empresas por argumento y no habia empresas cargadas.\nHint: Llama a get_empresas().")
            empresas = self._empresas

        if not debug_use_paging:
            request.id_empresa=empresas[0].id_empresa
            ret += await request_items(self._base_url, request, response_class)

        for empresa in empresas:
            request.id_empresa=empresa.id_empresa
            ret += await request_items_paginated(self._base_url, request, response_class)

        return ret

    async def get_all_clientes(self, empresas=None) -> list[Cliente]:
        clientes_request = ClientesRequest(
            colppy_session_token=self._token,
            only_active=True,
        )
        return await self.get_all_items_by_empresa(clientes_request, ClientesResponse)

    async def get_all_proveedores(self, empresas=None) -> list[Proveedor]:
        proveedores_request = ProveedoresRequest(
            colppy_session_token=self._token,
        )
        return await self.get_all_items_by_empresa(proveedores_request, ProveedoresResponse)

    async def get_all_movimientos(self, empresas=None, from_date="2013-01-01", to_date="2040-01-01") -> list[Movimiento]:
        movimientos_request = MovimientosRequest(
            colppy_session_token=self._token,
            from_date=from_date,
            to_date=to_date
        )
        return await self.get_all_items_by_empresa(movimientos_request, MovimientosResponse)

    async def get_all_comprobantes_compra(self, empresas=None) -> list[ComprobanteCompra]:
        ret: list[ComprobanteCompra] = []

        if empresas is None:
            empresas = self._empresas

        for empresa in empresas:
            ret += await self.get_comprobantes_compras_by_empresa(empresa)

        return ret

    async def get_comprobante_compra_details_by_id(self, id_empresa="", id_factura=""):
        comprobante_details_request = ComprobanteCompraDetailsRequest(
            colppy_session_token=self._token,
            id_empresa=id_empresa,
            id_factura=id_factura
        )

        return await request_items(self._base_url, comprobante_details_request,
                                             ComprobanteCompraDetailsResponse)

    async def get_comprobante_venta_details_by_id(self,  id_empresa="", id_factura=""):
        comprobante_details_request = ComprobateVentaDetailsRequest(
            colppy_session_token=self._token,
            id_empresa=id_empresa,
            id_factura=id_factura,
        )

        return await request_items(self._base_url, comprobante_details_request,
                                             ComprobanteVentaDetailsResponse)


    ############################################ NO SE USAN ###################################################################



    async def get_comprobantes_compras_by_empresa(self, empresa: Empresa, id_tipo_comprobante=None, filters=None,
                                                  start=0, limit=100):
        comprobantes_compra_request = ComprobanteCompraRequest(
            colppy_session_token=self._token,
            id_empresa=empresa.id_empresa,
            id_tipo_comprobante=id_tipo_comprobante,
            filters=filters
        )

        # TODO: usar request paginated
        # return await request_items_paginated(self._base_url, comprobantes_compra_request, ComprobanteCompraResponse)
        return await request_items(self._base_url, comprobantes_compra_request, ComprobanteCompraResponse)

    async def get_all_comprobantes_venta(self, empresas=None) -> list[ComprobanteVenta]:
        ret: list[ComprobanteVenta] = []

        if empresas is None:
            empresas = self._empresas

        for empresa in empresas:
            ret += await self.get_comprobantes_ventas_by_empresa(empresa)

        return ret

    async def get_comprobantes_ventas_by_empresa(self, empresa: Empresa, id_tipo_comprobante=None, filters=None,
                                                 start=0, limit=100):
        comprobantes_venta_request = ComprobanteVentaRequest(
            colppy_session_token=self._token,
            id_empresa=empresa.id_empresa,
            id_tipo_comprobante=id_tipo_comprobante,
            filters=filters
        )

        # TODO: usar request paginated
        # return await request_items_paginated(self._base_url, comprobantes_venta_request, ComprobanteVentaResponse)
        return await request_items(self._base_url, comprobantes_venta_request, ComprobanteVentaResponse)

    #TODO: Creo que no anda. Solo sirve para poblar la DB.
    async def get_all_comprobante_compra_details_by_id(self, empresas=None) -> list[ComprobanteCompraDetails]:
        ret: list[ComprobanteCompraDetails] = []

        if empresas is None:
            empresas = self._empresas

        for empresa in empresas:
            comprobantes_empresa = await self.get_comprobantes_compras_by_empresa(empresa)
            for comprobante in comprobantes_empresa:
                ret.append(await self.get_comprobante_compra_details_by_id(empresa, comprobante.id_factura))

        return ret


    async def get_all_comprobante_venta_details_by_id(self, empresas=None) -> list[ComprobanteVentaDetails]:
        ret: list[ComprobanteVentaDetails] = []

        if empresas is None:
            empresas = self._empresas

        for empresa in empresas:
            comprobantes_empresa = await self.get_comprobantes_ventas_by_empresa(empresa)
            for comprobante in comprobantes_empresa:
                ret.append(await self.get_comprobante_venta_details_by_id(empresa, comprobante.id_factura))

        return ret


    async def get_all_cobro_factura(self, empresas=None) -> list[CobroFactura]:
        ret: list[CobroFactura] = []

        if empresas is None:
            empresas = self._empresas

        for empresa in empresas:
            comprobantes_empresa = await self.get_comprobantes_compras_by_empresa(empresa)
            for comprobante in comprobantes_empresa:
                ret.append(await self.get_cobro_factura_by_id(empresa, comprobante.id_factura))

        return ret

    async def get_cobro_factura_by_id(self, empresa: Empresa, id_factura) -> list[CobroFactura]:
        cobro_factura_request = CobroFacturaRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token,
            id_empresa=empresa.id_empresa,
            id_factura=id_factura
        )

        # TODO: usar request paginated
        return await request_items(self._base_url, cobro_factura_request, CobroFacturaResponse)

    async def logout(self):
        logout_request = LogoutRequest(
            auth_user=self._auth_user,
            auth_password=self._auth_password,
            params_user=self._params_user,
            token=self._token
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self._base_url, json=logout_request.to_dict())
                response.raise_for_status()
                logout_response = LogoutResponse(response.json())
                logger.debug(f"Logout: {logout_response.get_logout()}")
                return logout_response.get_logout()
            except httpx.HTTPStatusError as e:
                logger.error(f"Error logging out: {e}")
                return False
