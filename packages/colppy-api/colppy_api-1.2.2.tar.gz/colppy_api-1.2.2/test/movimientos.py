import asyncio

from groovindb.core.db import GroovinDB

from colppy import ColppyAPIClient
from colppy.models.empresas import Empresa
from db_types import GeneratedClient

async def main():
    db: GeneratedClient = GroovinDB().client
    colppy_client = ColppyAPIClient()
    await colppy_client.get_token()

    #VARIAS QUERYS, voy pidiendo segun id_tabla
    # print( await db.dev.query("select id_elemento from norm_colppy.movimientos where id_tabla = 8") )

    #UNICA QUERY, creo un dict a partir del result; KEY id_tabla VALUE id_elemento
    # print( await db.dev.query("select id_tabla, id_elemento from norm_colppy.movimientos order by id_tabla asc") )



    #! TESTING FACTURA COMPRA
    #Ahora necesito pedirle al endpoint correspondiente a cada id_tabla los datos de los id_elementos que consegui.
    #Si hago la logica de muchas querys, lo tengo "hardcodeado"

    """
    --SI SON DE COMPRA, Y SI SON CREDITO, LEO ID_ELEMENTO_APLICADO 
    --SI SON DE COMPRA, Y SI SON DEBITO, LEO ID_ELEMENTO
    
    [
    "leer_id_elemento": [ {id_empresa, id_elemento} {...} {...} ],
    "leer_id_elemento_aplicado": [ {id_empresa, id_tabla_aplicado, id_elemento_aplicado} {} {} ]
    ]
    
    select id_empresa, id_elemento from norm_colppy.movimientos where id_tabla = 19 and debito_credito = 'D';
    select id_empresa, id_tabla_aplicado, id_elemento_aplicado from norm_colppy.movimientos where id_tabla = 19 and debito_credito = 'C';

    --SI SON DE VENTA, LEO APLICADO SI ES DEBITO!
    --SI SON DE COMPRA, LEO ID_ELEMENTO SI ES CREDITO
    select * from norm_colppy.movimientos where id_tabla = 8 and debito_credito = 'C' and id_tabla_aplicado != -1 and id_tabla_aplicado != 0;

    """

    # facturas = await db.dev.query("""
    # SELECT id_elemento
    # FROM (
    #      SELECT m1.id_tabla, m1.id_elemento
    #      FROM norm_colppy.movimientos m1
    #
    #      UNION
    #
    #      SELECT m2.id_tabla_aplicado as id_tabla, m2.id_elemento_aplicado AS id_elemento
    #      FROM norm_colppy.movimientos m2
    #  ) AS mj WHERE id_tabla = 8;
    #  -- or id_tabla = 19
    # """)

    facturas = await db.dev.query("""
    SELECT mj.id_tabla, array_agg(mj.id_elemento) AS elementos, array_length(array_agg(mj.id_elemento), 1) AS cantidad_elementos
FROM (
    SELECT DISTINCT m1.id_tabla, m1.id_elemento
    FROM norm_colppy.movimientos m1

    UNION

    SELECT DISTINCT m2.id_tabla_aplicado AS id_tabla, m2.id_elemento_aplicado AS id_elemento
    FROM norm_colppy.movimientos m2
    WHERE id_tabla_aplicado > 0
) AS mj
GROUP BY mj.id_tabla
ORDER BY mj.id_tabla;
    """)

    for factura_compra in facturas:
        print(factura_compra["id_tabla"])
        for elemento in factura_compra["elementos"]:
            print(elemento)
        # print(factura_compra['id_empresa'])
        # detail = await colppy_client.get_comprobante_compra_details_by_id(id_empresa=factura_compra['id_empresa'],
        #                                                          id_comprobante=factura_compra['id_elemento'])
        # print(detail)

if __name__ == '__main__':
    asyncio.run(main())