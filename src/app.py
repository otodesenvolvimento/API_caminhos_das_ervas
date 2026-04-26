from http  import HTTPStatus
from apiflask import APIFlask, HTTPError
from db import get_db, create_tables
from  models import Product
from schemas import ProductIn, ProductFilter,ProductOut   

app  = APIFlask(__name__, title='Produtos API ')
app.json.sort_keys = False


@app.get("/")
def index():
    return " <h1>API CAMINHO DAS ERVAS</h1>"


@app.get("/products")
@app.input(ProductFilter,location="query",arg_name='filter')
@app.output(ProductOut(many=True))
def find_all_products(filter: dict):
    print(filter )
    db= get_db()
    cursor = db.cursor()

    parameters =   [] 
    query = '''  SELECT id, name, description, quantity, price
       FROM products WHERE 1 = 1
       '''
    if filter.get('search'):
         query+=' AND name LIKE ? '
         parameters.append(f"%{filter.get('search')}%")

    if filter.get('min_price'):
         query+=" AND price >= ? "
         parameters.append(filter.get("min_price"))

    if filter.get('max_price'):
         query+=" AND price <= ? "
         parameters.append(filter.get("max_price"))


    cursor.execute(query, parameters)
    rows = cursor.fetchall()

    cursor.close()
    db.close()
   
    products = [Product(*row) for row in rows]
    return products


 
@app.get("/product/<int:id>")
@app.output(ProductOut)
def  find_product_by_id(id: int):
     db = get_db()
     cursor = db.cursor()

     query = """
       SELECT id, name, description, quantity, price
       FROM products WHERE id = ?

    """
     cursor.execute(query, (id,))
     data = cursor.fetchone()


     if data is None:
          raise HTTPError(message="Produto nao encontrado", status_code=HTTPStatus.NOT_FOUND
                           )



     print(data)

     cursor.close()
     db.close()
     return Product(*data)
     #return { 'message': "kkk..."}



@app.post('/products')
@app.input(ProductIn, arg_name='product_in')
@app.output(ProductOut)
def create_products(product_in:dict):
     db= get_db()
     cursor = db.cursor() 

     parameters =(
         product_in.get("name"),
         product_in.get("description"),
         product_in.get("quantity"),
         product_in.get("price")
         )    


     query = '''INSERT INTO products(name, description, quantity,price)
         VALUES(?,?,?,?) RETURNING id   

     '''
    # # # #  parameters =(
    # # # #      product_in.get("name"),
    # # # #      product_in.get("description"),
    # # # #      product_in.get("quantity"),
    # # # #      product_in.get("price")
    # # # #      )   
     cursor.execute(query, parameters) 
     id: int = cursor.fetchone()[0]
     db.commit()
     cursor.close()
     db.close()
     
     product = Product(id,*parameters)
     return (product, HTTPStatus.CREATED)

@app.put("/product/<int:id>")
@app.output(ProductOut)
@app.input(ProductIn, arg_name='product_in')
def update_product(id: int, product_in:dict):
     db= get_db()
     cursor = db.cursor() 

    #  parameters =(
    #      product_in.get("name"),
    #      product_in.get("description"),
    #      product_in.get("quantity"),
    #      product_in.get("price")
    #      )    


     query = '''UPDATE products
                SET name = ?, description = ?, quantity = ?,price = ?
                WHERE id  = ?

     '''
     parameters =(
         product_in.get("name"),
         product_in.get("description"),
         product_in.get("quantity"),
         product_in.get("price"),
         id,
         )   
     cursor.execute(query, parameters) 
     
     db.commit()
     cursor.close()
     db.close()
     
     product = Product(id,*parameters[:-1])
     return product


@app.delete("/product/<int:id>") 
def delete_product_by_id(id: int):
    db = get_db()
    cursor = db.cursor()

    query= """
        DELETE FROM products
        where id = ?

"""
    cursor.execute(query, (id,))
    db.commit()
    cursor.close()
    db.close()

    return {"message": "Produto excluido com sucesso."}




if __name__== "__main__":
    create_tables()
    app.run(debug=True)
  