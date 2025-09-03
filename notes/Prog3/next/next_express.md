# Uso de next() en Express.js

La función `next()` en Express.js es fundamental para controlar el flujo de una solicitud HTTP a través de la cadena de middlewares. Voy a simplificar cómo funciona:

## ¿Qué es next() en Express?

Es una función que permite que una solicitud avance a través de la cadena de middlewares en una aplicación Express. Determina cuál será el siguiente paso en el procesamiento de una solicitud HTTP.

## Formas básicas de usar next()

1. **`next()`**: Continúa con el siguiente middleware en la pila
2. **`next('route')`**: Salta al siguiente patrón de ruta
3. **`next(error)`**: Salta a los middlewares de manejo de errores
4. **No llamar a next() ni enviar respuesta**: La solicitud queda colgada (timeout)

## Ejemplos prácticos simplificados

### Uso básico de next()

```javascript
app.use((req, res, next) => {
  console.log('Pasando por el primer middleware');
  next(); // Continúa al siguiente middleware
});

app.use((req, res, next) => {
  console.log('Pasando por el segundo middleware');
  res.send('Respuesta enviada'); // No se llama a next(), termina aquí
});
```

### Middleware condicional

```javascript
const autenticar = (req, res, next) => {
  if (req.headers.authorization) {
    next(); // Usuario autenticado, continúa al siguiente middleware
  } else {
    res.status(401).send('No autorizado'); // La cadena termina aquí
  }
};

app.get('/area-restringida', autenticar, (req, res) => {
  res.send('Bienvenido al área restringida');
});
```

### Manejo de errores con next(error)

```javascript
app.get('/datos', async (req, res, next) => {
  try {
    const datos = await obtenerDatos();
    res.json(datos);
  } catch (error) {
    next(error); // Pasa el error al middleware de errores
  }
});

// Middleware de manejo de errores (siempre tiene 4 parámetros)
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).send('Algo salió mal');
});
```

### Múltiples middlewares en una ruta

```javascript
app.get('/usuarios/:id',
  // Middleware 1: validación
  (req, res, next) => {
    if (!req.params.id) return res.status(400).send('ID requerido');
    next();
  },
  // Middleware 2: obtención de datos
  (req, res, next) => {
    // Simulando obtención de usuario
    req.usuario = { id: req.params.id, nombre: 'Usuario' };
    next();
  },
  // Controlador final
  (req, res) => {
    res.json(req.usuario);
  }
);
```

## Regla esencial

**Nota Importante:** Siempre debes llamar a `next()` o enviar una respuesta con `res`. Si no lo haces, la solicitud quedará colgada indefinidamente.

Esta simplificación muestra los conceptos clave del uso de `next()` en Express.js, facilitando el entendimiento de cómo controlar el flujo de las solicitudes HTTP a través de los middlewares.