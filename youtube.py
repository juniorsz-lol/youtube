import mysql.connector

# Conexión a la base de datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            database="youtube_simulacion",
            user="root",
            password=""
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error conectando a la base de datos: {err}")
        return None

# Función para añadir un video
def añadir_video():
    conexion = conectar_db()
    cursor = conexion.cursor()

    titulo = input("Introduce el título del video: ")
    duracion = input("Introduce la duración del video (HH:MM:SS): ")
    creador = input("Introduce el nombre del creador: ")
    categoria = input("Introduce la categoría del video (opcional, presiona Enter para omitir): ")

    # Si categoría está vacía, asignamos None
    if not categoria:
        categoria = None

    cursor.execute(
        "INSERT INTO Videos (titulo, duracion, creador, categoria) VALUES (%s, %s, %s, %s)",
        (titulo, duracion, creador, categoria)
    )
    conexion.commit()
    print(f"¡Video '{titulo}' añadido exitosamente!")

    cursor.close()
    conexion.close()

# Función para listar videos
def listar_videos():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Videos")
    videos = cursor.fetchall()

    if videos:
        print("Lista de videos disponibles:")
        for video in videos:
            print(f"ID: {video[0]}, Título: {video[1]}, Duración: {video[2]}, Creador: {video[3]}, Categoría: {video[4]}")
    else:
        print("No hay videos disponibles.")

    cursor.close()
    conexion.close()

# Función para editar un video
def editar_video():
    conexion = conectar_db()
    cursor = conexion.cursor()

    listar_videos()
    video_id = input("Introduce el ID del video que deseas editar: ")

    nuevo_titulo = input("Introduce el nuevo título (deja vacío para mantener actual): ")
    nueva_duracion = input("Introduce la nueva duración (HH:MM:SS, deja vacío para mantener actual): ")
    nuevo_creador = input("Introduce el nuevo creador (deja vacío para mantener actual): ")
    nueva_categoria = input("Introduce la nueva categoría (deja vacío para mantener actual): ")

    query = "UPDATE Videos SET"
    valores = []
    if nuevo_titulo:
        query += " titulo = %s,"
        valores.append(nuevo_titulo)
    if nueva_duracion:
        query += " duracion = %s,"
        valores.append(nueva_duracion)
    if nuevo_creador:
        query += " creador = %s,"
        valores.append(nuevo_creador)
    if nueva_categoria:
        query += " categoria = %s,"
        valores.append(nueva_categoria)

    query = query.rstrip(",") + " WHERE id = %s"
    valores.append(video_id)

    cursor.execute(query, tuple(valores))
    conexion.commit()
    print("¡Video actualizado exitosamente!")

    cursor.close()
    conexion.close()

# Función para eliminar un video
def eliminar_video():
    conexion = conectar_db()
    cursor = conexion.cursor()

    listar_videos()
    video_id = input("Introduce el ID del video que deseas eliminar: ")

    cursor.execute("DELETE FROM Videos WHERE id = %s", (video_id,))
    conexion.commit()
    print("¡Video eliminado exitosamente!")

    cursor.close()
    conexion.close()

# Menú del administrador
def menu_principal():
    while True:
        print("\n===== youtube =====")
        print("1. Añadir video")
        print("2. Ver videos")
        print("3. Editar video")
        print("4. Eliminar video")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            añadir_video()
        elif opcion == "2":
            listar_videos()
        elif opcion == "3":
            editar_video()
        elif opcion == "4":
            eliminar_video()
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()
