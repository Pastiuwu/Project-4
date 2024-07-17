import re

# ------------------------Base de datos simulada para usuarios y trabajadores------------------------

usuarios = {}
trabajadores = []
id_trabajadores = 1


#------------------------Menú inicial de crear usuario e inicio de sesión ------------------------

def main():
    while True:
        print("Seleccione una opción:")
        print("1. Crear usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        option = input("Ingrese 1, 2 o 3: ")

        if option == "1":
            crear_usuario()
        elif option == "2":
            login()
        elif option == "3":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida, intente de nuevo.")


#------------------------Validador de contraseña segura con 8 caracteres, un Mayus y un número ------------------------

def validar_contraseña(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True

#------------------------validador de Rut------------------------    

def validar_rut(rut):
    return re.match(r"^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$", rut) or re.match(r"^\d{7,8}-[\dkK]$", rut)


#------------------------Validador de número de telefono chileno------------------------

def validar_telefono(phone):
    return re.match(r"^\+569\d{8}$", phone)
    


#------------------------Función de creación de usuario------------------------
def crear_usuario():
    while True:
        username = input("Ingrese un nombre de usuario: ")
        if username in usuarios:
            print("El nombre de usuario ya existe. Intente con otro.")
            continue

        password = input("Ingrese una contraseña: ")
        if not validar_contraseña(password):
            print("La contraseña no cumple con las políticas de seguridad. Intente de nuevo.")
            continue

        confirm_password = input("Confirme la contraseña: ")
        if password != confirm_password:
            print("Las contraseñas no coinciden. Intente de nuevo.")
            continue

        usuarios[username] = password
        print("Usuario creado exitosamente.")
        break


#------------------------Función de inicio de sesión------------------------
def login():
    while True:
        username = input("Ingrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")

        if username in usuarios and usuarios[username] == password:
            print("Inicio de sesión exitoso.")
            menu_usuario(username)
            break
        else:
            print("Nombre de usuario o contraseña incorrectos.")


#------------------------Menú de opción al inciar sesión------------------------        
def menu_usuario(username):
    while True:
        print("Seleccione una opción:")
        print("1. Usuario como trabajador")
        print("2. Jefe de recursos")
        print("3. Salir")
        option = input("Ingrese 1, 2 o 3: ")

        if option == "1":
            menu_trabajador(username)
        elif option == "2":
            code = input("Ingrese el código único para jefes de recursos humanos: ")
            if code == "1234":
                menu_admin()
            else:
                print("Código incorrecto.")
        elif option == "3":
            break
        else:
            print("Opción no válida.")


#------------------------Menu de Trabajadores------------------------
def menu_trabajador(username):
    while True:
        print("\nMenú de Trabajadores:")
        print("1. Actualizar Cargas Familiares")
        print("2. Actualizar Contactos de Emergencia")
        print("3. Actualizar Datos Personales")
        print("4. Salir")
        option = input("Seleccione una opción (1-4): ")

        if option == "1":
            manage_carga_familiar(username)
        elif option == "2":
            manage_contacto_emergencias(username)
        elif option == "3":
            manage_personal_data(username)
        elif option == "4":
            break
        else:
            print("Opción no válida.")


#------------------------Menú del jefe de R.R.H.H------------------------

def menu_admin():
    while True:
        print("\nMenú de Jefe de Recursos Humanos:")
        print("1. Agregar Datos Personales")
        print("2. Agregar Datos Laborales")
        print("3. Agregar Contactos de Emergencia")
        print("4. Agregar Cargas Familiares")
        print("5. Obtener Listado de Trabajadores")
        print("6. Eliminar Trabajador")
        print("7. Salir")
        option = input("Seleccione una opción (1-7): ")

        if option == "1":
            add_datos_personales()
        elif option == "2":
            add_datos_laborales()
        elif option == "3":
            add_contacto_emergencia()
        elif option == "4":
            add_carga_familiar()
        elif option == "5":
            get_lista_trabajadores()
        elif option == "6":
            eliminar_trabajador()
        elif option == "7":
            break
        else:
            print("Opción no válida.")


#------------------------Función de agregar datos personales---------------------------

def add_datos_personales():
    global id_trabajadores
    while True:
        username = input("Ingrese el nombre de usuario asociado: ")
        if username not in usuarios:
            print("Usuario no encontrado. Intente de nuevo.")
            continue

        full_name = input("Nombre completo: ")
        rut = input("RUT (formato: xx.xxx.xxx-x o xxxxxxxx-x): ")
        if not validar_rut(rut):
            print("RUT no válido. Intente de nuevo.")
            continue
        sex = input("Sexo (M/F): ")
        address = input("Dirección: ")
        phone = input("Teléfono (formato: +569xxxxxxxx): ")
        if not validar_telefono(phone):
            print("Teléfono no válido. Intente de nuevo.")
            continue

        trabajador_id = f"{id_trabajadores:02}"
        id_trabajadores += 1
        trabajador = {
            "id": trabajador_id,
            "username": username,
            "full_name": full_name,
            "rut": rut,
            "sex": sex,
            "address": address,
            "phone": phone,
            "labor_data": {},
            "emergency_contacts": [],
            "family_loads": []
        }
        trabajadores.append(trabajador)
        print(f"Datos personales agregados exitosamente. ID de trabajador: {trabajador_id}")
        break


#------------------------Función de agregar datos laborales ------------------------

def add_datos_laborales():
    rut = input("Ingrese el RUT del trabajador: ")
    trabajador = find_trabajador_by_rut(rut)
    if not trabajador:
        print("Trabajador no encontrado.")
        return

    cargo = input("Cargo: ")
    fecha_ingreso = input("Fecha de ingreso a la compañía (ejemplo: 2023-07-01): ")
    area = input("Área: ")
    departamento = input("Departamento: ")

    trabajador["labor_data"] = {
        "cargo": cargo,
        "fecha_ingreso": fecha_ingreso,
        "area": area,
        "departamento": departamento
    }
    print("Datos laborales agregados exitosamente.")


#------------------------Función de agregar contactos de emergencia-------------------------------------------

def add_contacto_emergencia():
    rut = input("Ingrese el RUT del trabajador: ")
    trabajador = find_trabajador_by_rut(rut)
    if not trabajador:
        print("Trabajador no encontrado.")
        return

    nombre_contacto = input("Nombre del contacto: ")
    relacion = input("Relación con el trabajador: ")
    telefono_contacto = input("Teléfono del contacto (formato: +569xxxxxxxx): ")
    if not validar_telefono(telefono_contacto):
        print("Teléfono no válido. Intente de nuevo.")
        return

    contact = {
        "nombre_contacto": nombre_contacto,
        "relacion": relacion,
        "telefono_contacto": telefono_contacto
    }
    trabajador["emergency_contacts"].append(contact)
    print("Contacto de emergencia agregado exitosamente.")


#------------------------Función de agregar contactos de emergencia-------------------------------------------

def add_carga_familiar():
    rut = input("Ingrese el RUT del trabajador: ")
    trabajador = find_trabajador_by_rut(rut)
    if not trabajador:
        print("Trabajador no encontrado.")
        return

    nombre_carga = input("Nombre de la carga familiar: ")
    parentesco = input("Parentesco: ")
    sexo_carga = input("Sexo (M/F): ")
    rut_carga = input("RUT de la carga (formato: xxxxxxxx-x): ")
    if not validar_rut(rut_carga):
        print("RUT no válido. Intente de nuevo.")
        return

    carga = {
        "nombre_carga": nombre_carga,
        "parentesco": parentesco,
        "sexo_carga": sexo_carga,
        "rut_carga": rut_carga
    }
    trabajador["family_loads"].append(carga)
    print("Carga familiar agregada exitosamente.")


#------------------------Función de Listados de datos de los trabajadores ingresados en el sistema-------------------------------------------    

def get_lista_trabajadores():
    print("Filtrar listado de trabajadores por:")
    sexo = input("1. Sexo (M/F)\n2. No filtrar\nSeleccione una opción: ")
    cargo = input("1. Cargo\n2. No filtrar\nSeleccione una opción: ")
    area = input("1. Área\n2. No filtrar\nSeleccione una opción: ")
    departamento = input("1. Departamento\n2. No filtrar\nSeleccione una opción: ")

    sexo = input("Sexo (M/F) o presione Enter para no filtrar: ") if sexo == "1" else ""
    cargo = input("Cargo o presione Enter para no filtrar: ") if cargo == "1" else ""
    area = input("Área o presione Enter para no filtrar: ") if area == "1" else ""
    departamento = input("Departamento o presione Enter para no filtrar: ") if departamento == "1" else ""

    filtered_trabajadores = [
        trabajador for trabajador in trabajadores
        if (sexo == "" or trabajador["sex"] == sexo) and
           (cargo == "" or trabajador["labor_data"].get("cargo") == cargo) and
           (area == "" or trabajador["labor_data"].get("area") == area) and
           (departamento == "" or trabajador["labor_data"].get("departamento") == departamento)
    ]

    for trabajador in filtered_trabajadores:
        print("\nID de trabajador:", trabajador["id"])
        print("Nombre completo:", trabajador["full_name"])
        print("RUT:", trabajador["rut"])
        print("Sexo:", trabajador["sex"])
        print("Dirección:", trabajador["address"])
        print("Teléfono:", trabajador["phone"])
        print("Datos laborales:", trabajador["labor_data"])
        print("Contactos de emergencia:", trabajador["emergency_contacts"])
        print("Cargas familiares:", trabajador["family_loads"])


#------------------------Función de Eliminar trabajador-------------------------------------------

def eliminar_trabajador():
    trabajador_id = input("Ingrese el ID del trabajador: ")
    trabajador = find_trabajador_by_id(trabajador_id)
    if not trabajador:
        print("Trabajador no encontrado.")
        return

    code = input("Ingrese el código único para confirmar la eliminación: ")
    if code != "1234":
        print("Código incorrecto.")
        return

    trabajadores.remove(trabajador)
    print("Trabajador eliminado exitosamente.")


#------------------------Menú Actualizar datos personales-------------------------------------------

def manage_personal_data(username):
    trabajador = find_trabajador_by_username(username)
    if not trabajador:
        print("Trabajador no encontrado.")
        return

    while True:
        print("\nOpciones de Datos Personales:")
        print("1. Actualizar")
        print("2. Eliminar")
        print("3. Volver")
        option = input("Seleccione una opción (1-3): ")

        if option == "1":
            update_personal_data(trabajador)
        elif option == "2":
            clear_personal_data(trabajador)
        elif option == "3":
            break
        else:
            print("Opción no válida.")


#------------------------Menú actualizar cargas familiares-------------------------------------------

def manage_carga_familiar(username):
    trabajador = find_trabajador_by_username(username)
    if not trabajador:
        print("Trabajador no encontrado.")
        return

    while True:
        print("\nOpciones de Cargas Familiares:")
        print("1. Actualizar")
        print("2. Eliminar")
        print("3. Volver")
        option = input("Seleccione una opción (1-3): ")

        if option == "1":
            add_carga_familiar_to_trabajador(trabajador)
        elif option == "2":
            remove_carga_familiar_from_trabajador(trabajador)
        elif option == "3":
            break
        else:
            print("Opción no válida.")


#------------------------Menú de Actualizar contactos de emergencia-------------------------------------------

def manage_contacto_emergencias(username):
    trabajador = find_trabajador_by_username(username)
    if not trabajador:
        print("Trabajador no encontrado.")
        return

    while True:
        print("\nOpciones de Contactos de Emergencia:")
        print("1. Actualizar")
        print("2. Eliminar")
        print("3. Volver")
        option = input("Seleccione una opción (1-3): ")

        if option == "1":
            add_contacto_emergencia_to_trabajador(trabajador)
        elif option == "2":
            remove_contacto_emergencia_from_trabajador(trabajador)
        elif option == "3":
            break
        else:
            print("Opción no válida.")

#------------------------Función de actualizar datas personales-------------------------------------------

def update_personal_data(trabajador):
    address = input("Nueva dirección: ")
    phone = input("Nuevo teléfono (formato: +569xxxxxxxx): ")
    if not validar_telefono(phone):
        print("Teléfono no válido. Intente de nuevo.")
        return

    trabajador["address"] = address
    trabajador["phone"] = phone
    print("Datos personales actualizados exitosamente.")


#------------------------Función de Eliminar datos personales-------------------------------------------

def clear_personal_data(trabajador):
    trabajador["address"] = ""
    trabajador["phone"] = ""
    print("Datos personales eliminados exitosamente.")


#------------------------Función de actualizar carga familiar-------------------------------------------

def add_carga_familiar_to_trabajador(trabajador):
    nombre_carga = input("Nombre de la carga familiar: ")
    parentesco = input("Parentesco: ")
    sexo_carga = input("Sexo (M/F): ")
    rut_carga = input("RUT de la carga (formato: xxxxxxxx-x): ")
    if not validar_rut(rut_carga):
        print("RUT no válido. Intente de nuevo.")
        return

    carga = {
        "nombre_carga": nombre_carga,
        "parentesco": parentesco,
        "sexo_carga": sexo_carga,
        "rut_carga": rut_carga
    }
    trabajador["family_loads"].append(carga)
    print("Carga familiar agregada exitosamente.")

    #------------------------Función de Elimnar carga familiar-------------------------------------------

def remove_carga_familiar_from_trabajador(trabajador):
    nombre_carga = input("Nombre de la carga familiar a eliminar: ")
    found = False
    for carga in trabajador["family_loads"]:
        if carga["nombre_carga"] == nombre_carga:
            trabajador["family_loads"].remove(carga)
            print("Carga familiar eliminada exitosamente.")
            found = True
            break
    if not found:
        print("Carga familiar no encontrada.")


#------------------------Función de actualizar contactos de emergencia-------------------------------------------

def add_contacto_emergencia_to_trabajador(trabajador):
    nombre_contacto = input("Nombre del contacto: ")
    relacion = input("Relación con el trabajador: ")
    telefono_contacto = input("Teléfono del contacto (formato: +569xxxxxxxx): ")
    if not validar_telefono(telefono_contacto):
        print("Teléfono no válido. Intente de nuevo.")
        return

    contact = {
        "nombre_contacto": nombre_contacto,
        "relacion": relacion,
        "telefono_contacto": telefono_contacto
    }
    trabajador["emergency_contacts"].append(contact)
    print("Contacto de emergencia agregado exitosamente.")


#------------------------Función de Eliminar contactos de emergencia-------------------------------------------

def remove_contacto_emergencia_from_trabajador(trabajador):
    nombre_contacto = input("Nombre del contacto de emergencia a eliminar: ")
    found = False
    for contact in trabajador["emergency_contacts"]:
        if contact["nombre_contacto"] == nombre_contacto:
            trabajador["emergency_contacts"].remove(contact)
            print("Contacto de emergencia eliminado exitosamente.")
            found = True
            break
    if not found:
        print("Contacto de emergencia no encontrado.")


#------------------Estas funciones sirven para buscar y recuperar información sobre los trabajadores almacenados en la lista 'trabajadores'-------------- 

def find_trabajador_by_username(username):
    for trabajador in trabajadores:
        if trabajador.get("username") == username:
            return trabajador
    return None

def find_trabajador_by_rut(rut):
    for trabajador in trabajadores:
        if trabajador["rut"] == rut:
            return trabajador
    return None

def find_trabajador_by_id(trabajador_id):
    for trabajador in trabajadores:
        if trabajador["id"] == trabajador_id:
            return trabajador
    return None

if __name__ == "__main__":
    main()
