import asyncio

from groovindb.core.db import GroovinDB

from colppy import ColppyAPIClient
from colppy.helpers.formatters import sql_bulk
from colppy.models.empresas import Empresa
from colppy.request.request import request_items_paginated
from colppy.response.comprobante_venta_details_response import ComprobanteVentaDetailsResponse
from db_types import GeneratedClient


async def main():
    db: GeneratedClient = GroovinDB().client
    colppy_client = ColppyAPIClient()
    await colppy_client.get_token()
    empresas = await colppy_client.get_empresas()
    for empresa in empresas:
        print(empresa.id_empresa, empresa.razon_social)

    movimientos_by_tabla = await db.dev.query("""
        SELECT mj.id_tabla, array_agg(mj.id_elemento) AS elementos, array_agg(mj.id_empresa) AS id_empresas, array_length(array_agg(mj.id_elemento), 1) AS cantidad_elementos
    FROM (
        SELECT DISTINCT m1.id_tabla, m1.id_elemento, m1.id_empresa
        FROM norm_colppy.movimientos m1

        UNION

        SELECT DISTINCT m2.id_tabla_aplicado AS id_tabla, m2.id_elemento_aplicado AS id_elemento, m2.id_empresa
        FROM norm_colppy.movimientos m2
        WHERE id_tabla_aplicado > 0
    ) AS mj
    GROUP BY mj.id_tabla
    ORDER BY mj.id_tabla;
        """)

    # factura de compra 8  --  factura de venta 19
    for tabla in movimientos_by_tabla:
        if tabla["id_tabla"] == 19:
            for i in range(0, len(tabla["elementos"])):
                print(f"EMPRESA {tabla['id_empresas'][i]}")
                print(f"IDFACTURA {tabla['elementos'][i]}")
                comprobante_venta = await colppy_client.get_comprobante_venta_details_by_id(id_empresa=tabla['id_empresas'][i],
                                                                                            id_factura=tabla['elementos'][i])
                print(sql_bulk(schema_db="norm_colppy", table_name="vista_comprobantes", models=[comprobante_venta]))

    # factura de compra 8  --  factura de venta 19
    # for tabla in movimientos_by_tabla:
    #     if tabla["id_tabla"] == 8:
    #         for i in range(0, len(tabla["elementos"])):
    #             print(f"EMPRESA {tabla['id_empresas'][i]}")
    #             print(f"IDFACTURA {tabla['elementos'][i]}")
    #             comprobante_compra = await colppy_client.get_comprobante_compra_details_by_id(id_empresa=tabla['id_empresas'][i],
    #                                                                                           id_factura=tabla['elementos'][i])
    #             print(comprobante_compra)
    #             print(sql_bulk(schema_db="norm_colppy", table_name="vista_comprobantes", models=[comprobante_compra]))




    #TODO: Tratar a los items por separado! (puedo sacar los items de la request y llamarle sql_bulk directo,
    #                                        es literalmente una lista de objetos comprobantedetailsitem!)
    #6023, 41533763
    # comprobante_venta = await colppy_client.get_comprobante_venta_details_by_id(id_empresa="6023", id_comprobante=41533763)
    # qry = sql_bulk(models=[comprobante_venta], schema_db="norm_colppy", table_name="vista_comprobantes")
    # print(qry)
    # await db.dev.execute(qry)


"""
ID_TABLA PARA FACTURAS VENTA (SEGUN CODIGO AIRFLOW VIEJO facturas_cobrar.py)
["FAC", "NCC", "NDC", "FAV", "NCV", "NDV", "FCC", "FVC", "", "NVE"]
[  8       8     8       19    19     19     19     19      no existe]
"""


"""
--OBSOLETO!!!!!
--SI SON DE COMPRA, Y SI SON CREDITO, LEO ID_ELEMENTO_APLICADO 
--SI SON DE COMPRA, Y SI SON DEBITO, LEO ID_ELEMENTO
select * from norm_colppy.movimientos where id_tabla = 19 and debito_credito = 'D' and id_tabla_aplicado != -1 and id_tabla_aplicado != 0;

--SI SON DE VENTA, LEO APLICADO SI ES DEBITO!
--SI SON DE COMPRA, LEO ID_ELEMENTO SI ES CREDITO
select * from norm_colppy.movimientos where id_tabla = 8 and debito_credito = 'C' and id_tabla_aplicado != -1 and id_tabla_aplicado != 0;

"""

if __name__ == "__main__":
    asyncio.run(main())