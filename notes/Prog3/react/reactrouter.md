# Navegación en React

## 🌐 Introducción: Single Page Applications (SPA)

### ¿Qué es una SPA?

Una **Single Page Application (SPA)** es una aplicación web que funciona dentro de una sola página HTML. En lugar de cargar páginas completamente nuevas desde el servidor, la SPA actualiza dinámicamente el contenido de la página actual.

### Diferencias: Sitio Web Tradicional vs SPA

#### 🏛️ Sitio Web Tradicional (Multi-Page Application)

 Usuario hace clic en "About" →

 1. Navegador envía petición HTTP al servidor
 2. Servidor responde con about.html completo
 3. Navegador recarga toda la página
 4. Se pierden estado, variables, etc.
 
 ❌ Problemas:

 - Recarga completa = experiencia lenta
 - Estado de la aplicación se pierde
 - Más carga en el servidor
 - UX interrumpida

⚡ Single Page Application (SPA)

 Usuario hace clic en "About" →
 
 1. JavaScript intercepta el clic
 2. Se actualiza la URL (sin recargar)
 3. Se cambia solo el contenido necesario
 4. Estado de la aplicación se mantiene

 ✅ Beneficios:

 - Experiencia fluida y rápida
 - Estado persistente
 - Menos carga en el servidor
 - UX similar a app nativa


### Ejemplo Visual de la Diferencia

```jsx
// 🏛️ TRADICIONAL: Cada clic = nueva página completa
function TraditionalWebsite() {
  return (
    <div>
      {/* ❌ Estos enlaces recargan toda la página */}
      <nav>
        <a href="/home.html">Home</a>      {/* Nueva petición HTTP */}
        <a href="/about.html">About</a>    {/* Nueva petición HTTP */}
        <a href="/contact.html">Contact</a> {/* Nueva petición HTTP */}
      </nav>
      
      {/* Todo este contenido se pierde y recarga */}
      <header>Header que se recarga cada vez</header>
      <main>Contenido que cambia</main>
      <footer>Footer que se recarga cada vez</footer>
    </div>
  );
}

// ⚡ SPA: Solo cambia el contenido necesario
function SPAWebsite() {
  const [currentPage, setCurrentPage] = useState('home');
  
  return (
    <div>
      {/* ✅ Estos enlaces solo cambian el estado */}
      <nav>
        <button onClick={() => setCurrentPage('home')}>Home</button>
        <button onClick={() => setCurrentPage('about')}>About</button>
        <button onClick={() => setCurrentPage('contact')}>Contact</button>
      </nav>
      
      {/* Header y footer se mantienen */}
      <header>Header que NUNCA se recarga</header>
      <main>
        {/* Solo este contenido cambia */}
        {currentPage === 'home' && <HomePage />}
        {currentPage === 'about' && <AboutPage />}
        {currentPage === 'contact' && <ContactPage />}
      </main>
      <footer>Footer que NUNCA se recarga</footer>
    </div>
  );
}
```

### Ventajas y Desventajas de las SPAs

**✅ Ventajas:**
- **Velocidad**: Después de la carga inicial, la navegación es instantánea
- **UX Fluida**: Experiencia similar a aplicaciones nativas
- **Estado Persistente**: Variables, formularios, scroll position se mantienen
- **Menos Ancho de Banda**: Solo se cargan los datos necesarios
- **Interactividad Rica**: Animaciones y transiciones suaves

**❌ Desventajas:**
- **Carga Inicial Lenta**: Toda la aplicación se debe descargar al principio
- **SEO Complejo**: Los motores de búsqueda pueden tener problemas
- **Gestión de Estado**: Más complejo manejar estado global
- **URLs y Navegación**: Requiere librerías como React Router
- **Compatibilidad**: Problemas en navegadores muy antiguos

### ¿Cuándo usar SPA vs Sitio Tradicional?


 ✅ ***USA SPA CUANDO:***

 - Aplicaciones interactivas (dashboards, apps)
 - Mucha interacción del usuario
 - Necesitas estado persistente
 - UX fluida es crítica
 - Ejemplo: Gmail, Spotify Web, Facebook

 ✅ ***USA SITIO TRADICIONAL CUANDO:***

 - Sitios informativos (blogs, noticias)
 - SEO es crítico
 - Contenido principalmente estático
 - Usuarios con conexiones lentas
 - Ejemplo: Sitios de noticias, blogs corporativos


## 🧭 ¿Qué es React Router?

**React Router** es la biblioteca estándar para manejar **navegación y rutas** en aplicaciones React. Permite crear SPAs con múltiples vistas manteniendo URLs reales y navegación del navegador funcionando correctamente.

### ¿Por qué necesitamos React Router?

```jsx
// ❌ Sin React Router - solo una página
function App() {
  const [currentPage, setCurrentPage] = useState('home');
  
  return (
    <div>
      <nav>
        <button onClick={() => setCurrentPage('home')}>Home</button>
        <button onClick={() => setCurrentPage('about')}>About</button>
        <button onClick={() => setCurrentPage('contact')}>Contact</button>
      </nav>
      
      {currentPage === 'home' && <Home />}
      {currentPage === 'about' && <About />}
      {currentPage === 'contact' && <Contact />}
    </div>
  );
}

// Problemas:
// - URL no cambia (/contact no existe realmente)
// - No funciona el botón atrás del navegador
// - No se puede compartir URL específica
// - No hay navegación por teclado
```

```jsx
// ✅ Con React Router - rutas reales
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
      </nav>
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </BrowserRouter>
  );
}

// Beneficios:
// ✅ URLs reales (/contact funciona)
// ✅ Botón atrás funciona
// ✅ URLs compartibles
// ✅ Navegación accesible
```



## 📦 Instalación y Configuración

### Instalación

```bash
npm install react-router-dom
```

### Configuración Básica

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
```



## 🛣️ Conceptos Fundamentales

### 1. BrowserRouter vs HashRouter

```jsx
// 🌐 BrowserRouter (Recomendado)
// URLs limpias: example.com/about
import { BrowserRouter } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      {/* Tu aplicación */}
    </BrowserRouter>
  );
}

// 🔗 HashRouter  
// URLs con hash: example.com/#/about
import { HashRouter } from 'react-router-dom';

function App() {
  return (
    <HashRouter>
      {/* Tu aplicación */}
    </HashRouter>
  );
}
```

### 2. Routes y Route

```jsx
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Routes>
      {/* Ruta exacta */}
      <Route path="/" element={<Home />} />
      
      {/* Rutas simples */}
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
      
      {/* Ruta con parámetros */}
      <Route path="/users/:id" element={<UserProfile />} />
      
      {/* Ruta catch-all para 404 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
```

### 3. Link vs NavLink

```jsx
import { Link, NavLink } from 'react-router-dom';

function Navigation() {
  return (
    <nav>
      {/* Link básico */}
      <Link to="/">Home</Link>
      <Link to="/about">About</Link>
      
      {/* NavLink con clase activa automática */}
      <NavLink 
        to="/products" 
        className={({ isActive }) => isActive ? 'active' : ''}
      >
        Products
      </NavLink>
      
      {/* NavLink con estilos inline */}
      <NavLink
        to="/contact"
        style={({ isActive }) => ({
          color: isActive ? 'red' : 'blue',
          fontWeight: isActive ? 'bold' : 'normal'
        })}
      >
        Contact
      </NavLink>
    </nav>
  );
}
```



## 🎯 Ejemplo Básico Completo

```jsx
import React from 'react';
import { BrowserRouter, Routes, Route, Link, NavLink } from 'react-router-dom';
import './App.css';

// Componentes de página
function Home() {
  return (
    <div>
      <h1>🏠 Página de Inicio</h1>
      <p>Bienvenido a nuestra aplicación</p>
      <Link to="/about">Conocer más sobre nosotros →</Link>
    </div>
  );
}

function About() {
  return (
    <div>
      <h1>ℹ️ Acerca de Nosotros</h1>
      <p>Somos una empresa dedicada a crear aplicaciones increíbles</p>
    </div>
  );
}

function Contact() {
  return (
    <div>
      <h1>📞 Contacto</h1>
      <p>Email: contact@example.com</p>
      <p>Teléfono: +1 234 567 890</p>
    </div>
  );
}

function NotFound() {
  return (
    <div style={{ textAlign: 'center' }}>
      <h1>404</h1>
      <h2>😕 Página no encontrada</h2>
      <Link to="/">← Volver al inicio</Link>
    </div>
  );
}

// Componente de navegación
function Navigation() {
  return (
    <nav style={{ 
      padding: '20px', 
      backgroundColor: '#f8f9fa', 
      borderBottom: '1px solid #ddd',
      marginBottom: '20px'
    }}>
      <div style={{ display: 'flex', gap: '20px' }}>
        <NavLink 
          to="/" 
          className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
          end // Para que solo sea activo en la ruta exacta
        >
          Home
        </NavLink>
        <NavLink 
          to="/about" 
          className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
        >
          About
        </NavLink>
        <NavLink 
          to="/contact" 
          className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
        >
          Contact
        </NavLink>
      </div>
    </nav>
  );
}

// Aplicación principal
function App() {
  return (
    <BrowserRouter>
      <div style={{ fontFamily: 'Arial, sans-serif' }}>
        <Navigation />
        
        <main style={{ padding: '0 20px' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
```

```css
/* App.css */
.nav-link {
  text-decoration: none;
  color: #0066cc;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: #e9ecef;
}

.nav-link.active {
  background-color: #0066cc;
  color: white;
}
```



## 🔗 Parámetros de URL

### useParams - Leer Parámetros

```jsx
import { useParams, Link } from 'react-router-dom';

// Ruta: /users/:id
function UserProfile() {
  const { id } = useParams();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Simular llamada a API
    const fetchUser = async () => {
      setLoading(true);
      try {
        // En una app real, harías: fetch(`/api/users/${id}`)
        const mockUser = {
          1: { name: 'Juan Pérez', email: 'juan@example.com', age: 28 },
          2: { name: 'Ana García', email: 'ana@example.com', age: 32 },
          3: { name: 'Pedro López', email: 'pedro@example.com', age: 25 }
        };
        
        await new Promise(resolve => setTimeout(resolve, 500)); // Simular delay
        setUser(mockUser[id] || null);
      } catch (error) {
        console.error('Error fetching user:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchUser();
  }, [id]);
  
  if (loading) {
    return <div>⏳ Cargando usuario...</div>;
  }
  
  if (!user) {
    return (
      <div>
        <h1>❌ Usuario no encontrado</h1>
        <p>El usuario con ID {id} no existe</p>
        <Link to="/users">← Volver a la lista de usuarios</Link>
      </div>
    );
  }
  
  return (
    <div>
      <h1>👤 Perfil de Usuario</h1>
      <div style={{ 
        border: '1px solid #ddd', 
        padding: '20px', 
        borderRadius: '8px',
        backgroundColor: '#f9f9f9'
      }}>
        <h2>{user.name}</h2>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Edad:</strong> {user.age}</p>
        <p><strong>ID:</strong> {id}</p>
      </div>
      <div style={{ marginTop: '20px' }}>
        <Link to="/users">← Volver a la lista</Link>
      </div>
    </div>
  );
}

// Lista de usuarios con enlaces
function UserList() {
  const users = [
    { id: 1, name: 'Juan Pérez' },
    { id: 2, name: 'Ana García' },
    { id: 3, name: 'Pedro López' }
  ];
  
  return (
    <div>
      <h1>👥 Lista de Usuarios</h1>
      <div style={{ display: 'grid', gap: '10px' }}>
        {users.map(user => (
          <Link 
            key={user.id}
            to={`/users/${user.id}`}
            style={{
              display: 'block',
              padding: '15px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              textDecoration: 'none',
              color: 'inherit',
              backgroundColor: '#f8f9fa'
            }}
          >
            <h3 style={{ margin: 0 }}>{user.name}</h3>
            <p style={{ margin: '5px 0 0 0', color: '#666' }}>
              Ver perfil →
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}

// En tu App.js, agregar estas rutas:
function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/users" element={<UserList />} />
        <Route path="/users/:id" element={<UserProfile />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### Múltiples Parámetros

```jsx
// Ruta: /products/:category/:id
function ProductDetail() {
  const { category, id } = useParams();
  
  return (
    <div>
      <h1>Producto {id}</h1>
      <p>Categoría: {category}</p>
      <p>ID del producto: {id}</p>
    </div>
  );
}

// Uso: /products/electronics/123
<Route path="/products/:category/:id" element={<ProductDetail />} />
```



## 🔍 Query Parameters y useSearchParams

### useSearchParams - Manejar Query Strings

```jsx
import { useSearchParams, Link } from 'react-router-dom';

function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products] = useState([
    { id: 1, name: 'Laptop Dell', category: 'electronics', price: 999 },
    { id: 2, name: 'iPhone 14', category: 'electronics', price: 799 },
    { id: 3, name: 'Silla Gaming', category: 'furniture', price: 299 },
    { id: 4, name: 'Mesa Oficina', category: 'furniture', price: 199 }
  ]);
  
  // Leer parámetros actuales
  const category = searchParams.get('category') || 'all';
  const search = searchParams.get('search') || '';
  const sortBy = searchParams.get('sort') || 'name';
  
  // Filtrar productos
  const filteredProducts = products.filter(product => {
    const matchesCategory = category === 'all' || product.category === category;
    const matchesSearch = product.name.toLowerCase().includes(search.toLowerCase());
    return matchesCategory && matchesSearch;
  });
  
  // Ordenar productos
  const sortedProducts = [...filteredProducts].sort((a, b) => {
    if (sortBy === 'price') return a.price - b.price;
    if (sortBy === 'name') return a.name.localeCompare(b.name);
    return 0;
  });
  
  // Función para actualizar parámetros
  const updateSearch = (key, value) => {
    const newSearchParams = new URLSearchParams(searchParams);
    if (value) {
      newSearchParams.set(key, value);
    } else {
      newSearchParams.delete(key);
    }
    setSearchParams(newSearchParams);
  };
  
  return (
    <div>
      <h1>🛍️ Lista de Productos</h1>
      
      {/* Controles de filtro */}
      <div style={{ 
        display: 'flex', 
        gap: '15px', 
        marginBottom: '20px',
        padding: '15px',
        backgroundColor: '#f8f9fa',
        borderRadius: '8px'
      }}>
        <div>
          <label>Buscar: </label>
          <input
            type="text"
            value={search}
            onChange={(e) => updateSearch('search', e.target.value)}
            placeholder="Buscar productos..."
            style={{ padding: '5px' }}
          />
        </div>
        
        <div>
          <label>Categoría: </label>
          <select
            value={category}
            onChange={(e) => updateSearch('category', e.target.value)}
            style={{ padding: '5px' }}
          >
            <option value="all">Todas</option>
            <option value="electronics">Electrónicos</option>
            <option value="furniture">Muebles</option>
          </select>
        </div>
        
        <div>
          <label>Ordenar por: </label>
          <select
            value={sortBy}
            onChange={(e) => updateSearch('sort', e.target.value)}
            style={{ padding: '5px' }}
          >
            <option value="name">Nombre</option>
            <option value="price">Precio</option>
          </select>
        </div>
        
        <button 
          onClick={() => setSearchParams({})}
          style={{ 
            padding: '5px 10px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px'
          }}
        >
          Limpiar filtros
        </button>
      </div>
      
      {/* URL actual para debugging */}
      <div style={{ 
        marginBottom: '20px', 
        padding: '10px', 
        backgroundColor: '#e9ecef',
        borderRadius: '4px',
        fontSize: '12px'
      }}>
        <strong>URL actual:</strong> /products?{searchParams.toString()}
      </div>
      
      {/* Lista de productos */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px' }}>
        {sortedProducts.map(product => (
          <div key={product.id} style={{ 
            border: '1px solid #ddd', 
            padding: '15px', 
            borderRadius: '8px' 
          }}>
            <h3>{product.name}</h3>
            <p>Categoría: {product.category}</p>
            <p>Precio: ${product.price}</p>
            <Link to={`/products/${product.id}`}>Ver detalles →</Link>
          </div>
        ))}
      </div>
      
      {sortedProducts.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666' }}>
          No se encontraron productos con los filtros actuales
        </p>
      )}
    </div>
  );
}

// Ejemplos de URLs generadas:
// /products?category=electronics
// /products?search=laptop&sort=price
// /products?category=furniture&search=silla&sort=name
```



## 🧭 Navegación Programática

### useNavigate - Navegar por Código

```jsx
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Simular login
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (credentials.email && credentials.password) {
        // Login exitoso - navegar al dashboard
        navigate('/dashboard', { replace: true });
        
        // Alternativamente, navegar con estado:
        // navigate('/dashboard', { 
        //   state: { from: 'login', user: credentials.email }
        // });
      } else {
        alert('Credenciales inválidas');
      }
    } catch (error) {
      console.error('Error en login:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleCancel = () => {
    // Navegar hacia atrás
    navigate(-1);
    
    // O navegar a una ruta específica
    // navigate('/');
  };
  
  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
      <h1>🔐 Iniciar Sesión</h1>
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>Email:</label>
          <input
            type="email"
            value={credentials.email}
            onChange={(e) => setCredentials(prev => ({ ...prev, email: e.target.value }))}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label>Contraseña:</label>
          <input
            type="password"
            value={credentials.password}
            onChange={(e) => setCredentials(prev => ({ ...prev, password: e.target.value }))}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <button 
            type="submit" 
            disabled={loading}
            style={{ 
              flex: 1,
              padding: '10px',
              backgroundColor: loading ? '#ccc' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px'
            }}
          >
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
          
          <button 
            type="button"
            onClick={handleCancel}
            style={{ 
              flex: 1,
              padding: '10px',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px'
            }}
          >
            Cancelar
          </button>
        </div>
      </form>
      
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <button onClick={() => navigate('/register')}>
          ¿No tienes cuenta? Registrarse
        </button>
      </div>
    </div>
  );
}

// Componente Dashboard que recibe el estado
function Dashboard() {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Acceder al estado pasado desde navigate
  const fromLogin = location.state?.from === 'login';
  const userEmail = location.state?.user;
  
  const handleLogout = () => {
    // Limpiar sesión y navegar al home
    navigate('/', { replace: true });
  };
  
  return (
    <div style={{ padding: '20px' }}>
      <h1>📊 Dashboard</h1>
      
      {fromLogin && (
        <div style={{ 
          backgroundColor: '#d4edda', 
          padding: '10px', 
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          ✅ Login exitoso! Bienvenido{userEmail && ` ${userEmail}`}
        </div>
      )}
      
      <p>Contenido del dashboard aquí...</p>
      
      <button onClick={handleLogout}>
        Cerrar Sesión
      </button>
    </div>
  );
}
```

### Navegación Condicional

```jsx
function ProtectedRoute({ children }) {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Verificar autenticación
    const checkAuth = async () => {
      try {
        // Simular verificación de token
        const token = localStorage.getItem('token');
        setIsAuthenticated(!!token);
      } catch (error) {
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };
    
    checkAuth();
  }, []);
  
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      // Redirigir a login si no está autenticado
      navigate('/login', { replace: true });
    }
  }, [loading, isAuthenticated, navigate]);
  
  if (loading) {
    return <div>⏳ Verificando autenticación...</div>;
  }
  
  return isAuthenticated ? children : null;
}

// Uso en rutas
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginForm />} />
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </BrowserRouter>
  );
}
```



## 🗂️ Rutas Anidadas

### Outlet - Componentes Hijos

```jsx
import { Outlet, Link, useLocation } from 'react-router-dom';

// Layout principal
function DashboardLayout() {
  const location = useLocation();
  
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <nav style={{ 
        width: '250px', 
        backgroundColor: '#f8f9fa', 
        padding: '20px',
        borderRight: '1px solid #ddd'
      }}>
        <h2>📊 Dashboard</h2>
        
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ marginBottom: '10px' }}>
            <Link 
              to="/dashboard" 
              style={{ 
                textDecoration: 'none',
                color: location.pathname === '/dashboard' ? '#007bff' : '#333'
              }}
            >
              📈 Resumen
            </Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link 
              to="/dashboard/users"
              style={{ 
                textDecoration: 'none',
                color: location.pathname.includes('/dashboard/users') ? '#007bff' : '#333'
              }}
            >
              👥 Usuarios
            </Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link 
              to="/dashboard/products"
              style={{ 
                textDecoration: 'none',
                color: location.pathname.includes('/dashboard/products') ? '#007bff' : '#333'
              }}
            >
              📦 Productos
            </Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link 
              to="/dashboard/settings"
              style={{ 
                textDecoration: 'none',
                color: location.pathname === '/dashboard/settings' ? '#007bff' : '#333'
              }}
            >
              ⚙️ Configuración
            </Link>
          </li>
        </ul>
      </nav>
      
      {/* Contenido principal */}
      <main style={{ flex: 1, padding: '20px' }}>
        {/* Aquí se renderizan los componentes hijos */}
        <Outlet />
      </main>
    </div>
  );
}

// Componentes de las páginas del dashboard
function DashboardHome() {
  return (
    <div>
      <h1>📈 Resumen del Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
        <div style={{ padding: '20px', backgroundColor: '#e3f2fd', borderRadius: '8px' }}>
          <h3>👥 Usuarios</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>1,234</p>
        </div>
        <div style={{ padding: '20px', backgroundColor: '#f3e5f5', borderRadius: '8px' }}>
          <h3>📦 Productos</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>567</p>
        </div>
        <div style={{ padding: '20px', backgroundColor: '#e8f5e8', borderRadius: '8px' }}>
          <h3>💰 Ventas</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>$89,012</p>
        </div>
      </div>
    </div>
  );
}

function DashboardUsers() {
  return (
    <div>
      <h1>👥 Gestión de Usuarios</h1>
      <div style={{ marginBottom: '20px' }}>
        <Link to="/dashboard/users/new" style={{ 
          backgroundColor: '#28a745',
          color: 'white',
          padding: '10px 20px',
          textDecoration: 'none',
          borderRadius: '4px'
        }}>
          ➕ Nuevo Usuario
        </Link>
      </div>
      
      {/* Aquí irían los componentes hijos de usuarios */}
      <Outlet />
    </div>
  );
}

function UsersList() {
  const users = [
    { id: 1, name: 'Juan Pérez', email: 'juan@example.com' },
    { id: 2, name: 'Ana García', email: 'ana@example.com' },
    { id: 3, name: 'Pedro López', email: 'pedro@example.com' }
  ];
  
  return (
    <div>
      <h2>Lista de Usuarios</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f8f9fa' }}>
            <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>ID</th>
            <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Nombre</th>
            <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Email</th>
            <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td style={{ padding: '10px', border: '1px solid #ddd' }}>{user.email}</td>
              <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                <Link to={`/dashboard/users/${user.id}`} style={{ marginRight: '10px' }}>
                  Ver
                </Link>
                <Link to={`/dashboard/users/${user.id}/edit`}>
                  Editar
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function NewUser() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ name: '', email: '' });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    // Simular creación de usuario
    console.log('Creando usuario:', formData);
    // Navegar de vuelta a la lista
    navigate('/dashboard/users');
  };
  
  return (
    <div>
      <h2>➕ Nuevo Usuario</h2>
      <form onSubmit={handleSubmit} style={{ maxWidth: '400px' }}>
        <div style={{ marginBottom: '15px' }}>
          <label>Nombre:</label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>Email:</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button type="submit" style={{ 
            backgroundColor: '#28a745',
            color: 'white',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '4px'
          }}>
            Crear Usuario
          </button>
          <button 
            type="button"
            onClick={() => navigate('/dashboard/users')}
            style={{ 
              backgroundColor: '#6c757d',
              color: 'white',
              padding: '10px 20px',
              border: 'none',
              borderRadius: '4px'
            }}
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}

// Configuración de rutas anidadas
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginForm />} />
        
        {/* Rutas anidadas del dashboard */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          {/* Ruta índice - se muestra cuando la URL es exactamente /dashboard */}
          <Route index element={<DashboardHome />} />
          
          {/* Rutas de usuarios */}
          <Route path="users" element={<DashboardUsers />}>
            {/* Ruta índice para /dashboard/users */}
            <Route index element={<UsersList />} />
            <Route path="new" element={<NewUser />} />
            <Route path=":id" element={<UserDetail />} />
            <Route path=":id/edit" element={<EditUser />} />
          </Route>
          
          <Route path="products" element={<DashboardProducts />} />
          <Route path="settings" element={<DashboardSettings />} />
        </Route>
        
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```



## 🔒 Rutas Protegidas y Guards

### Componente de Ruta Protegida

```jsx
import { Navigate, useLocation } from 'react-router-dom';

function ProtectedRoute({ children, requireAuth = true, roles = [] }) {
  const location = useLocation();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Verificar autenticación y roles
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          // En una app real, verificarías el token con el servidor
          const userData = JSON.parse(localStorage.getItem('user') || '{}');
          setUser(userData);
        }
      } catch (error) {
        console.error('Error verificando autenticación:', error);
      } finally {
        setLoading(false);
      }
    };
    
    checkAuth();
  }, []);
  
  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        ⏳ Verificando permisos...
      </div>
    );
  }
  
  // Si requiere autenticación pero no hay usuario
  if (requireAuth && !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  // Si requiere roles específicos
  if (user && roles.length > 0 && !roles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }
  
  return children;
}

// Componente para rutas de solo invitados (ej: login, register)
function GuestRoute({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        const userData = JSON.parse(localStorage.getItem('user') || '{}');
        setUser(userData);
      }
      setLoading(false);
    };
    
    checkAuth();
  }, []);
  
  if (loading) {
    return <div>⏳ Cargando...</div>;
  }
  
  // Si ya está autenticado, redirigir al dashboard
  if (user) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return children;
}

// Página de no autorizado
function Unauthorized() {
  const navigate = useNavigate();
  
  return (
    <div style={{ textAlign: 'center', padding: '50px' }}>
      <h1>🚫 Acceso Denegado</h1>
      <p>No tienes permisos para acceder a esta página</p>
      <div style={{ marginTop: '20px' }}>
        <button onClick={() => navigate('/')}>
          🏠 Ir al Inicio
        </button>
        <button onClick={() => navigate(-1)} style={{ marginLeft: '10px' }}>
          ← Volver
        </button>
      </div>
    </div>
  );
}

// Uso en la aplicación
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        
        {/* Rutas solo para invitados */}
        <Route 
          path="/login" 
          element={
            <GuestRoute>
              <LoginForm />
            </GuestRoute>
          } 
        />
        <Route 
          path="/register" 
          element={
            <GuestRoute>
              <RegisterForm />
            </GuestRoute>
          } 
        />
        
        {/* Rutas protegidas */}
        <Route 
          path="/dashboard/*" 
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          } 
        />
        
        {/* Ruta solo para administradores */}
        <Route 
          path="/admin/*" 
          element={
            <ProtectedRoute roles={['admin']}>
              <AdminPanel />
            </ProtectedRoute>
          } 
        />
        
        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### Hook Personalizado para Autenticación

```jsx
function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  
  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          // Verificar token con el servidor
          const userData = JSON.parse(localStorage.getItem('user') || '{}');
          setUser(userData);
        }
      } catch (error) {
        console.error('Error inicializando autenticación:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      } finally {
        setLoading(false);
      }
    };
    
    initAuth();
  }, []);
  
  const login = async (credentials) => {
    try {
      // Simular login
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });
      
      const data = await response.json();
      
      if (response.ok) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        setUser(data.user);
        return { success: true };
      } else {
        return { success: false, error: data.message };
      }
    } catch (error) {
      return { success: false, error: 'Error de conexión' };
    }
  };
  
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
  };
  
  const hasRole = (role) => {
    return user?.role === role;
  };
  
  const hasAnyRole = (roles) => {
    return roles.includes(user?.role);
  };
  
  return {
    user,
    loading,
    login,
    logout,
    hasRole,
    hasAnyRole,
    isAuthenticated: !!user
  };
}

// Uso del hook
function Dashboard() {
  const { user, logout, hasRole } = useAuth();
  
  return (
    <div>
      <header style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        padding: '10px 20px',
        backgroundColor: '#f8f9fa'
      }}>
        <h1>Dashboard</h1>
        <div>
          <span>Hola, {user?.name}</span>
          {hasRole('admin') && (
            <Link to="/admin" style={{ marginLeft: '10px' }}>
              Panel Admin
            </Link>
          )}
          <button onClick={logout} style={{ marginLeft: '10px' }}>
            Cerrar Sesión
          </button>
        </div>
      </header>
      
      {/* Contenido del dashboard */}
    </div>
  );
}
```



## 🎨 Layout y Navegación Avanzada

### Layout Persistente

```jsx
function AppLayout() {
  const location = useLocation();
  const { user, logout } = useAuth();
  
  // No mostrar header en páginas de login/register
  const hideHeader = ['/login', '/register'].includes(location.pathname);
  
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {!hideHeader && (
        <header style={{ 
          backgroundColor: '#343a40',
          color: 'white',
          padding: '0 20px'
        }}>
          <nav style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            height: '60px'
          }}>
            <Link to="/" style={{ 
              color: 'white', 
              textDecoration: 'none', 
              fontSize: '20px',
              fontWeight: 'bold'
            }}>
              🚀 Mi App
            </Link>
            
            <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
              <NavLink 
                to="/" 
                style={({ isActive }) => ({
                  color: isActive ? '#ffc107' : 'white',
                  textDecoration: 'none'
                })}
              >
                Inicio
              </NavLink>
              <NavLink 
                to="/products" 
                style={({ isActive }) => ({
                  color: isActive ? '#ffc107' : 'white',
                  textDecoration: 'none'
                })}
              >
                Productos
              </NavLink>
              
              {user ? (
                <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                  <NavLink 
                    to="/dashboard" 
                    style={({ isActive }) => ({
                      color: isActive ? '#ffc107' : 'white',
                      textDecoration: 'none'
                    })}
                  >
                    Dashboard
                  </NavLink>
                  <span>Hola, {user.name}</span>
                  <button 
                    onClick={logout}
                    style={{ 
                      background: 'none',
                      border: '1px solid white',
                      color: 'white',
                      padding: '5px 10px',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    Salir
                  </button>
                </div>
              ) : (
                <div style={{ display: 'flex', gap: '10px' }}>
                  <Link 
                    to="/login"
                    style={{ 
                      color: 'white',
                      textDecoration: 'none',
                      padding: '5px 10px',
                      border: '1px solid white',
                      borderRadius: '4px'
                    }}
                  >
                    Ingresar
                  </Link>
                  <Link 
                    to="/register"
                    style={{ 
                      backgroundColor: '#007bff',
                      color: 'white',
                      textDecoration: 'none',
                      padding: '5px 10px',
                      borderRadius: '4px'
                    }}
                  >
                    Registrarse
                  </Link>
                </div>
              )}
            </div>
          </nav>
        </header>
      )}
      
      <main style={{ flex: 1 }}>
        <Outlet />
      </main>
      
      {!hideHeader && (
        <footer style={{ 
          backgroundColor: '#f8f9fa',
          padding: '20px',
          textAlign: 'center',
          borderTop: '1px solid #ddd'
        }}>
          <p>&copy; 2024 Mi App. Todos los derechos reservados.</p>
        </footer>
      )}
    </div>
  );
}

// Breadcrumbs dinámicos
function Breadcrumbs() {
  const location = useLocation();
  
  const pathnames = location.pathname.split('/').filter(x => x);
  
  const breadcrumbNameMap = {
    '/dashboard': 'Dashboard',
    '/dashboard/users': 'Usuarios',
    '/dashboard/products': 'Productos',
    '/dashboard/settings': 'Configuración',
    '/products': 'Productos',
    '/about': 'Acerca de'
  };
  
  return (
    <nav style={{ 
      padding: '10px 20px',
      backgroundColor: '#f8f9fa',
      borderBottom: '1px solid #ddd'
    }}>
      <Link to="/" style={{ textDecoration: 'none', color: '#007bff' }}>
        🏠 Inicio
      </Link>
      
      {pathnames.map((name, index) => {
        const routeTo = `/${pathnames.slice(0, index + 1).join('/')}`;
        const isLast = index === pathnames.length - 1;
        const displayName = breadcrumbNameMap[routeTo] || name;
        
        return (
          <span key={routeTo}>
            <span style={{ margin: '0 10px', color: '#6c757d' }}>→</span>
            {isLast ? (
              <span style={{ color: '#6c757d' }}>{displayName}</span>
            ) : (
              <Link 
                to={routeTo} 
                style={{ textDecoration: 'none', color: '#007bff' }}
              >
                {displayName}
              </Link>
            )}
          </span>
        );
      })}
    </nav>
  );
}
```



## 🔄 Lazy Loading y Code Splitting

### Carga Diferida de Componentes

```jsx
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// 📦 Componentes cargados de forma diferida
const Dashboard = lazy(() => import('./pages/Dashboard'));
const UserList = lazy(() => import('./pages/UserList'));
const ProductDetail = lazy(() => import('./pages/ProductDetail'));

// Componente de loading
function LoadingSpinner() {
  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '200px' 
    }}>
      <div>⏳ Cargando...</div>
    </div>
  );
}

// Wrapper para lazy components
function LazyRoute({ children }) {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      {children}
    </Suspense>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        
        {/* Rutas con lazy loading */}
        <Route 
          path="/dashboard" 
          element={
            <LazyRoute>
              <Dashboard />
            </LazyRoute>
          } 
        />
        
        <Route 
          path="/users" 
          element={
            <LazyRoute>
              <UserList />
            </LazyRoute>
          } 
        />
        
        <Route 
          path="/products/:id" 
          element={
            <LazyRoute>
              <ProductDetail />
            </LazyRoute>
          } 
        />
      </Routes>
    </BrowserRouter>
  );
}
```

### Preloading Inteligente

```jsx
function NavigationWithPreload() {
  // Precargar componentes en hover
  const handleMouseEnter = (componentName) => {
    switch (componentName) {
      case 'dashboard':
        import('./pages/Dashboard');
        break;
      case 'users':
        import('./pages/UserList');
        break;
      default:
        break;
    }
  };
  
  return (
    <nav>
      <Link 
        to="/dashboard"
        onMouseEnter={() => handleMouseEnter('dashboard')}
      >
        Dashboard
      </Link>
      <Link 
        to="/users"
        onMouseEnter={() => handleMouseEnter('users')}
      >
        Usuarios
      </Link>
    </nav>
  );
}
```



## 📱 Patrones Avanzados

### Rutas Dinámicas y Meta Tags

```jsx
function RouteMeta({ title, description }) {
  useEffect(() => {
    document.title = title;
    
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
      metaDescription.setAttribute('content', description);
    }
  }, [title, description]);
  
  return null;
}

function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  
  useEffect(() => {
    // Cargar producto...
  }, [id]);
  
  if (!product) return <div>Cargando...</div>;
  
  return (
    <div>
      <RouteMeta 
        title={`${product.name} - Mi Tienda`}
        description={product.description}
      />
      
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  );
}
```

### Scroll Management

```jsx
function ScrollToTop() {
  const { pathname } = useLocation();
  
  useEffect(() => {
    // Scroll al top en cada cambio de ruta
    window.scrollTo(0, 0);
  }, [pathname]);
  
  return null;
}

// Scroll suave a secciones
function useScrollToSection() {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    }
  };
  
  return scrollToSection;
}

function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <Routes>
        {/* Rutas */}
      </Routes>
    </BrowserRouter>
  );
}
```



## 💻 Ejercicios Prácticos

### Ejercicio 1: E-commerce Básico

Crea una aplicación de e-commerce con las siguientes rutas:

```jsx
// Estructura requerida:
// /                    - Home con productos destacados
// /products            - Lista de todos los productos
// /products/:category  - Productos por categoría
// /product/:id         - Detalle del producto
// /cart                - Carrito de compras
// /checkout            - Proceso de compra (protegida)
// /login               - Login
// /register            - Registro
// /profile             - Perfil usuario (protegida)

// Características requeridas:
// - Navegación con breadcrumbs
// - Carrito persistente en localStorage
// - Rutas protegidas para usuarios autenticados
// - Query parameters para filtros y búsqueda
// - Lazy loading para páginas pesadas
```

### Ejercicio 2: Dashboard Administrativo

```jsx
// Estructura requerida:
// /admin                    - Dashboard principal
// /admin/users             - Lista de usuarios
// /admin/users/new         - Crear usuario
// /admin/users/:id         - Ver usuario
// /admin/users/:id/edit    - Editar usuario
// /admin/products          - Gestión de productos
// /admin/orders            - Gestión de pedidos
// /admin/settings          - Configuración

// Características requeridas:
// - Layout con sidebar
// - Rutas solo para admin
// - Navegación anidada
// - Formularios con validación
// - Confirmaciones antes de eliminar
```

### Ejercicio 3: Blog con Comentarios

```jsx
// Estructura requerida:
// /                    - Lista de posts
// /post/:slug          - Detalle del post
// /category/:name      - Posts por categoría
// /author/:id          - Posts por autor
// /search              - Búsqueda de posts
// /write               - Crear post (protegida)
// /edit/:id            - Editar post (protegida)

// Características requeridas:
// - URLs amigables con slugs
// - Comentarios anidados
// - Sistema de tags
// - Búsqueda con query parameters
// - Meta tags dinámicos para SEO
```



## 🎯 Mejores Prácticas

### Organización de Rutas

```jsx
// ✅ Organizar rutas por feature
const routes = {
  auth: [
    { path: '/login', element: <Login /> },
    { path: '/register', element: <Register /> }
  ],
  dashboard: [
    { path: '/dashboard', element: <Dashboard /> },
    { path: '/dashboard/users', element: <Users /> }
  ],
  public: [
    { path: '/', element: <Home /> },
    { path: '/about', element: <About /> }
  ]
};

// ✅ Constantes para rutas
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  USERS: '/dashboard/users',
  USER_DETAIL: (id) => `/users/${id}`,
  PRODUCTS: '/products',
  PRODUCT_DETAIL: (id) => `/products/${id}`
};
```

### Performance y SEO

```jsx
// ✅ Meta tags dinámicos
function useDocumentTitle(title) {
  useEffect(() => {
    document.title = title;
  }, [title]);
}

// ✅ Preloading crítico
function CriticalRoute({ children }) {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      {children}
    </Suspense>
  );
}

// ✅ Error boundaries para rutas
class RouteErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  render() {
    if (this.state.hasError) {
      return <div>Algo salió mal en esta página</div>;
    }
    
    return this.props.children;
  }
}
```



## 🔄 Resumen de Conceptos

### Componentes Principales:
- `BrowserRouter`: Proveedor de routing
- `Routes`: Contenedor de rutas
- `Route`: Definición de ruta individual
- `Link/NavLink`: Enlaces de navegación
- `Outlet`: Punto de renderizado para rutas anidadas

### Hooks Principales:
- `useNavigate`: Navegación programática
- `useParams`: Parámetros de URL
- `useSearchParams`: Query parameters
- `useLocation`: Información de la ubicación actual

### Patrones Importantes:
- Rutas protegidas con autenticación
- Rutas anidadas con Outlet
- Lazy loading para code splitting
- Layouts persistentes
- Breadcrumbs dinámicos



## 🏁 Próximos Pasos

En el siguiente módulo aprenderemos:

- **Estado global** con Context API y Redux
- **Testing** de componentes con rutas
- **Server-Side Rendering** con Next.js
- **PWA** y routing offline
- **React Router v7** y nuevas características

## ❓ Preguntas Frecuentes

**P: ¿Cuál es la diferencia entre Link y NavLink?**
R: `Link` es básico para navegación, `NavLink` incluye estado activo automático y es ideal para navegación principal.

**P: ¿Cuándo usar BrowserRouter vs HashRouter?**
R: `BrowserRouter` para URLs limpias en producción, `HashRouter` solo si no puedes configurar el servidor.

**P: ¿Cómo manejar rutas 404?**
R: Usa `<Route path="*" element={<NotFound />} />` al final de tus rutas.

**P: ¿Puedo tener múltiples parámetros en una ruta?**
R: Sí, puedes usar `/users/:userId/posts/:postId` y acceder con `useParams()`.

**P: ¿Cómo persisto el estado al navegar?**
R: Usa `location.state` para datos temporales o Context/localStorage para estado persistente.

**P: ¿React Router funciona con SSR?**
R: Sí, pero necesitas usar `StaticRouter` en el servidor y `BrowserRouter` en el cliente.px solid #ddd' }}>{user.id}</td>
              <td style={{ padding: '10px', border: '1px solid #ddd' }}>{user.name}</td>
              <td style={{ padding: '10px', border: '1