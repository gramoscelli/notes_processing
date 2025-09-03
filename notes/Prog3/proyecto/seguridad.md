# Seguridad en Aplicaciones Web: JWT, CORS y Mecanismos CSRF

## Introducción

En el desarrollo de aplicaciones web modernas, la implementación de mecanismos de seguridad robustos es fundamental para proteger tanto los datos de los usuarios como la integridad del sistema. Este documento analiza tres componentes esenciales de seguridad: JSON Web Tokens (JWT), Cross-Origin Resource Sharing (CORS) y protecciones contra Cross-Site Request Forgery (CSRF).

## JSON Web Tokens (JWT)

### ¿Qué es JWT?

JWT es un estándar abierto (RFC 7519) que define una forma compacta y autónoma de transmitir información de manera segura entre partes como un objeto JSON. Esta información puede ser verificada y confiable porque está firmada digitalmente.

### Estructura de un JWT

Un JWT consta de tres partes separadas por puntos:
- **Header**: Contiene el tipo de token y el algoritmo de firma
- **Payload**: Contiene las declaraciones (claims) sobre el usuario
- **Signature**: Verifica que el token no ha sido alterado

### Necesidad de JWT en Aplicaciones Web

#### 1. Autenticación Stateless
Las aplicaciones modernas requieren autenticación sin estado para mejorar la escalabilidad. JWT permite que cada token contenga toda la información necesaria para identificar al usuario, eliminando la necesidad de almacenar sesiones en el servidor.

#### 2. Escalabilidad Horizontal
En arquitecturas distribuidas con múltiples servidores, JWT facilita la autenticación sin requerir un almacén de sesiones compartido. Cualquier servidor puede validar un token sin consultar una base de datos centralizada.

#### 3. Integración con APIs
Para aplicaciones que consumen múltiples APIs o servicios, JWT proporciona un mecanismo estándar de autenticación que puede ser utilizado consistentemente across diferentes servicios.

#### 4. Seguridad en SPAs
Las Single Page Applications (SPA) se benefician de JWT porque permite mantener el estado de autenticación del lado del cliente de manera segura, sin depender de cookies de sesión tradicionales.

### Implementación Recomendada

```javascript
// Ejemplo de generación de JWT en Node.js
const jwt = require('jsonwebtoken');

const generateToken = (user) => {
  return jwt.sign(
    { 
      userId: user.id, 
      email: user.email,
      role: user.role 
    },
    process.env.JWT_SECRET,
    { 
      expiresIn: '15m',
      issuer: 'your-app-name'
    }
  );
};
```

## Cross-Origin Resource Sharing (CORS)

### ¿Qué es CORS?

CORS es un mecanismo que utiliza cabeceras HTTP adicionales para permitir que un navegador web ejecute una aplicación web desde un origen (dominio) para acceder a recursos de otro origen diferente.

### Necesidad de CORS

#### 1. Same-Origin Policy
Los navegadores implementan la política del mismo origen como medida de seguridad, bloqueando solicitudes entre diferentes dominios. CORS proporciona una forma controlada de relajar esta restricción.

#### 2. Arquitecturas Modernas
Las aplicaciones modernas frecuentemente separan el frontend del backend en diferentes dominios o puertos. CORS es esencial para permitir esta comunicación.

#### 3. APIs Públicas
Para servicios que ofrecen APIs públicas, CORS permite controlar qué dominios pueden acceder a los recursos, manteniendo la seguridad.

#### 4. Desarrollo y Producción
Durante el desarrollo, es común que el frontend y backend corran en puertos diferentes. CORS facilita esta configuración sin comprometer la seguridad.

### Configuración de CORS

```javascript
// Ejemplo de configuración CORS en Express.js
const cors = require('cors');

const corsOptions = {
  origin: [
    'https://yourdomain.com',
    'https://www.yourdomain.com'
  ],
  credentials: true,
  optionsSuccessStatus: 200,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
};

app.use(cors(corsOptions));
```

### Tipos de Solicitudes CORS

#### Solicitudes Simples
- Métodos: GET, HEAD, POST
- Headers permitidos: Accept, Accept-Language, Content-Language, Content-Type
- Content-Type limitado a: application/x-www-form-urlencoded, multipart/form-data, text/plain

#### Solicitudes Preflight
Para solicitudes que no califican como simples, el navegador envía una solicitud OPTIONS para verificar permisos antes de la solicitud real.

## Cross-Site Request Forgery (CSRF)

### ¿Qué es CSRF?

CSRF es un tipo de ataque que fuerza a un usuario autenticado a ejecutar acciones no deseadas en una aplicación web en la que está autenticado. El atacante engaña al navegador del usuario para que envíe solicitudes maliciosas utilizando las credenciales del usuario.

### Necesidad de Protección CSRF

#### 1. Protección de Acciones Sensibles
Las operaciones que modifican datos (transferencias bancarias, cambios de contraseña, eliminación de cuentas) requieren protección contra ejecución no autorizada.

#### 2. Validación de Intención del Usuario
CSRF ayuda a garantizar que las acciones realizadas en la aplicación fueron iniciadas intencionalmente por el usuario autenticado.

#### 3. Cumplimiento de Estándares
Muchos estándares de seguridad y regulaciones requieren implementar protecciones contra CSRF para aplicaciones que manejan datos sensibles.

### Mecanismos de Protección CSRF

#### 1. CSRF Tokens
Generar tokens únicos para cada sesión o formulario que deben ser incluidos en las solicitudes.

```javascript
// Ejemplo de implementación de CSRF token
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.use(csrfProtection);

app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});
```

#### 2. SameSite Cookies
Configurar cookies con el atributo SameSite para limitar cuándo se envían en solicitudes cross-site.

```javascript
app.use(session({
  cookie: {
    sameSite: 'strict', // o 'lax' según necesidades
    secure: true, // solo HTTPS
    httpOnly: true
  }
}));
```

#### 3. Verificación de Referer/Origin
Validar que las solicitudes provienen del dominio esperado.

#### 4. Double Submit Cookie
Enviar el token CSRF tanto en una cookie como en un header personalizado.

## Integración de los Tres Mecanismos

### Arquitectura Recomendada

```javascript
// Configuración integrada de seguridad
const express = require('express');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const csrf = require('csurf');

const app = express();

// Configuración CORS
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
  credentials: true
}));

// Middleware de autenticación JWT
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.sendStatus(401);
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

// Protección CSRF para rutas sensibles
const csrfProtection = csrf({ cookie: true });
app.use('/api/sensitive', csrfProtection);
```

### Flujo de Seguridad Completo

1. **Autenticación**: El usuario se autentica y recibe un JWT
2. **CORS**: El navegador verifica que el origen está permitido
3. **Autorización**: El servidor valida el JWT en cada solicitud
4. **CSRF**: Para operaciones sensibles, se verifica el token CSRF

## Mejores Prácticas

### Para JWT
- Utilizar tiempos de expiración cortos (15-30 minutos)
- Implementar refresh tokens para renovación
- Almacenar de forma segura (httpOnly cookies vs localStorage)
- Validar siempre la firma y expiración

### Para CORS
- Ser específico con los orígenes permitidos
- No usar wildcards (*) en producción con credentials
- Configurar headers apropiados para cada endpoint
- Implementar whitelist de dominios

### Para CSRF
- Usar tokens únicos por sesión
- Validar en todas las operaciones de escritura
- Combinar con verificación de Referer/Origin
- Implementar timeouts para tokens

## Consideraciones de Rendimiento

### JWT
- Los tokens grandes pueden impactar el rendimiento de la red
- Considerar el overhead de verificación de firma
- Balancear información incluida vs tamaño del token

### CORS
- Las solicitudes preflight agregan latencia
- Optimizar configuración para minimizar preflight requests
- Considerar caché de respuestas preflight

### CSRF
- Los tokens agregan overhead mínimo
- Considerar la generación y validación de tokens
- Optimizar el almacenamiento de tokens

## Ejemplo Práctico: Implementación en React

### Configuración del Cliente React

A continuación se presenta un ejemplo completo de cómo implementar estos mecanismos de seguridad en una aplicación React moderna:

#### 1. Configuración del Servicio de Autenticación

```javascript
// services/authService.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

// Configuración de Axios con interceptores
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Importante para CORS con cookies
  timeout: 10000
});

// Interceptor para agregar JWT token a las solicitudes
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar tokens expirados
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refreshToken
          });
          const { accessToken } = response.data;
          localStorage.setItem('accessToken', accessToken);
          // Reintentar la solicitud original
          error.config.headers.Authorization = `Bearer ${accessToken}`;
          return apiClient.request(error.config);
        } catch (refreshError) {
          // Refresh token inválido, logout
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (credentials) => {
    const response = await apiClient.post('/auth/login', credentials);
    const { accessToken, refreshToken, user } = response.data;
    
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    
    return { user, accessToken };
  },

  logout: async () => {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  },

  getCurrentUser: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  }
};

export { apiClient };
```

#### 2. Hook de Autenticación

```javascript
// hooks/useAuth.js
import { createContext, useContext, useEffect, useState } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        try {
          const userData = await authService.getCurrentUser();
          setUser(userData);
          setIsAuthenticated(true);
        } catch (error) {
          console.error('Error al verificar autenticación:', error);
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (credentials) => {
    try {
      const { user, accessToken } = await authService.login(credentials);
      setUser(user);
      setIsAuthenticated(true);
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.message || 'Error de autenticación' 
      };
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
    } finally {
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de AuthProvider');
  }
  return context;
};
```

#### 3. Componente con Protección CSRF

```javascript
// components/TransferForm.js
import { useState, useEffect } from 'react';
import { apiClient } from '../services/authService';

const TransferForm = () => {
  const [formData, setFormData] = useState({
    accountTo: '',
    amount: '',
    description: ''
  });
  const [csrfToken, setCsrfToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Obtener token CSRF al montar el componente
  useEffect(() => {
    const fetchCSRFToken = async () => {
      try {
        const response = await apiClient.get('/api/csrf-token');
        setCsrfToken(response.data.csrfToken);
      } catch (error) {
        console.error('Error al obtener token CSRF:', error);
      }
    };

    fetchCSRFToken();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Incluir token CSRF en la solicitud
      const response = await apiClient.post('/api/transfer', formData, {
        headers: {
          'X-CSRF-Token': csrfToken
        }
      });

      if (response.data.success) {
        alert('Transferencia realizada exitosamente');
        setFormData({ accountTo: '', amount: '', description: '' });
        
        // Obtener nuevo token CSRF después de la operación
        const newTokenResponse = await apiClient.get('/api/csrf-token');
        setCsrfToken(newTokenResponse.data.csrfToken);
      }
    } catch (error) {
      setError(error.response?.data?.message || 'Error al procesar transferencia');
      
      // Si el error es por token CSRF inválido, obtener uno nuevo
      if (error.response?.status === 403) {
        const newTokenResponse = await apiClient.get('/api/csrf-token');
        setCsrfToken(newTokenResponse.data.csrfToken);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <form onSubmit={handleSubmit} className="transfer-form">
      <h2>Transferencia Bancaria</h2>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="accountTo">Cuenta destino:</label>
        <input
          type="text"
          id="accountTo"
          name="accountTo"
          value={formData.accountTo}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="amount">Monto:</label>
        <input
          type="number"
          id="amount"
          name="amount"
          value={formData.amount}
          onChange={handleChange}
          min="0.01"
          step="0.01"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Descripción:</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows="3"
        />
      </div>

      {/* Token CSRF oculto */}
      <input type="hidden" name="_csrf" value={csrfToken} />

      <button type="submit" disabled={loading || !csrfToken}>
        {loading ? 'Procesando...' : 'Realizar Transferencia'}
      </button>
    </form>
  );
};

export default TransferForm;
```

#### 4. Configuración de Rutas Protegidas

```javascript
// components/ProtectedRoute.js
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return <div className="loading">Cargando...</div>;
  }

  if (!isAuthenticated) {
    // Redirigir a login preservando la URL de destino
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;
```

#### 5. Configuración Principal de la App

```javascript
// App.js
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import TransferPage from './pages/TransferPage';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="App">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/transfer" 
              element={
                <ProtectedRoute>
                  <TransferPage />
                </ProtectedRoute>
              } 
            />
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
```

#### 6. Manejo de Errores CORS

```javascript
// utils/corsErrorHandler.js
export const handleCORSError = (error) => {
  if (error.code === 'ERR_NETWORK') {
    return {
      type: 'CORS_ERROR',
      message: 'Error de conectividad. Verifica la configuración CORS del servidor.',
      details: 'El servidor puede no estar permitiendo solicitudes desde este origen.'
    };
  }
  
  if (error.response?.status === 0) {
    return {
      type: 'CORS_ERROR',
      message: 'No se pudo conectar con el servidor.',
      details: 'Verifica que el servidor esté ejecutándose y que CORS esté configurado correctamente.'
    };
  }
  
  return null;
};

// Uso en componentes
const handleAPIError = (error) => {
  const corsError = handleCORSError(error);
  if (corsError) {
    setError(corsError.message);
    console.error('Error CORS:', corsError.details);
    return;
  }
  
  // Manejar otros tipos de errores
  setError(error.response?.data?.message || 'Error desconocido');
};
```

### Variables de Entorno

```env
# .env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
```

```env
# .env.development
REACT_APP_API_URL=http://localhost:3001
REACT_APP_ENVIRONMENT=development
```

### Beneficios de esta Implementación

1. **Manejo Automático de Tokens**: Los interceptores de Axios manejan automáticamente la inclusión de JWT y la renovación de tokens expirados.

2. **Protección CSRF Transparente**: Los componentes que realizan operaciones sensibles obtienen y utilizan tokens CSRF automáticamente.

3. **Gestión de Estado Centralizada**: El contexto de autenticación proporciona un estado global accesible desde cualquier componente.

4. **Manejo de Errores CORS**: Se detectan y manejan específicamente los errores relacionados con CORS.

5. **Rutas Protegidas**: El sistema de rutas garantiza que solo usuarios autenticados accedan a recursos protegidos.

6. **Renovación Automática**: Los tokens se renuevan automáticamente cuando es necesario, proporcionando una experiencia de usuario fluida.

Esta implementación demuestra cómo integrar efectivamente JWT, CORS y protecciones CSRF en una aplicación React moderna, proporcionando una base sólida de seguridad mientras mantiene una buena experiencia de usuario.

## Conclusión

La implementación conjunta de JWT, CORS y protecciones CSRF proporciona una base sólida de seguridad para aplicaciones web modernas. Cada mecanismo aborda aspectos específicos de seguridad:

- **JWT** maneja la autenticación y autorización de manera escalable
- **CORS** controla el acceso cross-origin de manera segura
- **CSRF** protege contra ataques de falsificación de solicitudes

La implementación correcta de estos tres mecanismos, siguiendo las mejores prácticas establecidas, es fundamental para desarrollar aplicaciones web seguras y confiables en el entorno actual de amenazas cibernéticas.

## Referencias

- RFC 7519: JSON Web Token (JWT)
- W3C CORS Specification
- OWASP CSRF Prevention Cheat Sheet
- MDN Web Security Documentation