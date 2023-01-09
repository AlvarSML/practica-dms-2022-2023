# Requisitos para el proyecto de DMS

## Memoria
1. Formato **Markdown**
2. Se debe documentar la arquitectura
3. Justificacion de las decisiones de diseño (SOLID)
4. La última entrega debe recoger el trabajo futuro, pasos necesarios pero no implementarlo
   

## Entrega 1 - 13 Noviembre 2022 - 10pt
Ya tenemos :
- 🔑 Servicio de autenticación ( Está completo, no hay que tocarlo)
- ⚛ Servicio Backend (API) Organizado en *4 capas* pero es modificable
- ✨Fronted (Paginas y plantillas, web)

### Requisitos Funcionales:
1. Creacion de preguntas, respuestas y reportes
   1. [x] Las preguntas tienen un **titulo** y un **cuerpo**
   2. [] Solo los usuarios con rol de **discusion** podra crear preguntas y responder a las existentes
   3. [x] Los comentarios tienen un **feedback** positivo, negativo o neutro asociado sobre la respuesta
   4. [x] Las preguntas y respuestas (y comentarios) tienen **votos**
   5. [x] Se puede **reportar** todo, con una razón asociada
   6. [x] Todos los elementos anteriores tienen un **propietario**, el creador
   7. [x] Todos los elementos tienen un **timestamp** de su creación
   
2. Moderacion
   1. [x] Al usuario moderador le **llegan los reportes**
   2. [x] Un reporte puede ser **pendiente, aceptado o rechazado**
   3. [x] Un reporte se puede declarar **rechazado o aceptado**
   4. [x] Si se acepta un reporte, el elemento y sus hijos se **ocultan** permanentemente pero no se eliminan

3. Sesion
   1. [x] Todos los usuarios **iniciaran sesion** al entrar en la aplicación
   2. [] Los distintios roles tienen **operaciones** distintas (interfaces distintas?)
   3. [] Los permisos **no son jerarquicos** (Ej.: Un moderardor no comenta)
   4. [x] Boton de **cerrar sesión**

### Requisitos no funcionales:
1. Usar tipado estatico 🛑Penalizacion si no se usa en puntos clave🛑
2. Estilo correcto 7️⃣/🔟 Minimo
3. Participación de todo el grupo, según commits
4. Manuales, instalación y uso 📗


### Pendiente:
- [x] Completar los **"TODO"** del codigo 
- [x] Crear fronted estatico
- [ ] Cumplir los requisitos funcionales
- [ ] Cumplir los requisitos no funcionales
- [x] Rellenar la memoria

## Entrega 2 - 4 Diciembre 2022 - 10pt

Pendiente de la entrega 1
- [x] La memoria: Hablar sobre la arquitectura de la aplicacion y de los patrones a usar en cada componente
- [x] La pantalla de moderacion

A hacer en la entrega 2, todo lo relativo al backend:
- _Dentro del backend_ (API) se hacen las consultas a la base de datos devolviendo lo que se considere necesario segun la direccion por la que se entra.
- _En el fontend_ se hacen las llamadas al backend que se consideren oportunas para obtener los datos


## Entrega 3 - 18 Diciembre 2022 - 20pt