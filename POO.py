import re

class User:
    users = {}

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def create_user(cls):
        while True:
            username = input("Ingrese un nombre de usuario: ")
            if username in cls.users:
                print("El nombre de usuario ya existe. Intente con otro.")
                continue

            password = input("Ingrese una contraseña: ")
            if not cls.is_valid_password(password):
                print("La contraseña no cumple con las políticas de seguridad. Intente de nuevo.")
                continue

            confirm_password = input("Confirme la contraseña: ")
            if password != confirm_password:
                print("Las contraseñas no coinciden. Intente de nuevo.")
                continue

            cls.users[username] = User(username, password)
            print("Usuario creado exitosamente.")
            break

    @classmethod
    def is_valid_password(cls, password):
        if len(password) < 8:
            return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
        return True

    @classmethod
    def login(cls):
        while True:
            username = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")

            user = cls.users.get(username)
            if user and user.password == password:
                print("Inicio de sesión exitoso.")
                return user
            else:
                print("Nombre de usuario o contraseña incorrectos.")

class Worker:
    workers = []
    worker_id_counter = 1

    def __init__(self, username, full_name, rut, sex, address, phone):
        self.id = f"{Worker.worker_id_counter:02}"
        Worker.worker_id_counter += 1
        self.username = username
        self.full_name = full_name
        self.rut = rut
        self.sex = sex
        self.address = address
        self.phone = phone
        self.labor_data = {}
        self.emergency_contacts = []
        self.family_loads = []

    @classmethod
    def add_personal_data(cls):
        while True:
            username = input("Ingrese el nombre de usuario asociado: ")
            if username not in User.users:
                print("Usuario no encontrado. Intente de nuevo.")
                continue

            full_name = input("Nombre completo: ")
            rut = input("RUT (formato: xx.xxx.xxx-x o xxxxxxxx-x): ")
            if not cls.is_valid_rut(rut):
                print("RUT no válido. Intente de nuevo.")
                continue
            sex = input("Sexo (M/F): ")
            address = input("Dirección: ")
            phone = input("Teléfono (formato: +569xxxxxxxx): ")
            if not cls.is_valid_phone(phone):
                print("Teléfono no válido. Intente de nuevo.")
                continue

            worker = Worker(username, full_name, rut, sex, address, phone)
            cls.workers.append(worker)
            print(f"Datos personales agregados exitosamente. ID de trabajador: {worker.id}")
            break

    @staticmethod
    def is_valid_rut(rut):
        return re.match(r"^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$", rut) or re.match(r"^\d{7,8}-[\dkK]$", rut)

    @staticmethod
    def is_valid_phone(phone):
        return re.match(r"^\+569\d{8}$", phone)

    @classmethod
    def add_labor_data(cls):
        rut = input("Ingrese el RUT del trabajador: ")
        worker = cls.find_worker_by_rut(rut)
        if not worker:
            print("Trabajador no encontrado.")
            return

        cargo = input("Cargo: ")
        fecha_ingreso = input("Fecha de ingreso a la compañía (ejemplo: 2023-07-01): ")
        area = input("Área: ")
        departamento = input("Departamento: ")

        worker.labor_data = {
            "cargo": cargo,
            "fecha_ingreso": fecha_ingreso,
            "area": area,
            "departamento": departamento
        }
        print("Datos laborales agregados exitosamente.")

    @classmethod
    def add_emergency_contact(cls):
        rut = input("Ingrese el RUT del trabajador: ")
        worker = cls.find_worker_by_rut(rut)
        if not worker:
            print("Trabajador no encontrado.")
            return

        nombre_contacto = input("Nombre del contacto: ")
        relacion = input("Relación con el trabajador: ")
        telefono_contacto = input("Teléfono del contacto (formato: +569xxxxxxxx): ")
        if not cls.is_valid_phone(telefono_contacto):
            print("Teléfono no válido. Intente de nuevo.")
            return

        contact = {
            "nombre_contacto": nombre_contacto,
            "relacion": relacion,
            "telefono_contacto": telefono_contacto
        }
        worker.emergency_contacts.append(contact)
        print("Contacto de emergencia agregado exitosamente.")

    @classmethod
    def add_family_load(cls):
        rut = input("Ingrese el RUT del trabajador: ")
        worker = cls.find_worker_by_rut(rut)
        if not worker:
            print("Trabajador no encontrado.")
            return

        nombre_carga = input("Nombre de la carga familiar: ")
        parentesco = input("Parentesco: ")
        sexo_carga = input("Sexo (M/F): ")
        rut_carga = input("RUT de la carga (formato: xx.xxx.xxx-x o xxxxxxxx-x): ")
        if not cls.is_valid_rut(rut_carga):
            print("RUT no válido. Intente de nuevo.")
            return

        carga = {
            "nombre_carga": nombre_carga,
            "parentesco": parentesco,
            "sexo_carga": sexo_carga,
            "rut_carga": rut_carga
        }
        worker.family_loads.append(carga)
        print("Carga familiar agregada exitosamente.")

    @classmethod
    def get_worker_list(cls):
        print("Filtrar listado de trabajadores por:")
        sexo = input("1. Sexo (M/F)\n2. No filtrar\nSeleccione una opción: ")
        cargo = input("1. Cargo\n2. No filtrar\nSeleccione una opción: ")
        area = input("1. Área\n2. No filtrar\nSeleccione una opción: ")
        departamento = input("1. Departamento\n2. No filtrar\nSeleccione una opción: ")

        sexo = input("Sexo (M/F) o presione Enter para no filtrar: ") if sexo == "1" else ""
        cargo = input("Cargo o presione Enter para no filtrar: ") if cargo == "1" else ""
        area = input("Área o presione Enter para no filtrar: ") if area == "1" else ""
        departamento = input("Departamento o presione Enter para no filtrar: ") if departamento == "1" else ""

        filtered_workers = [
            worker for worker in cls.workers
            if (sexo == "" or worker.sex == sexo) and
               (cargo == "" or worker.labor_data.get("cargo") == cargo) and
               (area == "" or worker.labor_data.get("area") == area) and
               (departamento == "" or worker.labor_data.get("departamento") == departamento)
        ]

        for worker in filtered_workers:
            print("\nID de trabajador:", worker.id)
            print("Nombre completo:", worker.full_name)
            print("RUT:", worker.rut)
            print("Sexo:", worker.sex)
            print("Dirección:", worker.address)
            print("Teléfono:", worker.phone)
            print("Datos laborales:", worker.labor_data)
            print("Contactos de emergencia:", worker.emergency_contacts)
            print("Cargas familiares:", worker.family_loads)

    @classmethod
    def delete_worker(cls):
        worker_id = input("Ingrese el ID del trabajador: ")
        worker = cls.find_worker_by_id(worker_id)
        if not worker:
            print("Trabajador no encontrado.")
            return

        code = input("Ingrese el código único para confirmar la eliminación: ")
        if code != "1234":
            print("Código incorrecto.")
            return

        cls.workers.remove(worker)
        print("Trabajador eliminado exitosamente.")

    @classmethod
    def find_worker_by_username(cls, username):
        for worker in cls.workers:
            if worker.username == username:
                return worker
        return None

    @classmethod
    def find_worker_by_rut(cls, rut):
        for worker in cls.workers:
            if worker.rut == rut:
                return worker
        return None

    @classmethod
    def find_worker_by_id(cls, worker_id):
        for worker in cls.workers:
            if worker.id == worker_id:
                return worker
        return None

class Menu:
    @staticmethod
    def main():
        while True:
            print("Seleccione una opción:")
            print("1. Crear usuario")
            print("2. Iniciar sesión")
            print("3. Salir")
            option = input("Ingrese 1, 2 o 3: ")

            if option == "1":
                User.create_user()
            elif option == "2":
                user = User.login()
                if user:
                    Menu.user_menu(user)
            elif option == "3":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    @staticmethod
    def user_menu(user):
        while True:
            print("\nSeleccione una opción:")
            print("1. Trabajador")
            print("2. Administrador")
            print("3. Cerrar sesión")
            option = input("Ingrese 1, 2 o 3: ")

            if option == "1":
                Menu.worker_menu(user)
            elif option == "2":
                code = input("Ingrese el código único de administrador: ")
                if code == "1234":
                    Menu.admin_menu()
                else:
                    print("Código incorrecto.")
            elif option == "3":
                print("Cerrando sesión...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    @staticmethod
    def admin_menu():
        while True:
            print("\nMenú de Administrador:")
            print("1. Agregar datos personales del trabajador")
            print("2. Agregar datos laborales del trabajador")
            print("3. Agregar contacto de emergencia del trabajador")
            print("4. Agregar carga familiar del trabajador")
            print("5. Obtener listado de trabajadores")
            print("6. Eliminar trabajador")
            print("7. Cerrar sesión de administrador")
            option = input("Ingrese una opción: ")

            if option == "1":
                Worker.add_personal_data()
            elif option == "2":
                Worker.add_labor_data()
            elif option == "3":
                Worker.add_emergency_contact()
            elif option == "4":
                Worker.add_family_load()
            elif option == "5":
                Worker.get_worker_list()
            elif option == "6":
                Worker.delete_worker()
            elif option == "7":
                print("Cerrando sesión de administrador...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    @staticmethod
    def worker_menu(user):
        worker = Worker.find_worker_by_username(user.username)
        if not worker:
            print("Trabajador no encontrado.")
            return

        while True:
            print("\nMenú de Trabajador:")
            print("1. Actualizar datos personales")
            print("2. Agregar o eliminar contacto de emergencia")
            print("3. Agregar o eliminar carga familiar")
            print("4. Cerrar sesión de trabajador")
            option = input("Ingrese una opción: ")

            if option == "1":
                # Actualizar datos personales
                worker.address = input("Nueva dirección: ")
                phone = input("Nuevo teléfono (formato: +569xxxxxxxx): ")
                if Worker.is_valid_phone(phone):
                    worker.phone = phone
                else:
                    print("Teléfono no válido. Intente de nuevo.")
            elif option == "2":
                # Agregar o eliminar contacto de emergencia
                contact_option = input("1. Agregar contacto\n2. Eliminar contacto\nIngrese una opción: ")
                if contact_option == "1":
                    Worker.add_emergency_contact()
                elif contact_option == "2":
                    contact_name = input("Nombre del contacto a eliminar: ")
                    worker.emergency_contacts = [contact for contact in worker.emergency_contacts if contact["nombre_contacto"] != contact_name]
                    print("Contacto eliminado exitosamente.")
            elif option == "3":
                # Agregar o eliminar carga familiar
                carga_option = input("1. Agregar carga familiar\n2. Eliminar carga familiar\nIngrese una opción: ")
                if carga_option == "1":
                    Worker.add_family_load()
                elif carga_option == "2":
                    carga_name = input("Nombre de la carga familiar a eliminar: ")
                    worker.family_loads = [carga for carga in worker.family_loads if carga["nombre_carga"] != carga_name]
                    print("Carga familiar eliminada exitosamente.")
            elif option == "4":
                print("Cerrando sesión de trabajador...")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

# Iniciar el menú principal
Menu.main()
