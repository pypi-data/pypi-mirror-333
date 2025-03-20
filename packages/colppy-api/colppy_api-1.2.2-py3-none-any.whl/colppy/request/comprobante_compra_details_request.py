from colppy.request.request import Request


class ComprobanteCompraDetailsRequest(Request):
    def __init__(self, colppy_session_token="",
                 id_empresa="", id_factura=""):
        if not id_empresa:
            raise ValueError("Se debe proporcionar un id_factura!")
        if not id_factura:
            raise ValueError("Se debe proporcionar un id_empresa")

        super().__init__(
            colppy_session_token=colppy_session_token,
            provision="FacturaCompra",
            operacion="leer_facturacompra",
            id_empresa=id_empresa,
            id_factura=id_factura,
            admits_paging=False
        )
