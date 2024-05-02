from flask import Flask, render_template, redirect, url_for
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'DulceSabor'
DATABASE_USERNAME = 'sa'
DATABASE_PASSWORD = 'DABSceptile'

SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?driver=ODBC Driver 17 for SQL Server'

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)

# Función para obtener los pedidos en proceso
def obtener_pedidos_en_proceso():
    query = text("""
        SELECT
            p.id_pedido,
            c.nombre AS nombre_comida,
            c.precio AS costo_comida
        FROM
            detalle_de_pedido dp
            JOIN pedido p ON dp.id_pedido = p.id_pedido
            JOIN comida c ON dp.id_comida = c.id_comida
        WHERE
            p.estado = 'En Proceso'
        ORDER BY
            p.id_pedido;
    """)
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    session = Session()
    resultados = session.execute(query).fetchall()
    session.close()
    return resultados

# Función para obtener los detalles de la tabla comida
def obtener_detalles_comida():
    query = text("SELECT * FROM comida;")
    session = Session();
    resultados = session.execute(query).fetchall()
    session.commit()
    session.close()
    return resultados

# Función para obtener los detalles de la tabla detalle_de_pedido
def obtener_detalles_pedido():
    query = text("""SELECT * FROM detalle_de_pedido;""")
    session = Session()
    resultados = session.execute(query).fetchall()
    session.close()
    return resultados

# Función para obtener los detalles de la tabla pedido
def obtener_estados_pedido():
    query = text("""SELECT * FROM pedido;""")
    session = Session()
    resultados = session.execute(query).fetchall()
    session.close()
    return resultados

@app.route('/')
def index():
    pedidos = obtener_pedidos_en_proceso()
    detalles_comida = obtener_detalles_comida()
    detalles_pedido = obtener_detalles_pedido()
    estados_pedido = obtener_estados_pedido()

    print("Número de registros en detalles_comida:", len(detalles_comida))

    return render_template('index.html', pedidos=pedidos, detalles_comida=detalles_comida, detalles_pedido=detalles_pedido, estados_pedido=estados_pedido)

def pagina_no_encontrada(error):
    # return render_template('404.html'), 404
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
    
