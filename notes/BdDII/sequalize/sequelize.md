# Sequelize: ORM para bases de datos relacionales

## Introducción a ORM

Un **ORM (Object-Relational Mapping)** es una técnica de programación que permite convertir datos entre sistemas de tipos incompatibles en lenguajes de programación orientados a objetos. En términos simples, un ORM permite a los desarrolladores trabajar con bases de datos relacionales utilizando objetos de programación, eliminando la necesidad de escribir consultas SQL directamente.

[Documentación oficial de Sequelize versión 6](https://sequelize.org/docs/v6/)

### Ventajas de usar un ORM:

- **Abstracción de la base de datos**: Permite cambiar el motor de base de datos con cambios mínimos en el código.
- **Seguridad**: Ayuda a prevenir ataques de inyección SQL.
- **Productividad**: Reduce el código repetitivo y acelera el desarrollo.
- **Mantenibilidad**: El código es más limpio y fácil de mantener.
- **Mapeo de objetos**: Conversión automática entre tipos de datos de la base de datos y del lenguaje de programación.

### Desventajas:

- **Rendimiento**: Puede ser menos eficiente que SQL optimizado manualmente.
- **Curva de aprendizaje**: Requiere tiempo para dominar el ORM específico.
- **Complejidad**: Algunas consultas complejas pueden ser difíciles de expresar a través del ORM.

## Sequelize: ORM para Node.js

**Sequelize** es un ORM basado en promesas para Node.js que soporta PostgreSQL, MySQL, SQLite y MSSQL. Proporciona una abstracción sólida de la base de datos y facilita tareas comunes como la migración de esquemas y la validación de datos.

### Instalación

```bash
# Instalación básica
npm install sequelize

# Instalar el driver para la base de datos
npm install pg pg-hstore # PostgreSQL
npm install mysql2       # MySQL
npm install sqlite3      # SQLite
npm install tedious      # Microsoft SQL Server
```

### Conexión a Bases de Datos Específicas

### Conexión a MySQL

MySQL es uno de los sistemas de gestión de bases de datos relacionales más populares. Para conectarse a una base de datos MySQL con Sequelize, debes seguir estos pasos:

1. **Instalar los paquetes necesarios**:

```bash
npm install sequelize mysql2
```

2. **Configurar la conexión**:

```javascript
const { Sequelize } = require('sequelize');

// Opción 1: Parámetros separados
const sequelize = new Sequelize('nombre_db', 'usuario', 'contraseña', {
  host: 'localhost',
  dialect: 'mysql',
  port: 3306, // Puerto por defecto de MySQL
  pool: {
    max: 5,       // Máximo número de conexiones en el pool
    min: 0,       // Mínimo número de conexiones en el pool
    acquire: 30000, // Tiempo máximo (ms) para adquirir una conexión
    idle: 10000   // Tiempo máximo (ms) que una conexión puede estar inactiva
  },
  timezone: '+00:00' // Establecer zona horaria UTC (ajustar según necesidades)
});

// Opción 2: URI de conexión
const sequelize = new Sequelize('mysql://usuario:contraseña@localhost:3306/nombre_db');
```

3. **Verificar la conexión**:

```javascript
async function testMySQLConnection() {
  try {
    await sequelize.authenticate();
    console.log('Conexión a MySQL establecida correctamente.');
  } catch (error) {
    console.error('Error al conectar con MySQL:', error);
  }
}

testMySQLConnection();
```

4. **Opciones específicas para MySQL**:

```javascript
const sequelize = new Sequelize('nombre_db', 'usuario', 'contraseña', {
  host: 'localhost',
  dialect: 'mysql',
  dialectOptions: {
    charset: 'utf8mb4', // Soporte para caracteres especiales y emojis
    collate: 'utf8mb4_unicode_ci',
    // Para conexiones SSL:
    ssl: {
      key: fs.readFileSync('./client-key.pem'),
      cert: fs.readFileSync('./client-cert.pem'),
      ca: fs.readFileSync('./ca-cert.pem'),
      rejectUnauthorized: false
    },
    // Opciones para consultas
    multipleStatements: true, // Permitir múltiples consultas en una sola sentencia
  }
});
```

### Conexión a SQLite

SQLite es una base de datos SQL contenida en un único archivo, lo que la hace ideal para desarrollo, pruebas o aplicaciones pequeñas. Para usar SQLite con Sequelize:

1. **Instalar los paquetes necesarios**:

```bash
npm install sequelize sqlite3
```

2. **Configurar la conexión**:

```javascript
const { Sequelize } = require('sequelize');
const path = require('path');

// Opción 1: Conexión a un archivo SQLite
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: path.join(__dirname, 'database.sqlite'), // Ruta al archivo
  logging: console.log, // Opcional: para ver las consultas SQL
});

// Opción 2: SQLite en memoria (útil para pruebas)
const sequelizeMemory = new Sequelize('sqlite::memory:');
```

3. **Verificar la conexión**:

```javascript
async function testSQLiteConnection() {
  try {
    await sequelize.authenticate();
    console.log('Conexión a SQLite establecida correctamente.');
  } catch (error) {
    console.error('Error al conectar con SQLite:', error);
  }
}

testSQLiteConnection();
```

4. **Opciones adicionales para SQLite**:

```javascript
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './database.sqlite',
  dialectOptions: {
    // Opciones específicas para SQLite
    mode: sqlite3.OPEN_READWRITE | sqlite3.OPEN_CREATE, // Modo de apertura
    timeout: 30000, // Tiempo de espera en ms para operaciones ocupadas
  }
});
```

### Prácticas Recomendadas para Conexiones a Bases de Datos

1. **Variables de entorno**: Almacena las credenciales de conexión en variables de entorno y no en el código.

```javascript
// Usando dotenv para cargar variables de entorno desde un archivo .env
require('dotenv').config();

const sequelize = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASSWORD,
  {
    host: process.env.DB_HOST,
    dialect: process.env.DB_DIALECT // 'mysql' o 'sqlite'
  }
);
```

2. **Conexiones por entorno**: Configura conexiones diferentes según el entorno (desarrollo, pruebas, producción).

```javascript
const env = process.env.NODE_ENV || 'development';
const config = {
  development: {
    dialect: 'sqlite',
    storage: './dev-database.sqlite'
  },
  test: {
    dialect: 'sqlite',
    storage: ':memory:'
  },
  production: {
    dialect: 'mysql',
    host: process.env.DB_HOST,
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
  }
};

const sequelize = new Sequelize(config[env]);
```

3. **Manejo del pool de conexiones**: Ajusta el pool de conexiones según las necesidades de tu aplicación.

```javascript
// Para aplicaciones con alta carga (solo relevante para MySQL, no para SQLite)
const sequelize = new Sequelize('nombre_db', 'usuario', 'contraseña', {
  dialect: 'mysql',
  pool: {
    max: 20, // Más conexiones para aplicaciones con mucho tráfico
    min: 5,  // Mantener al menos 5 conexiones abiertas
    acquire: 60000, // Tiempo más largo para adquirir conexión
    idle: 30000 // Más tiempo antes de cerrar conexiones inactivas
  }
});
```

4. **Registro (logging)**: Configura el nivel de registro según tus necesidades.

```javascript
// Registrar todas las consultas (desarrollo)
const sequelize = new Sequelize('db', 'user', 'pass', {
  dialect: 'mysql',
  logging: console.log // o logging: true
});

// Registrar consultas lentas (producción)
const sequelize = new Sequelize('db', 'user', 'pass', {
  dialect: 'mysql',
  logging: (sql, timing) => {
    if (timing && timing > 1000) { // Solo registrar consultas que tomen más de 1 segundo
      console.warn(`Consulta lenta (${timing}ms):`, sql);
    }
  },
  benchmark: true // Habilitar medición de tiempo
});

// Desactivar registro (producción)
const sequelize = new Sequelize('db', 'user', 'pass', {
  dialect: 'mysql',
  logging: false
});
```

Estas configuraciones te permitirán conectarte eficientemente a bases de datos MySQL y SQLite con Sequelize, ajustando los parámetros según tus necesidades específicas.

## Definición de Modelos

Los modelos en Sequelize representan tablas en la base de datos. 

```javascript
const { Sequelize, DataTypes } = require('sequelize');
const sequelize = new Sequelize(/* ... */);

// Definición de un modelo User
const User = sequelize.define('User', {
  // Definición de atributos
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true
  },
  firstName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  lastName: {
    type: DataTypes.STRING
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  age: {
    type: DataTypes.INTEGER,
    validate: {
      min: 0
    }
  },
  isActive: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  }
}, {
  // Opciones del modelo
  timestamps: true,      // Añade createdAt y updatedAt
  tableName: 'usuarios', // Nombre personalizado para la tabla
  paranoid: true         // Soft delete (añade deletedAt)
});
```

### Tipos de Datos Comunes

Sequelize proporciona varios tipos de datos que corresponden a los tipos de datos de las bases de datos:

- `DataTypes.STRING`: VARCHAR(255)
- `DataTypes.TEXT`: TEXT
- `DataTypes.INTEGER`: INTEGER
- `DataTypes.FLOAT`: FLOAT
- `DataTypes.BOOLEAN`: BOOLEAN/TINYINT
- `DataTypes.DATE`: DATETIME
- `DataTypes.DATEONLY`: DATE
- `DataTypes.UUID`: UUID
- `DataTypes.JSON`: JSON (PostgreSQL, MySQL)
- `DataTypes.ARRAY`: ARRAY (PostgreSQL)

## Sincronización con la Base de Datos

Una vez definidos los modelos, es necesario sincronizarlos con la base de datos:

```javascript
// Sincronizar todos los modelos
// force: true -> Elimina y recrea las tablas (¡cuidado en producción!)
sequelize.sync({ force: false })
  .then(() => {
    console.log('Modelos sincronizados con la base de datos');
  });

// Sincronizar un modelo específico
User.sync({ alter: true }) // alter: true -> Actualiza la tabla si existe
  .then(() => {
    console.log('Modelo User sincronizado');
  });
```

## Relaciones entre Modelos

Sequelize soporta los tipos estándar de asociaciones. Estas relaciones son fundamentales para modelar correctamente la estructura de datos.

![Diagrama entidad-relación de una aplicación compleja](E-r_Diagram.jpg)

### One-To-One (Uno a Uno)

Una relación uno a uno significa que un registro en la tabla A tiene exactamente un registro correspondiente en la tabla B.

```javascript
const User = sequelize.define('User', { /* ... */ });
const Profile = sequelize.define('Profile', { /* ... */ });

// Un usuario tiene un perfil
User.hasOne(Profile);
// Un perfil pertenece a un usuario
Profile.belongsTo(User);
```

En la base de datos, esto típicamente se implementa añadiendo una clave foránea `UserId` en la tabla `Profiles`.

[Más sobre relaciones de uno-a-uno](https://siddharth-lakhara.medium.com/understanding-sequelize-associations-part-1-one-to-one-1-1-mapping-897ce176caf9)

### One-To-Many (Uno a Muchos)

Una relación uno a muchos significa que un registro en la tabla A puede tener múltiples registros correspondientes en la tabla B.

```javascript
const User = sequelize.define('User', { /* ... */ });
const Post = sequelize.define('Post', { /* ... */ });

// Un usuario tiene muchos posts
User.hasMany(Post);
// Un post pertenece a un usuario
Post.belongsTo(User);
```
En la base de datos, esto se implementa añadiendo una clave foránea `UserId` en la tabla `Posts`.

[Más sobre relaciones de uno-a-muchos](https://siddharth-lakhara.medium.com/understanding-sequelize-associations-part-2-one-to-many-1-n-mapping-10a7d7929a5b)

### Many-To-Many (Muchos a Muchos)

Una relación muchos a muchos significa que un registro en la tabla A puede tener múltiples registros correspondientes en la tabla B, y viceversa.

```javascript
const Student = sequelize.define('Student', { /* ... */ });
const Course = sequelize.define('Course', { /* ... */ });

// Un estudiante puede estar en muchos cursos
Student.belongsToMany(Course, { through: 'StudentCourses' });
// Un curso puede tener muchos estudiantes
Course.belongsToMany(Student, { through: 'StudentCourses' });
```

En la base de datos, esto se implementa creando una tabla de unión (`StudentCourses`) que contiene claves foráneas para ambas tablas (`StudentId` y `CourseId`).

[Más sobre relaciones muchos-a-muchos](https://siddharth-lakhara.medium.com/understanding-sequelize-associations-part-3-many-to-many-n-m-mapping-3e7dcdeb78db)
### Opciones Avanzadas para Relaciones

#### Personalización de Claves Foráneas

```javascript
User.hasMany(Post, {
  foreignKey: 'autorId', // Nombre personalizado para la clave foránea
  as: 'articulos'        // Alias para la relación
});

Post.belongsTo(User, {
  foreignKey: 'autorId',
  as: 'autor'
});
```

#### Relaciones con Scope

```javascript
// Todos los comentarios donde approved = true
Post.hasMany(Comment, {
  foreignKey: 'postId',
  scope: {
    approved: true
  },
  as: 'approvedComments'
});
```

#### Eliminación en Cascada

```javascript
User.hasMany(Post, {
  onDelete: 'CASCADE',  // Eliminar posts cuando se elimina el usuario
  onUpdate: 'CASCADE'   // Actualizar posts cuando se actualiza el usuario
});
```

## Operaciones CRUD

### Create (Crear)

```javascript
// Crear un registro
async function createUser() {
  try {
    const jane = await User.create({
      firstName: 'Jane',
      lastName: 'Doe',
      email: 'jane.doe@example.com',
      age: 25
    });
    console.log('Usuario creado:', jane.toJSON());
  } catch (error) {
    console.error('Error al crear usuario:', error);
  }
}
```

### Read (Leer)

```javascript
// Encontrar todos los registros
async function findAllUsers() {
  const users = await User.findAll();
  console.log('Todos los usuarios:', JSON.stringify(users, null, 2));
}

// Encontrar un registro por ID
async function findUserById(id) {
  const user = await User.findByPk(id);
  if (user) {
    console.log('Usuario encontrado:', user.toJSON());
  } else {
    console.log('Usuario no encontrado');
  }
}

// Encontrar registros con condiciones
async function findUsersByCondition() {
  const users = await User.findAll({
    where: {
      lastName: 'Doe',
      age: {
        [Op.gte]: 18 // Operador mayor o igual que
      }
    },
    attributes: ['id', 'firstName', 'email'], // Seleccionar solo ciertos campos
    order: [['createdAt', 'DESC']], // Ordenar por fecha de creación descendente
    limit: 10, // Limitar a 10 resultados
    offset: 0  // Comenzar desde el primer resultado
  });
}
```

### Update (Actualizar)

```javascript
// Actualizar un registro
async function updateUser(id) {
  const [updatedRows] = await User.update(
    { lastName: 'Smith', age: 26 },
    { where: { id } }
  );
  console.log(`${updatedRows} filas actualizadas`);
}

// Actualizar o crear un registro
async function upsertUser(data) {
  const [user, created] = await User.upsert(data);
  console.log(created ? 'Usuario creado' : 'Usuario actualizado');
}
```

### Delete (Eliminar)

```javascript
// Eliminar registros
async function deleteUser(id) {
  const deleted = await User.destroy({
    where: { id }
  });
  console.log(`${deleted} usuarios eliminados`);
}

// Restaurar registros eliminados (con paranoid: true)
async function restoreUser(id) {
  await User.restore({
    where: { id }
  });
}
```

## Consultas Avanzadas

Sequelize permite realizar consultas complejas con operadores y funciones:

```javascript
const { Op } = require('sequelize');

// Consulta con operadores
async function advancedQuery() {
  const users = await User.findAll({
    where: {
      [Op.or]: [
        { age: { [Op.lt]: 18 } }, // age < 18
        { age: { [Op.gt]: 65 } }  // age > 65
      ],
      [Op.and]: [
        { isActive: true },
        { email: { [Op.like]: '%@example.com' } }
      ]
    }
  });
}
```

### Operadores Comunes

- `Op.eq`: Igual a
- `Op.ne`: No igual a
- `Op.gt`: Mayor que
- `Op.gte`: Mayor o igual que
- `Op.lt`: Menor que
- `Op.lte`: Menor o igual que
- `Op.in`: En una lista
- `Op.notIn`: No en una lista
- `Op.like`: Como (con comodines)
- `Op.notLike`: No como
- `Op.between`: Entre dos valores
- `Op.notBetween`: No entre dos valores
- `Op.and`: Y lógico
- `Op.or`: O lógico
- `Op.not`: Negación lógica

## Transacciones

Las transacciones garantizan que una serie de operaciones se completen con éxito o se reviertan todas:

```javascript
async function transferMoney(fromAccountId, toAccountId, amount) {
  // Iniciar transacción
  const t = await sequelize.transaction();

  try {
    // Realizar operaciones dentro de la transacción
    await Account.decrement('balance', {
      by: amount,
      where: { id: fromAccountId },
      transaction: t
    });

    await Account.increment('balance', {
      by: amount,
      where: { id: toAccountId },
      transaction: t
    });

    // Confirmar transacción
    await t.commit();
    console.log('Transferencia completada con éxito');
  } catch (error) {
    // Revertir transacción en caso de error
    await t.rollback();
    console.error('Error en la transferencia:', error);
  }
}
```

## Hooks (Ganchos)

Los hooks permiten ejecutar funciones en determinados momentos del ciclo de vida de los modelos:

![Ciclo de vida de los hooks de Sequalize](lifecicle.png)

En el diagrama anterior se muestra el flujo de ejecución de los hooks durante el ciclo de vida de un modelo. Cada operación (create, update, delete) pasa por una serie de hooks que se ejecutan en un orden específico.





### Implementación de Hooks

```javascript
const User = sequelize.define('User', {
  // ...atributos
}, {
  hooks: {
    beforeCreate: (user) => {
      // Hash de contraseña antes de crear
      if (user.password) {
        user.password = bcrypt.hashSync(user.password, 10);
      }
    },
    afterCreate: (user) => {
      console.log(`Nuevo usuario creado: ${user.firstName}`);
    },
    beforeUpdate: (user) => {
      // Lógica antes de actualizar
    },
    afterDestroy: (user) => {
      // Lógica después de eliminar
    }
  }
});
```
### Casos de uso comunes para hooks

1. **Encriptación de contraseñas**: Encriptar contraseñas antes de guardarlas
2. **Normalización de datos**: Formatear datos (por ejemplo, convertir emails a minúsculas)
3. **Generación de slugs**: Crear slugs para URLs amigables
4. **Registro de cambios**: Mantener un historial de cambios
5. **Notificaciones**: Enviar notificaciones después de ciertas operaciones
6. **Validación compleja**: Realizar validaciones que no se pueden expresar con los validadores estándar

## Migraciones

Las migraciones permiten controlar los cambios en el esquema de la base de datos de manera ordenada y versionada.

### Estructura de un Archivo de Migración

```javascript
'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('Users', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      firstName: {
        type: Sequelize.STRING,
        allowNull: false
      },
      lastName: {
        type: Sequelize.STRING
      },
      email: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true
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

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('Users');
  }
};
```

### Ejecutar Migraciones

```bash
# Aplicar todas las migraciones pendientes
npx sequelize-cli db:migrate

# Revertir la última migración
npx sequelize-cli db:migrate:undo

# Revertir todas las migraciones
npx sequelize-cli db:migrate:undo:all

# Revertir hasta una migración específica
npx sequelize-cli db:migrate:undo:all --to XXXXXXXXXXXXXX-create-users.js
```

### Operaciones Comunes en Migraciones

1. **Crear tabla**:
```javascript
await queryInterface.createTable('TableName', {
  // definición de columnas
});
```

2. **Modificar tabla**:
```javascript
// Añadir columna
await queryInterface.addColumn('Users', 'phoneNumber', {
  type: Sequelize.STRING
});

// Eliminar columna
await queryInterface.removeColumn('Users', 'phoneNumber');

// Cambiar tipo de columna
await queryInterface.changeColumn('Users', 'email', {
  type: Sequelize.STRING(100),
  allowNull: false,
  unique: true
});
```

3. **Añadir índices**:
```javascript
await queryInterface.addIndex('Users', ['email', 'username']);
```

4. **Crear restricciones**:
```javascript
// Añadir clave foránea
await queryInterface.addConstraint('Posts', {
  fields: ['userId'],
  type: 'foreign key',
  name: 'fk_posts_user',
  references: {
    table: 'Users',
    field: 'id'
  },
  onDelete: 'cascade',
  onUpdate: 'cascade'
});
```

### Semillas (Seeds)

Las semillas permiten poblar la base de datos con datos iniciales o de prueba. Ejemplo de un archivo en la carpeta `seeders/`:
```javascript
'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.bulkInsert('Users', [
      {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@example.com',
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        firstName: 'Jane',
        lastName: 'Doe',
        email: 'jane@example.com',
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ]);
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.bulkDelete('Users', null, {});
  }
};
```

Para ejecutar las semillas:
```bash
# Ejecutar todas las semillas
npx sequelize-cli db:seed:all

# Revertir todas las semillas
npx sequelize-cli db:seed:undo:all
```


## Arquitectura de una Aplicación con Sequelize

Una arquitectura bien diseñada es fundamental para construir aplicaciones escalables y mantenibles con Sequelize. A continuación se muestra cómo se estructura típicamente una aplicación con Sequelize siguiendo patrones MVC (Modelo-Vista-Controlador).

### Estructura de Carpetas Recomendada

La siguiente estructura de carpetas es una forma organizada de implementar Sequelize en una aplicación Express:

```
proyecto/
├── config/                  # Configuraciones
│   ├── database.js          # Configuración de la base de datos
│   └── config.json          # Configuraciones por entorno
├── migrations/              # Migraciones de la base de datos
├── models/                  # Definición de modelos
│   ├── index.js             # Exporta todos los modelos
│   ├── user.js              # Modelo de Usuario
│   └── product.js           # Modelo de Producto
├── seeders/                 # Datos iniciales (semillas)
├── controllers/             # Controladores de la aplicación
│   ├── userController.js    # Controlador para usuarios
│   └── productController.js # Controlador para productos
├── routes/                  # Rutas de la API
│   ├── userRoutes.js        # Rutas para usuarios
│   └── productRoutes.js     # Rutas para productos
├── middlewares/             # Middlewares personalizados
├── services/                # Lógica de negocio
├── utils/                   # Utilidades
└── app.js                   # Punto de entrada
```
## Generación de Código con Sequelize CLI

Sequelize ofrece herramientas para generar automáticamente código a través de su CLI. Esta funcionalidad puede mejorar significativamente la productividad del desarrollador.

### Instalación de Sequelize CLI

```bash
# Instalación global
npm install -g sequelize-cli

# Instalación local (recomendada)
npm install --save-dev sequelize-cli
```

### Generación de Modelos y Migraciones

Sequelize CLI permite generar un modelo junto con su migración correspondiente en un solo comando:

```bash
# Generar modelo y migración
npx sequelize-cli model:generate --name User --attributes firstName:string,lastName:string,email:string

```

Este comando creará:

1. Un archivo de modelo en `models/user.js`
2. Un archivo de migración en `migrations/XXXXXXXXXXXXXX-create-user.js`

La migración incluirá automáticamente los campos especificados en `--attributes`, además de `id`, `createdAt` y `updatedAt`.

### Generación de Seeders
Sequelize CLI proporciona un comando simple para generar un nuevo archivo seeder:

```bash
# Generar un seeder
npx sequelize-cli seed:generate --name demo-users

```

Este comando crea un nuevo archivo JavaScript en la carpeta `seeders/` del proyecto. El nombre del archivo tendrá el formato:
`YYYYMMDDHHMMSS-demo-users.js` (donde YYYYMMDDHHMMSS es la fecha y hora de creación).

Por ejemplo: `20250514123456-demo-users.js`

### Estructura del Archivo Generado

Al ejecutar el comando, Sequelize generará un archivo con esta estructura básica:

```javascript
'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    /**
     * Add seed commands here.
     *
     * Example:
     * await queryInterface.bulkInsert('People', [{
     *   name: 'John Doe',
     *   isBetaMember: false
     * }], {});
    */
  },

  down: async (queryInterface, Sequelize) => {
    /**
     * Add commands to revert seed here.
     *
     * Example:
     * await queryInterface.bulkDelete('People', null, {});
     */
  }
};
```

Este archivo contiene dos funciones principales:

1. **up**: Contiene el código para añadir datos a la base de datos.
2. **down**: Contiene el código para revertir los cambios (eliminar los datos añadidos).

### Completando el Seeder

Para que el seeder funcione, debes editar el archivo para incluir tus propios datos. Un ejemplo completo sería:

```javascript
'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.bulkInsert('Users', [
      {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@example.com',
        role: 'user',
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        firstName: 'Jane',
        lastName: 'Smith',
        email: 'jane@example.com',
        role: 'user',
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        firstName: 'Admin',
        lastName: 'User',
        email: 'admin@example.com',
        role: 'admin',
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ]);
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.bulkDelete('Users', null, {});
  }
};
```


### Configuración en package.json

Para facilitar el uso, podemos añadir estos scripts a nuestro `package.json`:

```json
{
  "scripts": {
    "migrate": "sequelize-cli db:migrate",
    "migrate:undo": "sequelize-cli db:migrate:undo",
    "seed": "sequelize-cli db:seed:all",
    "seed:undo": "sequelize-cli db:seed:undo:all"
  }
}
```

### Herramientas de Terceros

También existen paquetes de terceros que facilitan la generación de código con Sequelize:

1. **sequelize-auto**: Genera modelos a partir de una base de datos existente.
   ```bash
   npm install -g sequelize-auto
   sequelize-auto -h localhost -d database -u username -p password -x port
   ```

2. **sequelize-mig**: Genera migraciones a partir de cambios en los modelos.
   ```bash
   npm install -g sequelize-mig
   sequelize-mig migration:make -n "create-users"
   ```

Estas herramientas pueden ayudar a generar rápidamente código boilerplate y enfocarse en la lógica de negocio.

## Flujo de Datos

El siguiente diagrama ilustra el flujo de datos en una aplicación que utiliza Sequelize:

![Flujo de datos en una aplicación con Sequelize](data_flow.png)

## Patrones de Diseño Comunes

1. **Repositorio**: Encapsula la lógica de acceso a datos

```javascript
// repositories/userRepository.js
class UserRepository {
  async findAll(options = {}) {
    return User.findAll(options);
  }
  
  async findById(id) {
    return User.findByPk(id);
  }
  
  async create(data) {
    return User.create(data);
  }
  
  // Más métodos...
}
```

2. **Servicio**: Contiene la lógica de negocio

```javascript
// services/userService.js
class UserService {
  constructor(userRepository) {
    this.userRepository = userRepository;
  }
  
  async registerUser(userData) {
    // Validaciones, reglas de negocio...
    return this.userRepository.create(userData);
  }
  
  // Más métodos...
}
```

## Buenas Prácticas

1. **Utiliza migraciones**: Para mantener un control de versiones del esquema de la base de datos.
2. **Modulariza tus modelos**: Cada modelo en su propio archivo.
3. **Valida datos**: Aprovecha las validaciones de Sequelize.
4. **Usa transacciones**: Para operaciones que afectan a múltiples registros.
5. **Maneja errores**: Captura y maneja adecuadamente los errores.
6. **Evita consultas N+1**: Utiliza eager loading (include) para cargar relaciones.
7. **Limita consultas**: Utiliza limit, offset y scopes para consultas eficientes.
8. **Seguridad**: Nunca confíes en la entrada del usuario sin validación.
9. **Testing**: Prueba tus modelos y consultas.
10. **Documentación**: Documenta tus modelos y sus relaciones.

## Implementación en una Aplicación Express

A continuación, veremos cómo implementar Sequelize en una aplicación Express utilizando una estructura de carpetas organizada. Transformaremos el ejemplo del modelo `Client` en memoria a un modelo Sequelize para usar en una API REST.

### Configuración de la Base de Datos (config/database.js)

```javascript
// config/database.js
const { Sequelize } = require('sequelize');

const env = process.env.NODE_ENV || 'development';
const config = {
  development: {
    database: 'db_development',
    username: 'root',
    password: '',
    host: 'localhost',
    dialect: 'mysql',
    logging: console.log
  },
  test: {
    database: 'db_test',
    username: 'root',
    password: '',
    host: 'localhost',
    dialect: 'mysql',
    logging: false
  },
  production: {
    database: process.env.DB_NAME,
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    host: process.env.DB_HOST,
    dialect: 'mysql',
    logging: false,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
};

const sequelize = new Sequelize(
  config[env].database,
  config[env].username,
  config[env].password,
  config[env]
);

module.exports = sequelize;
```

### Modelo de Cliente (models/client.js)

```javascript
// models/client.js
const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Client = sequelize.define('Client', {
  // Definimos los campos de la tabla
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  nombre: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: {
        msg: 'El nombre no puede estar vacío'
      }
    }
  },
  apellido: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: {
        msg: 'El apellido no puede estar vacío'
      }
    }
  },
  dni: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: {
      msg: 'El DNI ya está registrado'
    },
    validate: {
      notEmpty: {
        msg: 'El DNI no puede estar vacío'
      },
      isNumeric: {
        msg: 'El DNI debe contener solo números'
      }
    }
  }
}, {
  tableName: 'clients',
  timestamps: true // Añade createdAt y updatedAt
});

// Métodos estáticos personalizados (similar al mock original)
Client.createClient = async function(nombre, apellido, dni) {
  try {
    const client = await this.create({ nombre, apellido, dni });
    return client;
  } catch (error) {
    throw error;
  }
};

Client.updateClient = async function(id, nombre, apellido, dni) {
  try {
    const client = await this.findByPk(id);
    if (!client) {
      throw new Error('Error: el id no existe');
    }
    
    return await client.update({ nombre, apellido, dni });
  } catch (error) {
    throw error;
  }
};

Client.deleteClient = async function(id) {
  try {
    const client = await this.findByPk(id);
    if (!client) {
      throw new Error('Error: el id no existe');
    }
    return await client.destroy();
  } catch (error) {
    throw error;
  }
};

Client.listClients = async function() {
  try {
    const clients = await this.findAll();
    return clients.map(client => `${client.apellido}, ${client.nombre}`);
  } catch (error) {
    throw error;
  }
};

module.exports = Client;
```

### Índice de Modelos (models/index.js)

```javascript
// models/index.js
const sequelize = require('../config/database');
const Client = require('./client');

// Agregar otros modelos aquí...
// const OtroModelo = require('./otroModelo');

// Definir relaciones entre modelos
// Client.hasMany(OtroModelo);
// OtroModelo.belongsTo(Client);

const db = {
  sequelize,
  Client
  // Agregar otros modelos aquí
};

module.exports = db;
```

### Controlador de Clientes (controllers/clientController.js)

```javascript
// controllers/clientController.js
const { Client } = require('../models');

// Obtener todos los clientes
exports.getAllClients = async (req, res) => {
  try {
    const clients = await Client.findAll();
    res.status(200).json(clients);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Obtener un cliente por ID
exports.getClientById = async (req, res) => {
  try {
    const client = await Client.findByPk(req.params.id);
    if (!client) {
      return res.status(404).json({ message: 'Cliente no encontrado' });
    }
    res.status(200).json(client);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Crear un nuevo cliente
exports.createClient = async (req, res) => {
  try {
    const { nombre, apellido, dni } = req.body;
    const client = await Client.createClient(nombre, apellido, dni);
    res.status(201).json(client);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

// Actualizar un cliente
exports.updateClient = async (req, res) => {
  try {
    const { nombre, apellido, dni } = req.body;
    const client = await Client.updateClient(req.params.id, nombre, apellido, dni);
    res.status(200).json(client);
  } catch (error) {
    if (error.message === 'Error: el id no existe') {
      return res.status(404).json({ message: 'Cliente no encontrado' });
    }
    res.status(400).json({ message: error.message });
  }
};

// Eliminar un cliente
exports.deleteClient = async (req, res) => {
  try {
    await Client.deleteClient(req.params.id);
    res.status(204).send();
  } catch (error) {
    if (error.message === 'Error: el id no existe') {
      return res.status(404).json({ message: 'Cliente no encontrado' });
    }
    res.status(500).json({ message: error.message });
  }
};

// Obtener lista formateada de clientes
exports.getClientList = async (req, res) => {
  try {
    const clientList = await Client.listClients();
    res.status(200).json(clientList);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
```

### Rutas para Clientes (routes/clientRoutes.js)

```javascript
// routes/clientRoutes.js
const express = require('express');
const router = express.Router();
const clientController = require('../controllers/clientController');

// Definir rutas
router.get('/', clientController.getAllClients);
router.get('/list', clientController.getClientList);
router.get('/:id', clientController.getClientById);
router.post('/', clientController.createClient);
router.put('/:id', clientController.updateClient);
router.delete('/:id', clientController.deleteClient);

module.exports = router;
```

### Aplicación Express (app.js)

```javascript
// app.js
const express = require('express');
const { sequelize } = require('./models');
const clientRoutes = require('./routes/clientRoutes');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Rutas
app.use('/api/clients', clientRoutes);

// Sincronizar modelos con la base de datos
sequelize.sync({ force: false })
  .then(() => {
    console.log('Base de datos sincronizada');
    app.listen(PORT, () => {
      console.log(`Servidor corriendo en el puerto ${PORT}`);
    });
  })
  .catch(error => {
    console.error('Error al sincronizar la base de datos:', error);
  });
```

Este ejemplo muestra cómo transformar el modelo `Client` en memoria a un modelo Sequelize para usar en una aplicación Express. Hemos mantenido la funcionalidad del mock original (create, update, delete, list) pero implementándolo con Sequelize.

Los métodos estáticos personalizados (`createClient`, `updateClient`, `deleteClient`, `listClients`) proporcionan una interfaz similar al mock original, pero ahora usando la base de datos relacional a través de Sequelize.

## Conclusión

Sequelize es una herramienta poderosa que simplifica la interacción con bases de datos relacionales en aplicaciones Node.js. Si bien tiene una curva de aprendizaje, las ventajas que ofrece en términos de productividad, mantenibilidad y seguridad hacen que valga la pena invertir tiempo en dominarla.

Como todo ORM, hay que ser consciente de sus limitaciones, especialmente en consultas muy complejas o con grandes volúmenes de datos donde el SQL nativo puede ser más eficiente. Sin embargo, para la mayoría de las aplicaciones, Sequelize proporciona un excelente equilibrio entre facilidad de uso y rendimiento.

## Recursos Adicionales

- [Documentación oficial de Sequelize](https://sequelize.org/master/)
- [Repositorio de GitHub](https://github.com/sequelize/sequelize)
- [Guía de migraciones](https://sequelize.org/master/manual/migrations.html)
- [Validaciones en Sequelize](https://sequelize.org/master/manual/validations-and-constraints.html)
- [Hooks (Callbacks)](https://sequelize.org/master/manual/hooks.html)
