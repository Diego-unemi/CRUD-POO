from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient,VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        validar=Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(35,2);print(blue_color+"Registro de Cliente")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del cliente
        gotoxy(2,4);print(cyan_color+'Ingrese Dni:'+reset_color)
        dni = validar.cedula(green_color+'Error: Dni Invalido'+reset_color,15,4)
        nombre = input("Ingrese la nombre del cliente: ")
        apellido = input("Ingrese el apellido del cliente: ")
        # Crear el objeto Cliente
        cliente = validar.solo_letras(green_color+'cliente es regular o vip: ','Error: Eliga una de las dos opciones'+reset_color)
        if cliente == 'regular':
            new_client = RegularClient(nombre,apellido,dni,card=True)
        elif cliente == 'vip':
            new_client = VipClient(nombre,apellido,dni)
            VipClient.limit= int(input('ingrese limite de credito entre 10000-20000:'))
        else:
            pass
        # Guardar el producto
        gotoxy(15,10);print(red_color+"¿Está seguro de grabar el cliente (s/n): ")
        gotoxy(56,10);procesar = input().lower()
        if procesar == "s":
            # Guardar el cliente en el archivo JSON
            json_file = JsonFile(path+'/archivos/clients.json')
            clients = json_file.read()
            clients.append(new_client.getJson())
            json_file.save(clients)
            gotoxy(15,11);print("😊 cliente registrado satisfactoriamente 😊"+reset_color)
        else:
            gotoxy(20,11);print("❌ Registro de cliente cancelado ❌"+reset_color)
            time.sleep(2)
    def update(self):
        validar=Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(35,2);print(blue_color+"Edicion de clientes")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del cliente
        gotoxy(2,4);print(cyan_color+'Ingrese Dni a editar:'+reset_color)
        dni = validar.cedula(green_color+'Error: Dni Invalido'+reset_color,24,4)
        if dni.isdigit():
            json_file = JsonFile(path+'/archivos/clients.json')
            clients = json_file.read()
            client_index = None
            for i, client in enumerate(clients):
                if client["dni"] == dni:
                    client_index = i
                    break
            if client_index is not None:
                print(f'Cliente encontrado: {clients[client_index]}')
                clients[client_index]['nombre'] = input("Ingrese el nuevo nombre: ")
                clients[client_index]['apellido'] = input("Ingrese el nuevo apellido: ")
                cliente = validar.solo_letras(green_color+'cliente es regular o vip: ','Error: eliga alguna de las dos opciones'+reset_color)
                if cliente == 'regular':
                    clients[client_index]['valor'] = float(input("Ingrese el nuevo valor del descuento: "))
                elif cliente == 'vip':
                    clients[client_index]['valor'] = int(input("Ingrese el nuevo limite del crédito: "))
                else:
                    pass
                
                json_file.save(clients)
                print('Cliente editado satisfactoriamente.'+reset_color)
            else:
                print('No se encuentra dicho cliente a editar'+reset_color)
        else:
            print('DNI inválido'+reset_color)

    def delete(self):
        validar=Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(35,2);print(blue_color+"Eliminacion de clientes")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del cliente
        gotoxy(2,4);print(cyan_color+'Ingrese el dni a eliminar:'+reset_color)
        dni = validar.cedula(green_color+'Error: Dni Invalido'+reset_color,29,4)
        if dni.isdigit():
            json_file = JsonFile(path+'/archivos/clients.json')
            dato = json_file.read()
            clients = json_file.find("dni", dni)
            if clients:
                dato.remove(clients[0])
                json_file.save(dato)
                print("Cliente eliminado exitosamente."+reset_color)
            else:
                print("Usuario inexistente."+reset_color)
        else:
            print("DNI inválido."+reset_color)

    def consult(self):
        validar=Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(35,2);print(blue_color+"Consulta de clientes")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del cliente
        gotoxy(2,4);print(cyan_color+'Ingrese el dni o pulse enter para consultar a todos los clientes:'+reset_color)
        dni = validar.cedula(green_color+'Error: Dni Invalido'+reset_color,68,4)
        if dni.isdigit():
            json_file = JsonFile(path+'/archivos/clients.json')
            dni_clients = json_file.find("dni",dni)
            print(f"Impresion del cliente:{dni}")
            print(dni_clients+reset_color)
        else:   
            json_file = JsonFile(path+'/archivos/clients.json')
            dni_clients = json_file.read()
            print("Consulta de clientes")
            for cli in dni_clients:
                print(f"{cli['dni']}   {cli['nombre']}   {cli['apellido']}   {cli['valor']}")

class CrudProducts(ICrud):
    def create(self):
        validar= Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Producto")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del producto
        gotoxy(2,4);print(cyan_color+'Ingrese el ID a crear:'+reset_color)
        id = validar.solo_numeros(green_color+'Error: ID Invalido'+reset_color,22,4)
        descrip = input("Ingrese la descripción del producto: ")
        preci = float(input("Ingrese el precio del producto: "))
        stock = int(input("Ingrese el stock del producto: "))
        # Crear el objeto Producto
        new_product = Product(id, descrip, preci, stock)
        # Guardar el producto
        gotoxy(15,10);print(red_color+"¿Está seguro de grabar el producto? (s/n): ")
        gotoxy(56,10);procesar = input().lower()
        if procesar == "s":
            # Guardar el producto en el archivo JSON
            json_file = JsonFile(path+'/archivos/products.json')
            products = json_file.read()
            products.append(new_product.getJson())
            json_file.save(products)
            gotoxy(15,11);print("😊 Producto registrado satisfactoriamente 😊"+reset_color)
        else:
            gotoxy(20,11);print("❌ Registro de producto cancelado ❌"+reset_color)
            time.sleep(2)

    def update(self):
        validar=Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(35,2);print(blue_color+"Edicion de Productos")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del producto
        gotoxy(2,4);print(cyan_color+'Ingrese el ID a editar:'+reset_color)
        id = validar.solo_numeros(green_color+'Error: ID Invalido'+reset_color,26,4)
        if id:
            json_file = JsonFile(path+'/archivos/products.json')
            products = json_file.read()
            product_index = None
            for i, client in enumerate(products):
                if client["id"] == id:
                    product_index = i
                    break
            if product_index is not None:
                print(f'Producto encontrado: {products[product_index]}')
                products[product_index]['descripcion'] = input("Ingrese la nueva descripcion: ")
                products[product_index]['precio'] = float(input("Ingrese el nuevo precio: "))
                products[product_index]['stock'] = int(input("Ingrese el cuanto stock posee: "))
                json_file.save(products)
                print('producto editado satisfactoriamente.'+reset_color)
            else:
                print('No se encuetra dicho producto a editar'+reset_color)
        else:
            print('id del producto invalido'+reset_color)
    
    def delete(self):
        validar=Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Eliminacion de producto")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del producto
        gotoxy(2,4);print(cyan_color+'Ingrese el ID a Eliminar:'+reset_color)
        id = validar.solo_numeros(green_color+'Error: ID Invalido'+reset_color,28,4)
        if id:
            json_file = JsonFile(path+'/archivos/products.json')
            dato = json_file.read()
            products = json_file.find("id", id)
            if products:
                dato.remove(products[0])
                json_file.save(dato)
                print("producto eliminado exitosamente."+reset_color)
            else:
                print("producto inexistente."+reset_color)
        else:
            print("producto inválido."+reset_color)
        
    
    def consult(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Consulta de Productos")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del producto
        gotoxy(2,4);id= input(cyan_color+"Ingrese el ID o pulse enter para consultar a todos los productos: "+reset_color)
        if id.isdigit():
            id = int(id)
            json_file = JsonFile(path+'/archivos/products.json')
            id_products = json_file.find("id",id)
            print(f"Impresion del cliente:{id}")
            print(id_products+reset_color)
        else:    
            json_file = JsonFile(path+'/archivos/products.json')
            id_products = json_file.read()
            print("Consulta de productos")
            for prod in id_products:
                print(f"{prod['id']}   {prod['descripcion']}   {prod['precio']}   {prod['stock']}")

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(56,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("❌ Venta Cancelada ❌"+reset_color)    
        time.sleep(2)    
    
    def update(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Edicion de ventas")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del cliente
        invoice = input("Ingrese el id de la factura a editar: ")
        if invoice.isdigit():
            invoice= int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            invoice_index = None
            for i, invoice_fac in enumerate(invoices):
                if invoice_fac["factura"] == invoice:
                    invoice_index = i
                    break
            if invoice_index is not None:
                print(f'Producto encontrado: {invoices[invoice_index]}')
                invoices[invoice_index]['producto'] = input("Ingrese nueve producto: ")
                invoices[invoice_index]['cantidad'] = int(input("Ingrese nueva cantidad: "))
                json_file.save(invoices)
                print(f'Producto modificado: {invoices[invoice_index]}')
                print('producto editado satisfactoriamente.'+reset_color)
            else:
                print('No se encuetra dicho producto a editar'+reset_color)
        else:
            print('id del producto invalido'+reset_color)
    
    def delete(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Eliminacion de factura")
        gotoxy(2,3);print(purple_color+"*"*90+reset_color)
        # Obtener detalles del producto
        invoice = input("Ingrese el # de Factura a eliminar: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            dato = json_file.read()
            invoices = json_file.find("factura",invoice)            
            if invoices:
                dato.remove(invoices[0])
                json_file.save(dato)
                print("# factura eliminada exitosamente."+reset_color)
            else:
                print("# factura inexistente."+reset_color)
        else:
            print("# factura inválida."+reset_color)
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2),invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x=input("presione una tecla para continuar..."+reset_color)    

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("💵 Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],10,3)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()
            clients = CrudClients()
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],10,3)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                clients.create()
            elif opc1 == "2":
                clients.update()
            elif opc1 == "3":
                clients.delete()
            elif opc1 == "4":
                clients.consult()
            print("Regresando al menu Facturacion...")
            time.sleep(4)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()
            products = CrudProducts()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],10,3)
            opc2 = menu_products.menu()
            if opc2 == "1":
                products.create()
            elif opc2 == "2":
                products.update()
            elif opc2 == "3":
                products.delete()
            elif opc2 == "4":
                products.consult()
            print("Regresando al menu Facturacion...")
            time.sleep(4) 
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],10,3)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
            elif opc3 == "3":
                pass
            elif opc3 == "4":
                sales.delete()
            print("Regresando al menu Facturacion...")
            time.sleep(4) 
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

