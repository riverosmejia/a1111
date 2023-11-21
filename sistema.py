from usuario import Usuario
from imprimir import Imprimir

class Sistema:

    def __init__(self):
        self.lista_usuarios = []
        self.imprimir = Imprimir()
        self.archivo_usuarios = "usuarios.txt"
        self.archivo_grupos = "grupos.txt"
        self.usuario_actual = None
        self.leer_usuarios_desde_archivo(self.archivo_usuarios)
        self.leer_grupos_desde_archivo(self.archivo_grupos)

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

            if len(self.usuario_actual.Grupos) >= 3:

                print("Ya te has unido al máximo de grupos permitidos.")
                return

            nombre_grupo = input("Ingrese el nombre del grupo al que desea unirse: ")

            if nombre_grupo in self.lista_grupos and nombre_grupo not in self.usuario_actual.Grupos:

                print(nombre_grupo)

                print(self.usuario_actual.Grupos)

                print(self.usuario_actual)

                self.usuario_actual.Grupos.append(nombre_grupo)

                print(self.usuario_actual.Grupos)

                print(self.usuario_actual)

                print(f"Te has unido al grupo: {nombre_grupo}.")

                print(self.usuario_actual)

                self.guardar_lista_usuarios()
            else:
                print("El grupo ingresado no existe.")
        else:
            print("Debes iniciar sesión para unirte a un grupo.")

    def crear_grupo(self):
        if self.usuario_actual is not None:
            if len(self.usuario_actual.Grupos) >= 3:
                print("Ya has alcanzado el límite de grupos que puedes crear.")
                return

            nombre_grupo = input("Ingrese el nombre del nuevo grupo: ")
            if nombre_grupo not in self.lista_grupos:
                self.lista_grupos.append(nombre_grupo)
                self.usuario_actual.Grupos.append(nombre_grupo)
                print(f"Se ha creado y te has unido al grupo {nombre_grupo}.")
                self.guardar_lista_usuarios()
                self.guardar_grupos_en_archivo()
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