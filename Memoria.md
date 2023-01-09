# Memoria

## Indice


### 1. Propuesta general de diseño
 Propuesta de una interfaz sencilla estilo *stackoverflow* pero con comentarios de estilo *reddit* en varios niveles según quien responde a quien. 
 
 El sistema de votación puede ser estilo *reddit* o *stackoverflow* indistintamente, con enfoque en los puntos para el orden y como forma de recompensar al usuario, de esta forma como los comentarios mas votados aparecen primero no será necesario que el usuario se tenga que leer todo.

 Un esquema simple de como aparecerán los comentarios a una pregunta:
- Pregunta
  - Respuesta 1 
  - Respuesta 2 
    - Comentario a la respuesta 2 (👍)
  - Respuesta 3
    - Comentario a la respuesta 2 (👎)
  
#### 1.1 Diseño de las preguntas
Las preguntas podrían ser simples o se puede contemplar la opcion de agregar imágenes o texto enriquecido, se valorara segun complejidad durante el desarrollo del proyecto.

#### 1.2 Tipos de usuarios
En cuanto al la estructura de páginas podremos diferenciar entre las páginas para usuarios logeados y las de usuarios anonimos, a pesar que dentro de los logueados puedan existir distintos roles, los dos grandes grupos son los anteriormente mencionados.

Un usuario no logueado:
- Podrá ver las preguntas que hacen otros usuarios
- Al hacer clic en una pregunta podrá ver las respuestas a esta
- Se le dará la posibilidad de crearse una cuenta o iniciar sesión
- No se le permitirá hacer nuevas preguntas o responderlas
- No podrá votar las pregidénticountas/respuestas
- No podrá reportar preguntas/respuestas

Un usuario logueado podrá realizar las actividades propias de su rol.

Por lo tanto se podrá acceder a la pagina raiz o "inicio" sin estar logueado para tener una visión general de la aplicación o a una pregunta en concreto, pero para hacer cualquier otra accion se tendrá que estar logueado. El funciónamiento será idéntico al de *StackOverflow*, de esta forma no será necesario trabajar demasíado en la UX.

#### 1.3 funciónes de los usuarios

Dentro de los usuarios existen distintos roles:
- Discusión: Es el usuario standard, puede crear y responder preguntas.
- Moderador: Se encarga de atender los reportes sobre las preguntas y los comentarios.
- Administrador: Es un rol especial que solo lo tendrá el primer usuario creado "admin"

Un usuario Moderador no podrá publicar preguntas/respuestas y un Discusión no podrá moderar.

#### 1.4 Elementos prinresolucióncipales

La base de las aplicación son las preguntas con respuestas a modo de resolución y comentarios a la respuestas valorándolas, segun si son útiles o no. La dinámica  es extremadamente parecida a la de *StackOverflow*.

- Pregunta (El usuario plantea un problema):
  - Tiene un título y un cuerpo
  - Puede ser votada (Positivo o Negativo)
  - Tiene un Autor
  - Tiene una fecha de cración
- Respuestas (Los usuarios proponen soluciones):
  - Solo tienen cuerpo
  - Pueden ser votadas (Positivo o Negativo)
  - Tienen un autor
  - Siempre tienen una única pregunta asociada
  - Tienen una fecha de cración
  - Otros usuarios con rol "Discusión" podrán valorar mediante comentarios si es útil o no.habría
- Comentario (Valoración de una respuesta)
  - Solo tienen cuerpo y una mayor restricción de longitud
  - Tienen asociado una valoracion sobre la respuesta *positiva, negativa o neutra*
  - Se mostrará la fecha de cración y su autor
  - tendrán un tamñano mas reducido en pantalla
  - Se sombrearán según la valoracion
  - Podrán ser votados para resaltar los mas útiles


### 2. Consideraciones de para el desarrollo
#### 2.1. Docker
Por su simplicidad se han decidido modificar los ficheros de instalación e inicio y así permitir el desarrollo sin necesidad de reinicios.
Se ha asumido que los desarrolladores actuales han instalado las imágenes, por lo que se ha comentado las líneas de *"/practica-dms-2022-2023/components/dms2223auth/bin/dms2223auth-create-admin"* para que no se intente volver a crear el usuario admin.
Si se requiriese reinstalar la maquina habría que descomentarlas o no será posible loguearse en la aplicación.

Además para permitir la compatibilidad con WSL2 se ha editado *" practica-dms-2022-2023/docker/config/dev.yml" liena 33* para enlazar el puerto 8080 de Docker con el 8080 de Windows.

#### 2.2. Modo debug
Para agilizar el desarrollo se ha configurado Jinja/Flask para actualizarsa cada vez que se produce un cambio en el frontend, así no será necesario reiniciar el servicio o la maquina docker cada vez que haga un cambio a la web. 
Para ello se ha modificado:

- *practica-dms-2022-2023/components/dms2223frontend/install.sh*: Se ha comentado la eliminacion del directorio temporal, es posible que requiera ser descomentado para nuevas instalacións.
- *practica-dms-2022-2023/components/dms2223frontend/bin/dms2223frontend*: Se ha añadido:
```
app.config["TESTING"] = True
app.testing=True
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)
```
Esto permite la recarga automatica de templates y codigo de las peticiones del mismo archivo. 
Es recomendable eliminar estas líneas en un futuro despliegue.

#### 2.3. Datos de prueba
Tanto para el servicio de autenticación como para el de backend se ha creado un archivo python que genera unos datos base para pribar la palicacion.

- En *components/dms2223auth/bin* está *dms2223auth-create-admin* que crea un usuario con todos los roles, se debe comentar despues de la primera ejecución, sino provoca una excepción indicando que el usuario ya existe.
- En *components/dms2223backend/bin* está *dms2223backend-crear-ejemplo* donde se resetea la base de datos y se introducen unos datos base, en este caso cuando se despliegue habrá que eliminar su llamada de *install.sh*. 

### 3. Arquitectura de la aplicación
#### 3.1. Arquitectura del frontend
  El *frontend* se encarga por una parte de mostrar las los datos al usuario y
por otro hace solicitudes a servidores de datos mediante sus *API REST*. En nuestro caso hacemos uso de 2 de estos servicios, el de *autenticación* que gestiona usuarios y roles y el de *backend* que gestiona los datos generales de la aplicación.

Para llevar a cabo estos procesos se usan 2 capas:
  - **Capa de presentacion**: Englobaría los endpoints y sus templates asociadas, únicamente muestran informacion por el navegador y solo tiene conocimiento de la actividad del usuario, a que partes entra o donde hace clic.
  - **Capa de servicios (Origen de datos)**:  Se encarga de las comunicaciones con las APIs. Recibe peticiones de la capa de presentacion para obtener datos, tiene el conocimiento de los servicios externos que se usan. En general contruya las peticiones HTTP y comprueba las respuestas.

De esta forma se pueden añadir servicios para APIs nuevas en futuras aplicaciones sin tener que modificar los actuales, pero pudiendo hacer uso de ellos (Se respeta el principio Open/Close). Además queda separada la responsabilidad del acceso a datos de la de mostrarlos (Principio Single Responsibility)

![Diagrama del frontend](/imagenes/frontend.png "Diagrama frontend")

#### 3.2 Arquitectura del backend
El backend es responsable de la gestión de todos los datos y de su presentación a consumidores externos.

Dada la complejidad del backend, que no es excesiva, se ha decidido usar una arquitectura de 3 capas. Aunque en un principio se barajó usar 4 se llegó a la conclusión que la capa de logica y servicios se podian unir ya que no habia ninguna razón que justificase tener una capa dedicada únicamente a lógica.

Las capas son:

- **Datos**: En esta capa se realizan las consultas a la base de datos a través del ORM (SQLAlchemy), esta capa por lo tanto tiene conocimiento de la estructura de la BDD y de las clases del ORM, por eso esta capa recoge clases que contienen funciónes cuyos parámetros son clases del orm, al igual que los resultados que devuelve. Se garantiza la responsabilidad única mediante funciónes para cada consulta y se aplica el principio de sustitución de Liskov donde el polimorfismo lo permite, por ejemplo, en el caso de los elementos donde para ocultarlos lo podemos hacer con la misma función siempre que el objeto introducido sea una instancia de una clase hija de elemento.
- **Servicios (Logica)**: La capa de lógica por conveniencia se ha llamado de "servicios", donde cada uno tiene conocimento de un ámbito del backend. Esta capa hace de intermediario entre *Presentacion* y *Datos*, recibe diccionarios de datos, se comunica con *Datos* para hacer las operaciones necesarias y vuelve a devolver datos generales, de este modo permitimos que la capa de presentacion funcione sin conocimiento del ORM, así conseguimos independencia y flexibilidad. Esta capa permite modificar la BDD sin que la presentacion se vea afectada.
- **Presentación**: Es la responsable de atender las peticiones REST y devolver los datos pedidos, pero sin conocer como se obtienen en la base de datos o como son las clases del ORM

La división en 3 capas permite que cada una haga de fachada de las anteriores y así se simplifica enormemente el desarrollo, ya que fácilmente se pueden crear clases en cada capa para añadir funciónalidades sin afectar al resto del programa.

<div style="text-align: center;">

![Propuesta de datos](/imagenes/diagrama_capas.png "Diagrama propuesto")

</div>

#### 3.3 La Base de Datos
Realmente el diseño actual de servicios implica que por cada servidor REST habría una BDD distinta y tenemos una para *Auth* y otra para *Backend* pero como no se ha modificado *Auth* no se va a entrar en detalle.

El diagrama se ha realizado en base al diseño en el ORM por lo que se incluyen relaciones de herencia, aunque realmente no exitan en SQLITE.

El diagrama general:
![Diagrama de la BDD](/imagenes/diagrama_bdd.png "Diagrama frontend")

Vamos a distinguir 3 partes importantes en cuanto a las decisiones de diseño, los *elementos*, los *reportes* y los *votos*.

- **Elementos**: Se ha decidido usar el polimorfismo para preguntas, respuestas y comentarios debido a que todos comparten una parte importante de información, como el autor, la fecha de cración y el contenido pero además la interacción con ellos es similar todos se crear, reportar y votar de la misma manera. Las implicaciones son estas: todos lo elementos tienen una id de elemento que lo hace único, si hay una pregunta con id 1 no habrá un comentarios con id 1, si queremos votar un elemento o cambiar su visibilidad podemos usar una única función donde se reciban elementos aprovechando *liskov*.
- **Reportes**: Inicialmente solo iba a existir una clase de reporte con una relacción a elemento que sirviese para cualquier tipo de elemento pero por agilidad en las consultas, especialmente cuando hay que obtener todos los reportes a x tipo de elemento, separar los reportes en tipos simplifica las consultas pero provoca que sea mas complicado hacer funciónes que sirvan para todos los tipos de elemento. A pesar del polimorfismo es sencillo trabajar sobre los campos comunes, como el estado donde las funciones pueden recibir todos lo tipos de reporte.
- **Votos**: El modelo de voto es similar a como era el reporte en un inicio, se relaciona con elemento y así será posible votar todos los tipos de elemento. Se ha decidido hacer todos lo elementos votables a pesar que las preguntas no se requiere que lo sean, siendo estrictos habría que haber creado una clase mas hija de elemento, *ElementoVotable* con el que estuviese relacionado voto, pero se ha considerado que no implementar las funciónalidades de voto en pregunta es mas sencillo y permite mas flexibilidad a la hora de hacer cambios en un futuro si se permitiese votar las preguntas.

### 4. Trabajo futuro

Se propone crear un sistema de *recompensas* que a modo de servicio independiente, como *Auth* lleve la cuenta de los votos que reciben sus elementos, cuanto se le reporta o cuantas veces hace respuestas que hayan sido útiles u otras métricas que se puedan añadir para representar como de útil es un usuario en la comunidad.

Las métricas se podrían utilizar para dar *premios* a los usuarios que cumplan algunas condiciones, como insignias especiales por x respuestas o por haber alcanzado y votos positivos.

En cuanto a la implementacion a pesar que el almacenamiento y la gestión de métricas seria independiente, nos encontramos con el problema de como obtener estos datos, existirían 2 opciones:
1. Añadir *triggers* en la cración de elementos, votos y reportes e ir actualizando el servicio de recompensas. Seria problemático a la hora de implementarlo, ya que podria romper el principio de Open/Close de algunas clases.
2. Comprobar los datos de un ususario en momentos concretos, cuando inicia sesión, la cierra o cada x tiempo. Seria mas sencillo pero la latencia de actualizacion de datos aumentaria y las consultas serian mas pesadas.

> Los problemas de la opcion 1 se dan porque la implementación de las funciónes de cración de objetos en el ORM no permite la inclusion de nuevas funciónalidades. en un futuro seria interesante modificarlas de forma que permitan su extensión mediante inyección de dependencias.

Otra posibilidad, gracias al bajo acoplamiento del servicio, sería la posibilidad de utilizar estas puntuaciones, si se da el caso, para otras aplicaciónes que se hagan en un futuro, que no tengan preguntas o respuestas, pero donde se quiera conocer la reputación de los usuarios.

> Seria practico implementar un patrón observador, pero para ello seria necesario modificar las clases originales para añadir metodos de notificacion.

Una posibilidad de diseño seria esta:
![Propuesta de datos](/imagenes/propuesta.png "Diagrama propuesto")

En este caso un premio concreto se recibiría ligado a tener cierta métrica en un nivel concreto, permitiéndose crear multiples métricas y premios.
