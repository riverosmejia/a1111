from usuario import Usuario
from imprimir import Imprimir

class Sistema:

    def __init__(self):
        self.lista_usuarios = []
        self.lista_grupos_obj = []
        self.imprimir = Imprimir()
        self.archivo_usuarios = "usuarios.txt"
        self.archivo_grupos = "grupos.txt"
        self.usuario_actual = None
        self.leer_usuarios_desde_archivo(self.archivo_usuarios)
        self.leer_grupos_desde_archivo(self.archivo_grupos)

    def obtener_grupo_por_nombre(self, lista_grupos, nombre_grupo):
        for grupo in lista_grupos:
            if grupo == nombre_grupo:
                return grupo

        return None

    def retirarse_de_grupo(self, usuario_actual, lista_grupos, nombre_grupo):
        grupo_obj = self.obtener_grupo_por_nombre(lista_grupos, nombre_grupo)

        if grupo_obj is not None:
            if nombre_grupo in usuario_actual.Grupos:
                usuario_actual.Grupos.remove(nombre_grupo)
                print(f"Te has retirado del grupo: {nombre_grupo}.")
                self.guardar_lista_usuarios()
            else:
                print("No puedes retirarte de un grupo al que no perteneces.")
        else:
            print("El grupo especificado no existe.")

    def guardar_grupos_en_archivo(self):

        with open(self.archivo_grupos, "w") as archivo:
            for grupo in self.lista_grupos:
                archivo.write(f"{grupo.nombre}\n")

    def leer_grupos_desde_archivo(self, nombre_archivo):
       
        try:
            with open(nombre_archivo, "r") as archivo:
                lineas = archivo.readlines()
                self.lista_grupos_obj = [Grupo(linea.strip()) for linea in lineas]
        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no existe.")
        except Exception as e:
            print(f"Error al leer la lista de grupos desde el archivo: {e}")

    def agregar_usuario(self, usuario):

        self.lista_usuarios.append(usuario)

    def guardar_en_archivo(self, usuario, nombre_archivo):

        with open(nombre_archivo, "a") as archivo:
            archivo.write(usuario.obtener_info() + "\n")

    def guardar_lista_usuarios(self):

        print("Guardando lista de usuarios...")
        with open(self.archivo_usuarios, "r") as archivo:
            lineas = archivo.readlines()

        with open(self.archivo_usuarios, "w") as archivo:
            for i, linea in enumerate(lineas):
                if f"Nombre: {self.usuario_actual.nombre}" in linea and f"Contraseña: {self.usuario_actual.contraseña}" in linea:
                    print(f"Borrando línea para {self.usuario_actual.nombre}")
                    continue  # No escribir la línea existente del usuario actual

                archivo.write(linea)

            # Agregar el usuario actual al final del archivo
            archivo.write(self.usuario_actual.obtener_info() + "\n")

        print("Lista de usuarios guardada correctamente.")

    def leer_usuarios_desde_archivo(self, nombre_archivo):

        usuarios = []

        try:
            with open(nombre_archivo, "r") as archivo:
                lineas = archivo.readlines()

                for linea in lineas:
                    nombre_inicio = linea.find("Nombre:")
                    contrasena_inicio = linea.find("Contraseña:")
                    monto_inicio = linea.find("Monto:")
                    grupos_inicio = linea.find("Grupos:")

                    if (
                        nombre_inicio != -1
                        and contrasena_inicio != -1
                        and monto_inicio != -1
                        and grupos_inicio != -1
                    ):
                        nombre = linea[nombre_inicio + len("Nombre:"):contrasena_inicio].strip()
                        contrasena = linea[contrasena_inicio + len("Contraseña:"):monto_inicio].strip()
                        monto_str = linea[monto_inicio + len("Monto:"):grupos_inicio].strip()
                        grupos_str = linea[grupos_inicio + len("Grupos:"):].strip()

                        try:
                            monto = int(monto_str)
                        except ValueError:
                            print(f"Error al convertir monto a entero en la línea: {linea}")
                            continue

                        grupos = [grupo.strip() for grupo in grupos_str.split(',')]
                        usuarios.append(Usuario(nombre, contrasena, monto, grupos))

        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no existe.")
        except Exception as e:
            print(f"Error al leer usuarios desde el archivo: {e}")

        return usuarios

    def leer_grupos_desde_archivo(self, nombre_archivo):
        try:
            with open(nombre_archivo, "r") as archivo:
                lineas = archivo.readlines()
                self.lista_grupos = [linea.strip() for linea in lineas]
        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no existe.")
        except Exception as e:
            print(f"Error al leer la lista de grupos desde el archivo: {e}")

    def guardar_grupos_en_archivo(self):
        with open(self.archivo_grupos, "w") as archivo:
            for grupo in self.lista_grupos:
                archivo.write(f"{grupo}\n")

    def iniciar_sesion(self):
        nombre = input("Ingrese su nombre: ")
        contrasena = input("Ingrese su contraseña: ")
        usuarios = self.leer_usuarios_desde_archivo(self.archivo_usuarios)

        print('<<------------------------>>')

        for usuario_actual in usuarios:
            if usuario_actual.nombre == nombre and usuario_actual.contraseña == contrasena:
                print(f"Inicio de sesión exitoso. Hola, {nombre}!")
                self.usuario_actual = usuario_actual  # Actualizar la instancia del usuario actual
                return

        print("Inicio de sesión fallido. Verifique sus credenciales.")
        print('<<------------------------>>')

    def cerrar_sesion(self):
        self.usuario_actual = None
        print("Sesión cerrada.")

    def unirse_a_grupo(self):
        if self.usuario_actual is not None:
            # Verificar si el usuario ya pertenece al máximo de grupos permitidos
            if len(self.usuario_actual.Grupos) >= 3:
                print("Ya perteneces al máximo de grupos permitidos (3).")
                return

            nombre_grupo = input("Ingrese el nombre del grupo al que desea unirse: ")

            # Verificar si el grupo existe en la lista de grupos
            grupo_obj = self.obtener_grupo_por_nombre(nombre_grupo)
            if grupo_obj is not None:
                # Verificar si el grupo ya tiene el máximo de usuarios permitidos (3)
                if len(grupo_obj.usuarios) >= 3:
                    print(f"El grupo {nombre_grupo} ya tiene el máximo de usuarios permitidos (3).")
                else:
                    # Verificar si el usuario ya pertenece al grupo
                    if nombre_grupo not in self.usuario_actual.Grupos:
                        grupo_obj.usuarios.append(self.usuario_actual)
                        self.usuario_actual.Grupos.append(nombre_grupo)
                        print(f"Te has unido al grupo: {nombre_grupo}.")
                        self.guardar_lista_usuarios()
                        self.guardar_grupos_en_archivo()
                    else:
                        print(f"Ya perteneces al grupo {nombre_grupo}.")
            else:
                print(f"El grupo {nombre_grupo} no existe.")
        else:
            print("Debes iniciar sesión para unirte a un grupo.")

    def crear_grupo(self):
        if self.usuario_actual is not None:
            nombre_grupo = input("Ingrese el nombre del nuevo grupo: ")

            # Verificar que el grupo no exista
            if nombre_grupo not in self.lista_grupos:
                saldo_inicial = int(input("Ingrese el saldo inicial del grupo: "))
                
                # Agregar el nuevo grupo con su saldo al archivo de grupos
                with open(self.archivo_grupos, "a") as archivo:
                    archivo.write(f"{nombre_grupo}:{saldo_inicial}\n")

                # Actualizar la lista de grupos en memoria
                self.lista_grupos.append(nombre_grupo)

                # Agregar el nuevo grupo a la lista de grupos del usuario actual
                self.usuario_actual.Grupos.append(nombre_grupo)

                print(f"Se ha creado y te has unido al grupo {nombre_grupo} con un saldo inicial de {saldo_inicial}.")
                self.guardar_lista_usuarios()
            else:
                print("Ya existe un grupo con ese nombre.")
        else:
            print("Debes iniciar sesión para crear un grupo.")

    def arrancamos(self):

        print(self.lista_usuarios)

        salir = False

        while not salir:
            valido = False

            print(self.usuario_actual)
            if self.usuario_actual is not None:
                print(self.usuario_actual.Grupos)

            while not valido:
                self.imprimir.menu()

                resp = int(input('R/= '))

                if 0 < resp <= 12:
                    valido = True
                else:
                    print('<------- Respuesta inválida, por favor intente de nuevo -------->')

            if resp == 1:
                self.iniciar_sesion()

            if resp == 2:
                self.cerrar_sesion()

            if resp == 3:
                nombre = input("Ingrese su nombre: ")
                monto = 0
                try:
                    monto = int(input("Ingrese su Monto: "))
                except ValueError:
                    print("El monto debe ser un número entero.")
                    continue

                contrasena = input("Ingrese su contraseña: ")

                nuevo_usuario = Usuario(nombre, contrasena, monto)
                self.guardar_en_archivo(nuevo_usuario, self.archivo_usuarios)

            if resp==4:

                print(self.usuario_actual)

                self.unirse_a_grupo()

            if resp==5:

                self.crear_grupo()

            if resp == 6:

                
                # Opción para retirarse de un grupo
                if self.usuario_actual is not None and self.usuario_actual.Grupos:
                    nombre_grupo = input("Ingrese el nombre del grupo del que desea retirarse: ")
                    self.retirarse_de_grupo(self.usuario_actual, self.lista_grupos, nombre_grupo)
                else:
                    print("No puedes retirarte de un grupo si no estás en ninguno.")