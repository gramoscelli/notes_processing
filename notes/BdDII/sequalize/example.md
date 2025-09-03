# Ejemplo: CRUD con Express y Sequelize CLI (Biblioteca)

## Primera parte: Modelo de Libros

### Paso 1: Iniciar el proyecto

```bash
# Crear el proyecto con Express generator
npx express-generator --no-view api-biblioteca
cd api-biblioteca

# Instalar dependencias
npm install
npm install sequelize mysql2 dotenv cors
npm install --save-dev sequelize-cli
```

### Paso 2: Inicializar Sequelize CLI

```bash
npx sequelize-cli init
```

### Paso 3: Configurar la conexión a la base de datos

Editar `config/config.json`:

```json
{
  "development": {
    "username": "gustavo",
    "password": "miclavesecreta",
    "database": "biblioteca_db",
    "host": "127.0.0.1",
    "dialect": "mysql"
  },
  "test": {
    "username": "gustavo",
    "password": "miclavesecreta",
    "database": "biblioteca_db_test",
    "host": "127.0.0.1",
    "dialect": "mysql"
  },
  "production": {
    "username": "gustavo",
    "password": "miclavesecreta",
    "database": "biblioteca_db_production",
    "host": "127.0.0.1",
    "dialect": "mysql"
  }
}
```

### Paso 4: Crear la base de datos

```bash
npx sequelize-cli db:create
```

### Paso 5: Crear el modelo Libro con migración

```bash
npx sequelize-cli model:generate --name Libro --attributes titulo:string,genero:string,anioPublicacion:integer,disponible:boolean
```

Editar la migración generada en `migrations/XXXX-create-libro.js` para personalizar campos:

```javascript
'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('Libros', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      titulo: {
        type: Sequelize.STRING(100),
        allowNull: false
      },
      genero: {
        type: Sequelize.STRING(50),
        allowNull: true
      },
      anioPublicacion: {
        type: Sequelize.INTEGER,
        allowNull: true
      },
      disponible: {
        type: Sequelize.BOOLEAN,
        defaultValue: true
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('Libros');
  }
};
```

### Paso 6: Ejecutar la migración

```bash
npx sequelize-cli db:migrate
```

### Paso 7: Crear semilla para libros

```bash
npx sequelize-cli seed:generate --name demo-libros
```

Editar la semilla en `seeders/XXXX-demo-libros.js`:

```javascript
'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {
    await queryInterface.bulkInsert('Libros', [
      {
        titulo: 'Don Quijote de la Mancha',
        genero: 'Novela',
        anioPublicacion: 1605,
        disponible: true,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        titulo: 'Cien años de soledad',
        genero: 'Realismo mágico',
        anioPublicacion: 1967,
        disponible: true,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        titulo: 'El principito',
        genero: 'Fábula',
        anioPublicacion: 1943,
        disponible: true,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ], {});
  },

  async down (queryInterface, Sequelize) {
    await queryInterface.bulkDelete('Libros', null, {});
  }
};
```

### Paso 8: Ejecutar la semilla

```bash
npx sequelize-cli db:seed:all
```

### Paso 9: Crear controlador para los libros

Crear directorio `controllers` y añadir `libroController.js`:

```javascript
const { Libro } = require('../models');

// Obtener todos los libros
exports.getAllLibros = async (req, res) => {
  try {
    const libros = await Libro.findAll();
    res.status(200).json(libros);
  } catch (error) {
    console.error('Error al obtener libros:', error);
    res.status(500).json({ message: 'Error al obtener libros' });
  }
};

// Obtener un libro por ID
exports.getLibroById = async (req, res) => {
  try {
    const libro = await Libro.findByPk(req.params.id);
    if (!libro) {
      return res.status(404).json({ message: 'Libro no encontrado' });
    }
    res.status(200).json(libro);
  } catch (error) {
    res.status(500).json({ message: 'Error al buscar el libro' });
  }
};

// Crear un nuevo libro
exports.createLibro = async (req, res) => {
  try {
    const libro = await Libro.create(req.body);
    res.status(201).json(libro);
  } catch (error) {
    res.status(400).json({ message: 'Error al crear el libro', error: error.message });
  }
};

// Actualizar un libro
exports.updateLibro = async (req, res) => {
  try {
    const [updated] = await Libro.update(req.body, {
      where: { id: req.params.id }
    });
    
    if (updated) {
      const updatedLibro = await Libro.findByPk(req.params.id);
      return res.status(200).json(updatedLibro);
    }
    
    throw new Error('Libro no encontrado');
  } catch (error) {
    res.status(500).json({ message: 'Error al actualizar libro', error: error.message });
  }
};

// Eliminar un libro
exports.deleteLibro = async (req, res) => {
  try {
    const deleted = await Libro.destroy({
      where: { id: req.params.id }
    });
    
    if (deleted) {
      return res.status(204).send();
    }
    
    throw new Error('Libro no encontrado');
  } catch (error) {
    res.status(500).json({ message: 'Error al eliminar libro', error: error.message });
  }
};
```

### Paso 10: Crear rutas para libros

Crear archivo `routes/librosRoutes.js`:

```javascript
const express = require('express');
const router = express.Router();
const libroController = require('../controllers/libroController');

// Rutas CRUD para libros
router.get('/', libroController.getAllLibros);
router.get('/:id', libroController.getLibroById);
router.post('/', libroController.createLibro);
router.put('/:id', libroController.updateLibro);
router.delete('/:id', libroController.deleteLibro);

module.exports = router;
```

### Paso 11: Actualizar app.js

```javascript
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const cors = require('cors');

// Importar rutas
const indexRouter = require('./routes/index');
const librosRouter = require('./routes/librosRoutes');

const app = express();

// Middleware
app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// Rutas
app.use('/', indexRouter);
app.use('/api/libros', librosRouter);

module.exports = app;
```

## Segunda parte: Extender con modelo Autor

### Paso 1: Crear modelo Autor con migración

```bash
npx sequelize-cli model:generate --name Autor --attributes nombre:string,nacionalidad:string,fechaNacimiento:dateonly
```

Editar la migración generada en `migrations/XXXX-create-autor.js`:

```javascript
'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('Autors', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      nombre: {
        type: Sequelize.STRING(100),
        allowNull: false
      },
      nacionalidad: {
        type: Sequelize.STRING(50),
        allowNull: true
      },
      fechaNacimiento: {
        type: Sequelize.DATEONLY,
        allowNull: true
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('Autors');
  }
};
```

### Paso 2: Crear migración para añadir autorId a libros

```bash
npx sequelize-cli migration:generate --name add-autor-id-to-libros
```

Editar la migración generada en `migrations/XXXX-add-autor-id-to-libros.js`:

```javascript
'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {
    await queryInterface.addColumn('Libros', 'autorId', {
      type: Sequelize.INTEGER,
      references: {
        model: 'Autors',
        key: 'id'
      },
      onUpdate: 'CASCADE',
      onDelete: 'SET NULL',
      allowNull: true
    });
  },

  async down (queryInterface, Sequelize) {
    await queryInterface.removeColumn('Libros', 'autorId');
  }
};
```

### Paso 3: Actualizar los modelos para agregar relaciones

Modificar `models/libro.js`:

```javascript
'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class Libro extends Model {
    static associate(models) {
      // Define la relación con Autor
      Libro.belongsTo(models.Autor, { foreignKey: 'autorId' });
    }
  }
  
  Libro.init({
    titulo: {
      type: DataTypes.STRING(100),
      allowNull: false
    },
    genero: DataTypes.STRING(50),
    anioPublicacion: DataTypes.INTEGER,
    disponible: {
      type: DataTypes.BOOLEAN,
      defaultValue: true
    },
    autorId: {
      type: DataTypes.INTEGER,
      allowNull: true
    }
  }, {
    sequelize,
    modelName: 'Libro',
  });
  
  return Libro;
};
```

Modificar `models/autor.js`:

```javascript
'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class Autor extends Model {
    static associate(models) {
      // Define la relación con Libro
      Autor.hasMany(models.Libro, { foreignKey: 'autorId' });
    }
  }
  
  Autor.init({
    nombre: {
      type: DataTypes.STRING(100),
      allowNull: false
    },
    nacionalidad: DataTypes.STRING(50),
    fechaNacimiento: DataTypes.DATEONLY
  }, {
    sequelize,
    modelName: 'Autor',
  });
  
  return Autor;
};
```

### Paso 4: Ejecutar las migraciones

```bash
npx sequelize-cli db:migrate
```

### Paso 5: Crear semilla para autores

```bash
npx sequelize-cli seed:generate --name demo-autores
```

Editar la semilla en `seeders/XXXX-demo-autores.js`:

```javascript
'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {
    await queryInterface.bulkInsert('Autors', [
      {
        nombre: 'Miguel de Cervantes',
        nacionalidad: 'Española',
        fechaNacimiento: '1547-09-29',
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        nombre: 'Gabriel García Márquez',
        nacionalidad: 'Colombiana',
        fechaNacimiento: '1927-03-06',
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        nombre: 'Antoine de Saint-Exupéry',
        nacionalidad: 'Francesa',
        fechaNacimiento: '1900-06-29',
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ], {});
  },

  async down (queryInterface, Sequelize) {
    await queryInterface.bulkDelete('Autors', null, {});
  }
};
```

### Paso 6: Crear semilla para actualizar libros con autores

```bash
npx sequelize-cli seed:generate --name update-libros-with-autores
```

Editar la semilla en `seeders/XXXX-update-libros-with-autores.js`:

```javascript
'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {
    // Obtener IDs de autores
    const [autores] = await queryInterface.sequelize.query(
      'SELECT id, nombre FROM Autors;'
    );
    
    // Utilizar una consulta directa para actualizar los libros con sus autores correspondientes
    if(autores && autores.length >= 3) {
      // Actualizar Don Quijote para relacionarlo con Cervantes
      await queryInterface.sequelize.query(
        'UPDATE Libros SET autorId = ? WHERE titulo LIKE ?',
        {
          replacements: [autores[0].id, 'Don Quijote%']
        }
      );
      
      // Actualizar Cien años para relacionarlo con García Márquez
      await queryInterface.sequelize.query(
        'UPDATE Libros SET autorId = ? WHERE titulo LIKE ?',
        {
          replacements: [autores[1].id, 'Cien años%']
        }
      );
      
      // Actualizar El principito para relacionarlo con Saint-Exupéry
      await queryInterface.sequelize.query(
        'UPDATE Libros SET autorId = ? WHERE titulo LIKE ?',
        {
          replacements: [autores[2].id, 'El principito%']
        }
      );
    }
  },

  async down (queryInterface, Sequelize) {
    // Eliminar las relaciones con autores
    await queryInterface.sequelize.query(
      'UPDATE Libros SET autorId = NULL'
    );
  }
};
```

### Paso 7: Ejecutar las semillas

```bash
npx sequelize-cli db:seed:all
```

### Paso 8: Crear controlador para autores

Crear archivo `controllers/autorController.js`:

```javascript
const { Autor, Libro } = require('../models');

// Obtener todos los autores
exports.getAllAutores = async (req, res) => {
  try {
    const autores = await Autor.findAll();
    res.status(200).json(autores);
  } catch (error) {
    res.status(500).json({ message: 'Error al obtener autores', error: error.message });
  }
};

// Obtener un autor por ID con sus libros
exports.getAutorById = async (req, res) => {
  try {
    const autor = await Autor.findByPk(req.params.id, {
      include: [{ model: Libro }] // Incluir libros asociados
    });
    
    if (!autor) {
      return res.status(404).json({ message: 'Autor no encontrado' });
    }
    
    res.status(200).json(autor);
  } catch (error) {
    res.status(500).json({ message: 'Error al buscar el autor', error: error.message });
  }
};

// Crear un nuevo autor
exports.createAutor = async (req, res) => {
  try {
    const autor = await Autor.create(req.body);
    res.status(201).json(autor);
  } catch (error) {
    res.status(400).json({ message: 'Error al crear el autor', error: error.message });
  }
};

// Actualizar un autor
exports.updateAutor = async (req, res) => {
  try {
    const [updated] = await Autor.update(req.body, {
      where: { id: req.params.id }
    });
    
    if (updated) {
      const updatedAutor = await Autor.findByPk(req.params.id);
      return res.status(200).json(updatedAutor);
    }
    
    throw new Error('Autor no encontrado');
  } catch (error) {
    res.status(500).json({ message: 'Error al actualizar autor', error: error.message });
  }
};

// Eliminar un autor
exports.deleteAutor = async (req, res) => {
  try {
    const deleted = await Autor.destroy({
      where: { id: req.params.id }
    });
    
    if (deleted) {
      return res.status(204).send();
    }
    
    throw new Error('Autor no encontrado');
  } catch (error) {
    res.status(500).json({ message: 'Error al eliminar autor', error: error.message });
  }
};
```

### Paso 9: Actualizar el controlador de libros para incluir autores

Actualizar `controllers/libroController.js`:

```javascript
const { Libro, Autor } = require('../models');

// Actualizar para incluir información del autor
exports.getAllLibros = async (req, res) => {
  try {
    const libros = await Libro.findAll({
      include: [{ model: Autor }]
    });
    res.status(200).json(libros);
  } catch (error) {
    console.error('Error al obtener libros:', error);
    res.status(500).json({ message: 'Error al obtener libros' });
  }
};

// Actualizar para incluir información del autor
exports.getLibroById = async (req, res) => {
  try {
    const libro = await Libro.findByPk(req.params.id, {
      include: [{ model: Autor }]
    });
    if (!libro) {
      return res.status(404).json({ message: 'Libro no encontrado' });
    }
    res.status(200).json(libro);
  } catch (error) {
    res.status(500).json({ message: 'Error al buscar el libro' });
  }
};

// El resto del controlador permanece igual
```

### Paso 10: Crear rutas para autores

Crear archivo `routes/autoresRoutes.js`:

```javascript
const express = require('express');
const router = express.Router();
const autorController = require('../controllers/autorController');

// Rutas CRUD para autores
router.get('/', autorController.getAllAutores);
router.get('/:id', autorController.getAutorById);
router.post('/', autorController.createAutor);
router.put('/:id', autorController.updateAutor);
router.delete('/:id', autorController.deleteAutor);

module.exports = router;
```

### Paso 11: Actualizar app.js para incluir las nuevas rutas

```javascript
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const cors = require('cors');

// Importar rutas
const indexRouter = require('./routes/index');
const librosRouter = require('./routes/librosRoutes');
const autoresRouter = require('./routes/autoresRoutes');

const app = express();

// Middleware
app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// Rutas
app.use('/', indexRouter);
app.use('/api/libros', librosRouter);
app.use('/api/autores', autoresRouter);

module.exports = app;
```

## Guía para los alumnos

### Pasos para ejecutar el proyecto

1. **Clonar o iniciar el proyecto**:
   ```bash
   # Si inicias desde cero:
   npx express-generator --no-view api-biblioteca
   cd api-biblioteca
   npm install
   npm install sequelize mysql2 dotenv cors
   npm install --save-dev sequelize-cli
   ```

2. **Configurar Sequelize**:
   ```bash
   npx sequelize-cli init
   ```

3. **Configurar la base de datos** (Editar `config/config.json`):
   ```json
   {
     "development": {
       "username": "gustavo",
       "password": "miclavesecreta",
       "database": "biblioteca_db",
       "host": "127.0.0.1",
       "dialect": "mysql"
     }
   }
   ```

4. **Crear la base de datos**:
   ```bash
   npx sequelize-cli db:create
   ```

5. **Ejecutar migraciones y semillas**:
   ```bash
   # Ejecutar migraciones
   npx sequelize-cli db:migrate
   
   # Ejecutar semillas
   npx sequelize-cli db:seed:all
   ```

6. **Iniciar el servidor**:
   ```bash
   npm start
   ```

### Endpoints disponibles

**Libros**:
- GET /api/libros - Obtener todos los libros (con información de autor)
- GET /api/libros/:id - Obtener un libro por ID (con información de autor)
- POST /api/libros - Crear nuevo libro
- PUT /api/libros/:id - Actualizar libro
- DELETE /api/libros/:id - Eliminar libro

**Autores**:
- GET /api/autores - Obtener todos los autores
- GET /api/autores/:id - Obtener un autor por ID (incluye sus libros)
- POST /api/autores - Crear nuevo autor
- PUT /api/autores/:id - Actualizar autor
- DELETE /api/autores/:id - Eliminar autor

### Comandos útiles de Sequelize CLI

```bash
# Crear un nuevo modelo
npx sequelize-cli model:generate --name NombreModelo --attributes campo1:tipo,campo2:tipo

# Crear una migración
npx sequelize-cli migration:generate --name nombre-migracion

# Deshacer última migración
npx sequelize-cli db:migrate:undo

# Crear una semilla
npx sequelize-cli seed:generate --name nombre-semilla
```
