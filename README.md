# Protocolo de transmisión de peticiones entre cliente y servidor
El proyecto en este repositorio es un protocolo de comunicación entre cliente y servidor que pretende imitar de manera muy básica el funcionamiento de plataformas como Steam o servicios de cuentas de videojuegos como los de Ubisoft, EA, etc.
El programa solo funciona como protocolo de transmisión y no está ligado a una base de datos por lo que solo se administra la comunicación entre cliente y servidor y no el procesamiento de los datos necesarios para la base de datos en un caso real.

## Códigos de respuestas
El programa le permite al usuario ejecutar siete operaciones distinas, estas son:
- Inicio de sesión.
- Cerrar sesión.
- Crear usuario.
- Editar nombre de usuario.
- Editar contraseña.
- Comprar un juego.
- Ver la lista de juegos disponibles en el perfil del usuario (juegos comprados).

Para procesar estas peticiones el cliente y el servidor se comunican con códigos de estado que les permiten saber qué petición busca hacer el usuario y actuar acorde a ello.

### Estados del cliente
| Código | Descripción                |
| :-------- | :------------------------- |
| `LOGIN` | Indica que el usuario quiere iniciar sesión. |
| `NEW_USR` | Petición para crear un nuevo usuario. |
| `GAMES_LIST` | Petición para obetener lista de juegos disponibles. Se llama cuando el usuario quiere comprar un juego. |
| `GAME_SELECTION` | Le indica al servidor que el usuario ha escogido qué juego comprará. |
| `USER_GAMES_LIST` | Petición para obtener la lista de juegos adquiridos por el usuario. |
| `EDIT_PASSWORD` | Indica que el usuario quiere modificar su contraseña. |
| `EDIT_USERNAME` | Indica que el usuario quiere modificar su nombre de usuario. |
| `LOGOUT` | Indica que el usuario quiere cerrar sesión. |

### Respuestas del servidor
| Código | Descripción                |
| :-------- | :------------------------- |
| `LOGIN_RES` | Respuesta a la petición de inicio de sesión. |
| `NEW_USR_RES` | Respuesta a la petición para crear un nuevo usuario. |
| `GAMES_LIST_RES` | Respuesta para la petición del catálogo del servicio. |
| `NEW_GAME_RES` | Respuesta al usuario después de que la compra se procesó en el servidor. |
| `USER_GAMES_LIST_RES` | Respuesta con la lista de juegos adquiridos por el usuario. |
| `EDIT_PASSWORD_RES` | Respuesta con el resultado de la petición para modificar contraseña. |
| `EDIT_USERNAME_RES` | Respuesta con el resultado de la petición para modificar nombre de usuario. |
| `LOGOUT_RES` | Respuesta después del cierre de sesión. |
