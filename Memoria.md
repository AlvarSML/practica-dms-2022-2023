# Memoria

### 1. Propuesta general de diseño
 Propuesta de una interfaz sencilla estilo *stackoverflow* pero con comentarios de estilo *reddit* en varios niveles segun quien responde a quien. 
 
 El sistema de votacion puede ser estilo *reddit* o *stackoverflow* indistintamente, con enfoque en los puntos para el orden y como forma de recompensar al usuario, de esta forma como los comentarios mas votados aparecen primero no sera necesario que el usuario se tenga que leer todo.

 Un esquema simple de como apareceran los comentarios a una pregunta:
- Pregunta
  - Respuesta 1 
  - Respuesta 2 
    - Comentario a la respuesta 2 (👍)
  - Respuesta 3
    - Comentario a la respuesta 2 (👎)
  
#### 1.1 Diseño de las preguntas
Las preguntas podrian ser simples o se puede contemplar la opcion de agregar imagenes o texto enriquecido, se valorara segun complejidad durante el desarrollo del proyecto.

#### 1.2 Tipos de usuarios
En cuanto al la estructura de paginas podremos diferenciar entre las paginas para usuarios logeados y las de usuarios anonimos, a pesar que dentro de los logueados puedan existir distintos roles, los dos gradnes grupos son los anteriormente mensionados.

Un usuario no logueado:
- Podra ver las preguntas que hacen otros usuarios
- Al hacer click en una pregunta podra ver las respuestas a esta
- Se le dara la posibilidad de crearse una cuenta o iniciar sesion
- No se le permitira hacer nuevas preguntas o responderlas
- No podra votar las preguntas/respuestas
- No podra reportar preguntas/respuestas

Un usuario logueado podra realizar las actividades propias de su rol.

Por lo tanto se podra acceder a la pagina raiz o "inicio" sin estar logueado para tener una vision general de la aplicacion o a una pregunta en concreto, pero para hacer cualquier otra accion se tendra que estar logueado. El funcionamiento sera identico al de *StackOverflow*, de esta forma no sera necesario trabajar demasiado en la UX.

#### 1.3 Funciones de los usuarios

Dentro de los usuarios existen distintos roles:
- Discusion: Es el usuario standard, puede crear y responder preguntas.
- Moderador: Se encarga de atender los reportes sobre las preguntas y los comentarios.
- Administrador: Es un rol especial que solo lo tendra el primer usuario creado "admin"

Un usuario Moderador no podra publicar preguntas/respuestas y un Discusion no podra moderar.

#### 1.4 Elementos principales

La base de las aplicacion son las preguntas con respuestas a modo de resolucion y comentarios a la respuestas valorandolas, segun si son utiles o no. La dinamica es extremadamente parecida a la de *StackOverflow*.

- Pregunta (El usuario plantea un problema):
  - Tiene un titulo y un cuerpo
  - Puede ser votada (Positivo o Negativo)
  - Tiene un Autor
  - Tiene una fecha de creacion
- Respuestas (Los usuarios proponen soluciones):
  - Solo tienen cuerpo
  - Pueden ser votadas (Positivo o Negativo)
  - Tienen un autor
  - Siempre tienen una única pregunta asociada
  - Tienen una fecha de creacion
  - Otros usuarios con rol "Discusion" podrán valorar mediante comentarios si es útil o no.
- Comentario (Valoracion de una respuesta)
  - Solo tienen cuerpo y una mayor restriccion de longitud
  - Tienen asociado una valoracion sobre la respuesta *positiva, negativa o neutra*
  - Se mostrará la fecha de creacion y su autor
  - Tendran un tamñano mas reducido en pantalla
  - Se sombrearan según la valoracion
  - Podran ser votados para resaltar los mas útiles


### 2. Consideraciones de para el desarrollo
#### 2.1 Docker
Por su simplicidad se han decidido modificar los ficheros de instalacion e inicio y asi permitir el desarrollo sin necesiadad de reinicios.
Se ha asumido que los desarrolladores actuales han instalado las imagenes, por lo que se ha comentado las lineas de *"/practica-dms-2022-2023/components/dms2223auth/bin/dms2223auth-create-admin"* para que no se intente volver a crear el usuario admin.
Si se requiriese reinstalar la maquina habria que desomentarlas o no sera posible loguearse en la aplicacion.

Ademas para permitir la compatibilidad con WSL2 se ha editado *" practica-dms-2022-2023/docker/config/dev.yml" liena 33* para enlazar el puerto 8080 de Docker con el 8080 de Windows.

#### 2.2 Modo debug
Para agilizar el desarrollo se ha configurado Jinja/Flask para actualizarsa cada vez que se produce un cambio en el frontend, asi no sera necesario reiniciar el servicio o la maquina docker cada vez que haga un cambio a la web. 
Para ello se ha modificado:

- *practica-dms-2022-2023/components/dms2223frontend/install.sh*: Se ha comentado la eliminacion del directorio temporal, es posible que requiera ser descomentado para nuevas instalacions.
- *practica-dms-2022-2023/components/dms2223frontend/bin/dms2223frontend*: Se ha añadido:
```
app.config["TESTING"] = True
app.testing=True
app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)
```
Esto permite la recarga automatica de templates y codigo de las peticiones del mismo archivo. 
Es recomendable eliminar estas lineas en un futuro despliegue.

### 3. Arquitectura de la aplicacion
#### 3.1. Arquitectura del frontend
  El *frontend* se encarga por una parte de mostrar las los datos al usuario y
por otro hace solicitudes a servidores de datos mediante sus *API REST*. En nuestro caso hacemos uso de 2 de estos servicios, el de *Autenticacion* que gestiona usuarios y roles y el de *backend* que gestiona los datos generales de la aplicacion.

Para llevar a cabo estos procesos se usan 2 capas:
  - **Capa de presentacion**: Englobaria los endpoints y sus templates asociadas, únicamente muestran informacion por el navegador y solo tiene conocimiento de la actividad del usuario, a que partes entra o donde hace click.
  - **Capa de servicios**:  Se encarga de las comunicaciones con las APIs. Recibe peticiones de la capa de presentacion para obtener datos, tiene el conocimiento de los servicios externos que se usan. En general contruya las peticiones HTTP y comprueba las respuestas.

De esta forma se pueden añadir servicios para APIs nuevas en futuras apliaciones sin tener que modificar los actuales, pero puediendo hacer uso de ellos (Se respeta el principio Open/Close). Ademas queda separada la responsabilidad del acceso a datos de la de mostrarlos (Principio Single Responsibility)

![Diagrama del frontend](/imagenes/frontend.png "Diagrama frontend")

#### 3.2 Arquitectura del backend
El backend es responsable de la gestion de todos los datos y de su presentacion a consumidores externos.

Dada la complejidad del backend, que no es excesiba, se ha decidido usar una arquitectura de 3 capas. Aunque en un principio se barajó usar 4 se llegó a la conclusion que la capa de logica y servicios se podian unir ya que no habia ninguna razon que justificase tener una capa dedicada unicamente a logica.

Las capas son:

- **Datos**: En esta capa se realizan las consultas a la base de datos a traves del ORM (SQLAlchemy), esta capa por lo tanto tiene conocimiento de la estructura de la BDD y de las clases del ORM, por eso esta capa recoge clases que contienen fuciones cuyos paramentros son clases del orm, al igual que los resultados que devuelve. Se garantiza la responsabilidad única mediante funciones para cada consulta y se aplica el principio de sustitución de Liskov donde el polimorfismo lo permite, por ejemplo en el caso de los elementos donde para ocultarlos lo podemos hacer con la misma funcion siempre que el objeto introducido sea una instancia de una clase hija de elemento.
- **Servicios (Logica)**: La capa de logica por conveniencia se ha llamado de "servicios", donde cada uno tiene conocimento de un ambito del backend. Esta capa hace de intermediario entre *Presentacion* y *Datos*, recibe diccionarios de datos, se comunica con *Datos* para hacer las operaciones necesarias y vuelve a devolver datos generales, de este modo permitimos que la capa de presentacion funcione sin conocimiento del ORM, asi conseguimos independencia y flexibilidad. Esta capa permite modificar la BDD sin que la presentacion se vea afectada.
- **Presentacion**: Es la responsable de atender las peticiones REST y devolver los datos pedidos, pero sin conocer como se obtienen en la base de datos o como son las clases del ORM

La division en 3 capas permite que cada una haga de fachada de las anteriores y asi se simplifica enormemente el desarrollo, ya que facilmente se pueden crear clases en cada capa para añadir funcionalidades sin afectar al resto del programa.

#### 3.3 La Base de Datos
Realmente el diseño actual de servicios implica que por cada servidor REST habria una BDD distinta y tenemos una para *Auth* y otra para *Backend* pero como no se ha modificado *Auth* no se va a entrar en detalle.

El diagrama se ha realizado en base al diseño en el ORM por lo que se incluyen relacciones de herencia, aunque realmente no exitan en SQLITE.

El diagrama general:
![Diagrama de la BDD](/imagenes/diagrama_bdd.png "Diagrama frontend")

Vamos a distinguir 3 partes importantes en cuanto a las decisiones de diseño, los *elementos*, los *reportes* y los *votos*.

- **Elementos**: Se ha decidido usar el polimorfismo para preguntas, respuestas y comentarios debido a que todos comparten una parte importante de informacion, como el autor, la fecha de creacion y el continido pero además la interaccion con ellos es similar todos se crear, reportar y votar de la misma manera. Las implicaciones son estas: todos lo elementos tienen una id de elemento que lo hace unico, si hay una pregunta con id 1 no habra un comentarion con id 1, si queremos votar un elemento o cambiar su visibilidad podemos usar una única funcion donde se reciban elementos aprovechando *liskov*.
- **Reportes**: Inicialmente solo iba a existir una clase de reporte con una relaccion a elemento que sirviese para cualquier tipo de elemento pero por agilidad en las consultas, especialmente cuando hay que obtener todos los reportes a x tipo de elemento, separar los reportes en tipos simplifica las consultas pero provoca que sea mas complicado hacer funciones que sirvan para todos los tipos de elemento. A pesar del polimorfismo es sencillo trabajar sobre los campos comunes, como el estado donde las fucniones pueden recibir todos lo tipos de reporte.
- **Votos**: El modelo de voto es similar a como era el reporte en un inicio, se relacciona con elemento y asi sera posible votar todos los tipos de elemento. Se ha decidido hacer todos lo elementos votables a pesar que las preguntas no se requiere que lo sean, siendo estrictos habria que haber creado una clase mas hija de elemento, *ElementoVotable* con el que estuviese relaccionado voto, pero se ha considerado que no implementar las funcionalidades de voto en pregunta es mas sencillo y permite mas flexibilidad a la hora de hacer cambios en un futuro si se permitiese votar las preguntas.

<div style="text-align: center;">

![Propuesta de datos](/imagenes/diagrama_capas.png "Diagrama propuesto")

</div>

### 4. Trabajo futuro

Se propone crear un sistema de *recompensas* que a modo de servicio independiente, como *Auth* lleve la cuenta de los votos que reciben sus elementos, cuanto se le reporta o cuantas veces hace respuestas que hayan sido útiles u otras metricas que se puedan añadir para representar como de util es un usuario en la comunidad.

Las metricas se podrian utilizar para dar *premios* a los usuarios que cumplan algunas condiciones, como insignias especiales por x respuestas o por haber alcanzado y votos positivos.

En cuanto a la implementacion a pesar que el almacenamiento y la genstion de metricas seria independiente, nos encontramos con el problema de como obtener estos datos, existirian 2 opciones:
1. Añadir *triggers* en la creacion de elementos, votos y reportese ir actualizando el servicio de recompensas. Seria problematico a la hora de implementarlo, ya que podria romper el principio de Open/Close de algunas clases.
2. Comprobar los datos de un ususario en momentos concretos, cuando inicia sesion, la cierra o cada x tiempo. Seria mas sencillo pero la latencia de actualizacion de datos aumentaria y las consultas serian mas pesadas.

> Los problemas de la opcion 1 se dan porque la implementacion de las funciones de creacion de objetos en el ORM no permite la inclusion de nuevas funcionalidades. en un futuro seria interesante modificarlas de forma que permitan su extension mediante inyeccion de dependencias.

Otra posibilidad, gracias al bajo acoplamiento del servicio, seria la posibilidad de utilizar estas puntuaciones, si se da el caso, para otras aplicaciones que se hagan en un futuro, que no tengan preguntas o respuestas pero donde se quiera conocer la reputación de los usuarios.

Una posibilidad de diseño seria esta:
![Propuesta de datos](/imagenes/propuesta.png "Diagrama propuesto")

En este caso un premio concreto se recibiria ligado a tener cierta metrica en un nivel concreto, permitiendose crear multiples metricas y premios.

TODO: Falta diagrama de capas