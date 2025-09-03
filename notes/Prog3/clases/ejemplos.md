# Ejemplos de Programación Orientada a Objetos en JavaScript

## 1. Relaciones entre Objetos

### 1.1 Asociación

La asociación es una relación en la que un objeto utiliza o interactúa con otro, pero ambos pueden existir independientemente.

```javascript
// Asociación: Un profesor puede estar asociado a varios cursos
class Profesor {
  constructor(nombre, especialidad) {
    this.nombre = nombre;
    this.especialidad = especialidad;
    this.cursos = []; // Referencias a cursos que enseña
  }
  
  asignarCurso(curso) {
    this.cursos.push(curso);
    curso.asignarProfesor(this);
  }
  
  listarCursos() {
    return this.cursos.map(curso => curso.nombre);
  }
}

class Curso {
  constructor(nombre, codigo) {
    this.nombre = nombre;
    this.codigo = codigo;
    this.profesor = null; // Referencia al profesor
  }
  
  asignarProfesor(profesor) {
    this.profesor = profesor;
  }
  
  getInfoCurso() {
    return `${this.codigo}: ${this.nombre} - Profesor: ${this.profesor ? this.profesor.nombre : 'Sin asignar'}`;
  }
}

// Uso
const profJuan = new Profesor('Juan Pérez', 'Programación');
const cursoJS = new Curso('JavaScript Avanzado', 'JS101');
const cursoPython = new Curso('Python Básico', 'PY101');

profJuan.asignarCurso(cursoJS);
profJuan.asignarCurso(cursoPython);

console.log(profJuan.listarCursos()); // ['JavaScript Avanzado', 'Python Básico']
console.log(cursoJS.getInfoCurso()); // 'JS101: JavaScript Avanzado - Profesor: Juan Pérez'
```

### 1.2 Agregación

En la agregación, un objeto contiene otros objetos, pero éstos pueden existir de forma independiente.

```javascript
// Agregación: Un equipo contiene jugadores, pero los jugadores pueden existir sin el equipo
class Jugador {
  constructor(nombre, posicion) {
    this.nombre = nombre;
    this.posicion = posicion;
  }
  
  getInfo() {
    return `${this.nombre} (${this.posicion})`;
  }
}

class Equipo {
  constructor(nombre) {
    this.nombre = nombre;
    this.jugadores = []; // Agregación: el equipo tiene jugadores
  }
  
  agregarJugador(jugador) {
    this.jugadores.push(jugador);
  }
  
  quitarJugador(nombreJugador) {
    this.jugadores = this.jugadores.filter(j => j.nombre !== nombreJugador);
  }
  
  listarJugadores() {
    return this.jugadores.map(j => j.getInfo());
  }
}

// Uso
const leo = new Jugador('Leo Messi', 'Delantero');
const cristiano = new Jugador('Cristiano Ronaldo', 'Delantero');
const neymar = new Jugador('Neymar Jr', 'Extremo');

const barcelona = new Equipo('FC Barcelona');
barcelona.agregarJugador(leo);
barcelona.agregarJugador(neymar);

const juventus = new Equipo('Juventus');
juventus.agregarJugador(cristiano);

console.log(barcelona.listarJugadores()); // ['Leo Messi (Delantero)', 'Neymar Jr (Extremo)']

// Si el Barcelona "libera" a Neymar, éste sigue existiendo
barcelona.quitarJugador('Neymar Jr');
// Neymar podría unirse a otro equipo
juventus.agregarJugador(neymar);

console.log(juventus.listarJugadores()); // ['Cristiano Ronaldo (Delantero)', 'Neymar Jr (Extremo)']
```

### 1.3 Composición

En la composición, un objeto está compuesto por otros objetos que dependen de él, y si el objeto contenedor se destruye, también lo hacen sus componentes.

```javascript
// Composición: Un automóvil está compuesto por motor y ruedas. Si el automóvil "muere", sus partes también
class Motor {
  constructor(tipo, potencia) {
    this.tipo = tipo;
    this.potencia = potencia;
    this.encendido = false;
  }
  
  encender() {
    this.encendido = true;
    return `Motor ${this.tipo} encendido`;
  }
  
  apagar() {
    this.encendido = false;
    return `Motor ${this.tipo} apagado`;
  }
}

class Rueda {
  constructor(posicion) {
    this.posicion = posicion;
    this.presion = 2.2;
  }
  
  inflar(presion) {
    this.presion = presion;
    return `Rueda ${this.posicion} inflada a ${this.presion} bar`;
  }
}

class Automovil {
  constructor(marca, modelo) {
    this.marca = marca;
    this.modelo = modelo;
    // Composición: las partes son creadas por el automóvil
    this.motor = new Motor("V6", 300);
    this.ruedas = [
      new Rueda("delantera-izquierda"),
      new Rueda("delantera-derecha"),
      new Rueda("trasera-izquierda"),
      new Rueda("trasera-derecha")
    ];
  }
  
  encender() {
    return `${this.marca} ${this.modelo}: ${this.motor.encender()}`;
  }
  
  apagar() {
    return `${this.marca} ${this.modelo}: ${this.motor.apagar()}`;
  }
  
  inflarRuedas(presion) {
    return this.ruedas.map(rueda => rueda.inflar(presion));
  }
}

// Uso
const miAuto = new Automovil("Toyota", "Corolla");
console.log(miAuto.encender()); // 'Toyota Corolla: Motor V6 encendido'
console.log(miAuto.inflarRuedas(2.4)); // ['Rueda delantera-izquierda inflada a 2.4 bar', ...]

// Si el auto se destruye (por ejemplo, se elimina la referencia)
// el motor y las ruedas también desaparecen ya que no tienen existencia independiente
```

## 2. Buenas Prácticas en POO

### 2.1 Principio de Responsabilidad Única (SRP)

Cada clase debe tener una única razón para cambiar.

```javascript
// MAL: Clase con múltiples responsabilidades
class UsuarioMal {
  constructor(nombre, email) {
    this.nombre = nombre;
    this.email = email;
    this.carrito = [];
  }
  
  // Responsabilidad: gestión de usuario
  actualizarPerfil(nuevoNombre, nuevoEmail) {
    this.nombre = nuevoNombre;
    this.email = nuevoEmail;
  }
  
  // Responsabilidad: autenticación
  verificarCredenciales(password) {
    // lógica de autenticación
    return password === "contraseña123";
  }
  
  // Responsabilidad: gestión de carrito
  agregarAlCarrito(producto) {
    this.carrito.push(producto);
  }
  
  calcularTotalCarrito() {
    return this.carrito.reduce((total, producto) => total + producto.precio, 0);
  }
  
  // Responsabilidad: envío de emails
  enviarEmailConfirmacion() {
    console.log(`Enviando email a ${this.email}...`);
    // lógica para enviar email
  }
}

// BIEN: Clases con responsabilidades únicas
class Usuario {
  constructor(nombre, email) {
    this.nombre = nombre;
    this.email = email;
  }
  
  actualizarPerfil(nuevoNombre, nuevoEmail) {
    this.nombre = nuevoNombre;
    this.email = nuevoEmail;
  }
}

class Autenticador {
  verificarCredenciales(usuario, password) {
    // lógica de autenticación
    return password === "contraseña123";
  }
}

class Carrito {
  constructor(usuario) {
    this.usuario = usuario;
    this.productos = [];
  }
  
  agregarProducto(producto) {
    this.productos.push(producto);
  }
  
  calcularTotal() {
    return this.productos.reduce((total, producto) => total + producto.precio, 0);
  }
}

class NotificadorEmail {
  static enviarConfirmacion(usuario, mensaje) {
    console.log(`Enviando email a ${usuario.email}: ${mensaje}`);
    // lógica para enviar email
  }
}

// Uso
const usuario = new Usuario("Ana", "ana@ejemplo.com");
const carrito = new Carrito(usuario);
const autenticador = new Autenticador();

if (autenticador.verificarCredenciales(usuario, "contraseña123")) {
  carrito.agregarProducto({nombre: "Laptop", precio: 1200});
  console.log(`Total: $${carrito.calcularTotal()}`);
  NotificadorEmail.enviarConfirmacion(usuario, "Su compra fue realizada con éxito");
}
```

### 2.2 Ley de Demeter (Principio de Menor Conocimiento)

Un objeto sólo debe hablar con sus "amigos cercanos" y no con extraños.

```javascript
// MAL: Violación de la Ley de Demeter
class Cartera {
  constructor(dinero) {
    this.dinero = dinero;
  }
  
  getDinero() {
    return this.dinero;
  }
  
  extraerDinero(cantidad) {
    if (cantidad <= this.dinero) {
      this.dinero -= cantidad;
      return cantidad;
    }
    return 0;
  }
}

class PersonaMal {
  constructor(nombre, dinero) {
    this.nombre = nombre;
    this.cartera = new Cartera(dinero);
  }
  
  getCartera() {
    return this.cartera;
  }
}

class ComercianteMal {
  venderProducto(persona, precioProducto) {
    // Viola la Ley de Demeter: accede a un objeto a través de otro
    if (persona.getCartera().getDinero() >= precioProducto) {
      persona.getCartera().extraerDinero(precioProducto);
      return `Producto vendido a ${persona.nombre}`;
    }
    return `${persona.nombre} no tiene suficiente dinero`;
  }
}

// BIEN: Respetando la Ley de Demeter
class CarteraBien {
  constructor(dinero) {
    this.dinero = dinero;
  }
  
  tieneSuficiente(cantidad) {
    return this.dinero >= cantidad;
  }
  
  extraer(cantidad) {
    if (this.tieneSuficiente(cantidad)) {
      this.dinero -= cantidad;
      return cantidad;
    }
    return 0;
  }
}

class PersonaBien {
  constructor(nombre, dinero) {
    this.nombre = nombre;
    this.cartera = new CarteraBien(dinero);
  }
  
  tieneSuficienteDinero(cantidad) {
    return this.cartera.tieneSuficiente(cantidad);
  }
  
  pagar(cantidad) {
    return this.cartera.extraer(cantidad);
  }
}

class ComercianteBien {
  venderProducto(persona, precioProducto) {
    // Respeta la Ley de Demeter: solo habla con el objeto persona
    if (persona.tieneSuficienteDinero(precioProducto)) {
      persona.pagar(precioProducto);
      return `Producto vendido a ${persona.nombre}`;
    }
    return `${persona.nombre} no tiene suficiente dinero`;
  }
}

// Uso
const maria = new PersonaBien("María", 500);
const comerciante = new ComercianteBien();

console.log(comerciante.venderProducto(maria, 300)); // 'Producto vendido a María'
console.log(comerciante.venderProducto(maria, 300)); // 'María no tiene suficiente dinero'
```

### 2.3 Interfaces e Implementación

JavaScript no tiene interfaces nativas, pero podemos simularlas.

```javascript
// Simulación de una interfaz usando una clase abstracta
class FormaGeometrica {
  constructor() {
    if (this.constructor === FormaGeometrica) {
      throw new Error("No se puede instanciar una clase abstracta");
    }
  }
  
  calcularArea() {
    throw new Error("Método abstracto 'calcularArea()' debe ser implementado");
  }
  
  calcularPerimetro() {
    throw new Error("Método abstracto 'calcularPerimetro()' debe ser implementado");
  }
}

// Implementaciones concretas
class Rectangulo extends FormaGeometrica {
  constructor(ancho, alto) {
    super();
    this.ancho = ancho;
    this.alto = alto;
  }
  
  calcularArea() {
    return this.ancho * this.alto;
  }
  
  calcularPerimetro() {
    return 2 * (this.ancho + this.alto);
  }
}

class Circulo extends FormaGeometrica {
  constructor(radio) {
    super();
    this.radio = radio;
  }
  
  calcularArea() {
    return Math.PI * this.radio * this.radio;
  }
  
  calcularPerimetro() {
    return 2 * Math.PI * this.radio;
  }
}

// Función que trabaja con la "interfaz" FormaGeometrica
function imprimirInfoForma(forma) {
  if (!(forma instanceof FormaGeometrica)) {
    throw new Error("El parámetro debe implementar FormaGeometrica");
  }
  
  console.log(`Área: ${forma.calcularArea()}`);
  console.log(`Perímetro: ${forma.calcularPerimetro()}`);
}

// Uso
const rectangulo = new Rectangulo(5, 3);
const circulo = new Circulo(4);

imprimirInfoForma(rectangulo);
// Área: 15
// Perímetro: 16

imprimirInfoForma(circulo);
// Área: 50.26548245743669
// Perímetro: 25.132741228718345

// Esto daría error:
// const formaInvalida = new FormaGeometrica();
// imprimirInfoForma(formaInvalida);
```

## 3. Patrones de Diseño Comunes en POO

### 3.1 Singleton

Garantiza que una clase tenga una única instancia y proporciona un punto de acceso global a ella.

```javascript
class Configuracion {
  constructor() {
    // Si ya existe una instancia, devuélvela
    if (Configuracion.instancia) {
      return Configuracion.instancia;
    }
    
    // Configuración por defecto
    this.tema = "claro";
    this.notificaciones = true;
    this.idioma = "es";
    
    // Guardar la instancia
    Configuracion.instancia = this;
  }
  
  getConfig() {
    // Devolvemos una copia para evitar modificaciones directas
    return { 
      tema: this.tema, 
      notificaciones: this.notificaciones, 
      idioma: this.idioma 
    };
  }
  
  setConfig(clave, valor) {
    if (clave in this) {
      this[clave] = valor;
      return true;
    }
    return false;
  }
}

// Uso
const config1 = new Configuracion();
const config2 = new Configuracion();

console.log(config1 === config2); // true, ambas variables apuntan a la misma instancia

config1.setConfig("tema", "oscuro");
console.log(config2.getConfig().tema); // "oscuro", la modificación se refleja en todas las referencias
```

### 3.2 Factory Method

Define una interfaz para crear objetos, permitiendo a las subclases decidir qué clase instanciar.

```javascript
// Producto abstracto
class Notificacion {
  constructor() {
    if (this.constructor === Notificacion) {
      throw new Error("Clase abstracta Notificacion no puede ser instanciada");
    }
  }
  
  enviar(mensaje) {
    throw new Error("Método abstracto enviar() debe ser implementado");
  }
}

// Productos concretos
class NotificacionEmail extends Notificacion {
  constructor(destinatario) {
    super();
    this.destinatario = destinatario;
  }
  
  enviar(mensaje) {
    return `Enviando correo a ${this.destinatario}: ${mensaje}`;
  }
}

class NotificacionSMS extends Notificacion {
  constructor(telefono) {
    super();
    this.telefono = telefono;
  }
  
  enviar(mensaje) {
    return `Enviando SMS a ${this.telefono}: ${mensaje}`;
  }
}

class NotificacionPush extends Notificacion {
  constructor(deviceId) {
    super();
    this.deviceId = deviceId;
  }
  
  enviar(mensaje) {
    return `Enviando notificación push a dispositivo ${this.deviceId}: ${mensaje}`;
  }
}

// Creador abstracto
class CreadorNotificacion {
  constructor() {
    if (this.constructor === CreadorNotificacion) {
      throw new Error("Clase abstracta CreadorNotificacion no puede ser instanciada");
    }
  }
  
  // Factory method
  crearNotificacion() {
    throw new Error("Método abstracto crearNotificacion() debe ser implementado");
  }
  
  // Método que usa el factory method
  enviarNotificacion(mensaje) {
    const notificacion = this.crearNotificacion();
    return notificacion.enviar(mensaje);
  }
}

// Creadores concretos
class CreadorNotificacionEmail extends CreadorNotificacion {
  constructor(destinatario) {
    super();
    this.destinatario = destinatario;
  }
  
  crearNotificacion() {
    return new NotificacionEmail(this.destinatario);
  }
}

class CreadorNotificacionSMS extends CreadorNotificacion {
  constructor(telefono) {
    super();
    this.telefono = telefono;
  }
  
  crearNotificacion() {
    return new NotificacionSMS(this.telefono);
  }
}

class CreadorNotificacionPush extends CreadorNotificacion {
  constructor(deviceId) {
    super();
    this.deviceId = deviceId;
  }
  
  crearNotificacion() {
    return new NotificacionPush(this.deviceId);
  }
}

// Función que selecciona el tipo de notificación según preferencias del usuario
function notificadorFactory(usuario) {
  if (usuario.preferenciaNotificacion === "email") {
    return new CreadorNotificacionEmail(usuario.email);
  } else if (usuario.preferenciaNotificacion === "sms") {
    return new CreadorNotificacionSMS(usuario.telefono);
  } else {
    return new CreadorNotificacionPush(usuario.deviceId);
  }
}

// Uso
const usuario1 = {
  nombre: "Juan",
  email: "juan@ejemplo.com",
  preferenciaNotificacion: "email"
};

const usuario2 = {
  nombre: "María",
  telefono: "+1234567890",
  preferenciaNotificacion: "sms"
};

const notificador1 = notificadorFactory(usuario1);
const notificador2 = notificadorFactory(usuario2);

console.log(notificador1.enviarNotificacion("Nuevo mensaje")); 
// 'Enviando correo a juan@ejemplo.com: Nuevo mensaje'

console.log(notificador2.enviarNotificacion("Nuevo mensaje")); 
// 'Enviando SMS a +1234567890: Nuevo mensaje'
```

### 3.3 Observer (Observador)

Define una dependencia uno-a-muchos entre objetos, de modo que cuando un objeto cambia de estado, todos sus dependientes son notificados y actualizados automáticamente.

```javascript
// Observable (Sujeto)
class Tienda {
  constructor(nombre) {
    this.nombre = nombre;
    this.observadores = [];
    this.productos = [];
  }
  
  suscribir(observador) {
    this.observadores.push(observador);
  }
  
  desuscribir(observador) {
    this.observadores = this.observadores.filter(obs => obs !== observador);
  }
  
  notificar(datos) {
    for (const observador of this.observadores) {
      observador.actualizar(datos);
    }
  }
  
  agregarProducto(producto) {
    this.productos.push(producto);
    this.notificar({
      tienda: this.nombre,
      evento: 'nuevo_producto',
      producto: producto
    });
  }
  
  cambiarPrecio(productoId, nuevoPrecio) {
    const producto = this.productos.find(p => p.id === productoId);
    if (producto) {
      const precioAnterior = producto.precio;
      producto.precio = nuevoPrecio;
      this.notificar({
        tienda: this.nombre,
        evento: 'cambio_precio',
        producto: producto,
        precioAnterior: precioAnterior,
        precioNuevo: nuevoPrecio
      });
    }
  }
}

// Interfaz Observer
class Observer {
  constructor() {
    if (this.constructor === Observer) {
      throw new Error("Clase abstracta Observer no puede ser instanciada");
    }
  }
  
  actualizar(datos) {
    throw new Error("Método abstracto actualizar() debe ser implementado");
  }
}

// Observadores concretos
class ClienteObservador extends Observer {
  constructor(nombre) {
    super();
    this.nombre = nombre;
  }
  
  actualizar(datos) {
    if (datos.evento === 'nuevo_producto') {
      console.log(`Hola ${this.nombre}, hay un nuevo producto en ${datos.tienda}: ${datos.producto.nombre} por $${datos.producto.precio}`);
    } else if (datos.evento === 'cambio_precio') {
      if (datos.precioNuevo < datos.precioAnterior) {
        console.log(`¡${this.nombre}! El precio de ${datos.producto.nombre} en ${datos.tienda} ha bajado de $${datos.precioAnterior} a $${datos.precioNuevo}`);
      }
    }
  }
}

class ProveedorObservador extends Observer {
  constructor(nombreEmpresa) {
    super();
    this.nombreEmpresa = nombreEmpresa;
  }
  
  actualizar(datos) {
    if (datos.evento === 'nuevo_producto') {
      console.log(`[${this.nombreEmpresa}] Nuevo producto agregado a ${datos.tienda}: ${datos.producto.nombre}`);
    } else if (datos.evento === 'cambio_precio') {
      console.log(`[${this.nombreEmpresa}] ${datos.tienda} ha cambiado el precio de ${datos.producto.nombre} de $${datos.precioAnterior} a $${datos.precioNuevo}`);
    }
  }
}

// Uso
const tienda = new Tienda("TechStore");

const cliente1 = new ClienteObservador("Ana");
const cliente2 = new ClienteObservador("Carlos");
const proveedor = new ProveedorObservador("TechSupplies Inc");

tienda.suscribir(cliente1);
tienda.suscribir(cliente2);
tienda.suscribir(proveedor);

// Agregar un nuevo producto
tienda.agregarProducto({
  id: 1,
  nombre: "Smartphone XYZ",
  precio: 599
});

// Cambiar el precio (descuento)
tienda.cambiarPrecio(1, 499);

// Ana ya no quiere recibir notificaciones
tienda.desuscribir(cliente1);

// Otro cambio de precio
tienda.cambiarPrecio(1, 549);
```
