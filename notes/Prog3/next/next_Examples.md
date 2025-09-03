# Uso de next() en Express.js

## 1. Uso Básico de next()

Este ejemplo muestra cómo la solicitud fluye a través de varios middlewares utilizando `next()`:

```javascript
const express = require('express');
const app = express();

// Middleware 1: Logger
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next(); // Pasa al siguiente middleware
});

// Middleware 2: Añadir datos a la solicitud
app.use((req, res, next) => {
  req.tiempoInicio = Date.now();
  next(); // Pasa al siguiente middleware
});

// Ruta específica
app.get('/hello', (req, res) => {
  const tiempoTotal = Date.now() - req.tiempoInicio;
  res.send(`Hello World! (Procesado en ${tiempoTotal}ms)`);
  // No hay next() porque la respuesta ya fue enviada
});

app.listen(3000, () => {
  console.log('Servidor ejecutándose en puerto 3000');
});
```

## 2. next('route') - Saltar a la Siguiente Ruta

Este ejemplo demuestra cómo usar `next('route')` para saltar a la siguiente definición de ruta:

```javascript
const express = require('express');
const app = express();

// Definición de ruta con múltiples controladores
app.get('/usuario/:id',
  // Middleware para verificar si el usuario es administrador
  (req, res, next) => {
    if (req.params.id === 'admin') {
      // Si es admin, salta a la siguiente definición de ruta
      next('route');
    } else {
      // Si no es admin, continúa con el siguiente middleware
      next();
    }
  },
  // Este middleware solo se ejecuta para usuarios no admin
  (req, res) => {
    res.send(`Usuario regular: ${req.params.id}`);
  }
);

// Esta es la siguiente definición de ruta (se ejecuta si se llama a next('route'))
app.get('/usuario/:id', (req, res) => {
  res.send('Panel de administrador');
});

app.listen(3000);
```

## 3. next(error) - Manejo de Errores

Muestra cómo pasar errores a un middleware especial para manejarlos:

```javascript
const express = require('express');
const app = express();

// Middleware que podría generar un error
app.get('/division/:numerador/:denominador', (req, res, next) => {
  const numerador = parseInt(req.params.numerador);
  const denominador = parseInt(req.params.denominador);
  
  if (denominador === 0) {
    // Pasamos un error al siguiente middleware de manejo de errores
    next(new Error('No se puede dividir por cero'));
  } else {
    res.send(`Resultado: ${numerador / denominador}`);
  }
});

// Middleware de manejo de errores (SIEMPRE tiene 4 parámetros)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send(`Error: ${err.message}`);
});

app.listen(3000);
```

## 4. Middleware Asíncrono con next()

Ejemplo de cómo manejar operaciones asíncronas correctamente con `next()`:

```javascript
const express = require('express');
const app = express();

// Simulación de una función que obtiene datos de forma asíncrona
function obtenerDatosDeBaseDeDatos(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id <= 0) {
        reject(new Error('ID no válido'));
      } else {
        resolve({ id, nombre: `Usuario ${id}` });
      }
    }, 500);
  });
}

// Middleware que maneja una operación asíncrona
app.get('/usuario/:id', async (req, res, next) => {
  try {
    const id = parseInt(req.params.id);
    const usuario = await obtenerDatosDeBaseDeDatos(id);
    res.json(usuario);
  } catch (error) {
    // Pasar el error al middleware de manejo de errores
    next(error);
  }
});

// Middleware de manejo de errores
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: err.message });
});

app.listen(3000);
```

## 5. Cadena de Middlewares para una Ruta

Ejemplo que muestra una cadena de middlewares aplicados a una ruta específica:

```javascript
const express = require('express');
const app = express();

// Middleware para validar parámetros
const validarParametros = (req, res, next) => {
  const id = parseInt(req.params.id);
  if (isNaN(id) || id <= 0) {
    return res.status(400).send('ID debe ser un número positivo');
  }
  // Modificar el objeto req para facilitar el uso posterior
  req.validatedId = id;
  next();
};

// Middleware para autenticación
const autenticar = (req, res, next) => {
  const token = req.headers.authorization;
  if (!token) {
    return res.status(401).send('Se requiere autenticación');
  }
  // Simular verificación de token
  if (token !== 'token-secreto') {
    return res.status(403).send('Token no válido');
  }
  next();
};

// Middleware para verificar permisos
const verificarPermisos = (req, res, next) => {
  // Supongamos que el token 'token-secreto' tiene permisos admin
  req.esAdmin = true;
  next();
};

// Aplicar cadena de middlewares a una ruta
app.get('/recurso/:id', 
  validarParametros,
  autenticar,
  verificarPermisos,
  (req, res) => {
    res.json({
      mensaje: 'Acceso concedido',
      recursoId: req.validatedId,
      esAdmin: req.esAdmin
    });
  }
);

app.listen(3000);
```

## 6. No llamar a next() o no enviar respuesta

Este ejemplo ilustra qué ocurre si no se llama a `next()` ni se envía una respuesta:

```javascript
const express = require('express');
const app = express();

// Middleware que procesa la solicitud correctamente
app.use((req, res, next) => {
  console.log('Middleware 1: Siempre se ejecuta');
  next();
});

// Middleware con condición que podría no continuar
app.use((req, res, next) => {
  console.log('Middleware 2: Verifica condición');
  
  // Si la URL tiene el parámetro "continuar", seguimos adelante
  if (req.query.continuar === 'true') {
    console.log('Continuando al siguiente middleware');
    next();
  } else {
    console.log('¡ADVERTENCIA! Ni se llama a next() ni se envía respuesta');
    // La solicitud quedará colgada indefinidamente aquí
    // El cliente esperará hasta que ocurra un timeout
  }
});

// Este middleware no se ejecutará si el anterior no llama a next()
app.use((req, res, next) => {
  console.log('Middleware 3: Generando respuesta');
  res.send('Respuesta generada con éxito');
});

// Solución: Implementar un timeout para detectar solicitudes colgadas
app.use((req, res, next) => {
  const timeout = setTimeout(() => {
    if (!res.headersSent) {
      console.error('Solicitud sin respuesta después de 10 segundos');
      res.status(500).send('Timeout del servidor');
    }
  }, 10000);
  
  // Limpiamos el timeout cuando la respuesta sea enviada
  res.on('finish', () => {
    clearTimeout(timeout);
  });
  
  next();
});

app.listen(3000);
```

## 7. Combinando distintos comportamientos de next()

Este ejemplo muestra varios comportamientos de `next()` en una aplicación completa:

```javascript
const express = require('express');
const app = express();

// Middleware de nivel de aplicación para todas las rutas
app.use(express.json());

// Middleware de registro
app.use((req, res, next) => {
  console.log(`Solicitud recibida: ${req.method} ${req.path}`);
  next();
});

// Middleware para verificar API key
app.use((req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  
  if (!apiKey) {
    return next(new Error('API key requerida'));
  }
  
  if (apiKey === 'clave-secreta') {
    req.usuario = { tipo: 'premium' };
  } else {
    req.usuario = { tipo: 'básico' };
  }
  
  next();
});

// Ruta con decisión de flujo usando next('route')
app.get('/contenido',
  (req, res, next) => {
    if (req.usuario.tipo === 'premium') {
      next(); // Continúa con el siguiente middleware en esta ruta
    } else {
      next('route'); // Salta a la siguiente definición de esta ruta
    }
  },
  (req, res) => {
    res.json({ tipo: 'premium', contenido: 'Contenido exclusivo' });
  }
);

// Ruta alternativa (se ejecuta cuando se llama a next('route'))
app.get('/contenido', (req, res) => {
  res.json({ tipo: 'básico', contenido: 'Contenido básico' });
});

// Ruta que podría generar error
app.get('/procesar/:datos', (req, res, next) => {
  try {
    const datos = req.params.datos;
    if (datos === 'error') {
      throw new Error('Error de procesamiento');
    }
    res.send(`Datos procesados: ${datos}`);
  } catch (error) {
    next(error); // Pasar al middleware de error
  }
});

// Middleware para manejar rutas no encontradas (se ejecuta si no hay coincidencia)
app.use((req, res, next) => {
  res.status(404).send('Ruta no encontrada');
});

// Middleware de manejo de errores (siempre al final)
app.use((err, req, res, next) => {
  console.error('Error:', err.message);
  res.status(500).send(`Ocurrió un error: ${err.message}`);
});

app.listen(3000, () => {
  console.log('Servidor iniciado en puerto 3000');
});
```

Estos ejemplos ilustran los diferentes casos de uso y comportamientos de la función `next()` en Express.js. Recuerda que siempre debes llamar a `next()` o enviar una respuesta con métodos como `res.send()` o `res.json()` para evitar que las solicitudes queden colgadas.