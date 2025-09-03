# React Native para desarrolladores React

## ¿Qué es React Native?

React Native es un framework que permite desarrollar aplicaciones móviles nativas usando React y JavaScript. A diferencia de React para web, React Native compila a código nativo para iOS y Android.

**Filosofía clave**: "Learn once, write anywhere" - Aprende React una vez, úsalo en múltiples plataformas.

## Principales diferencias con React Web

### 1. Componentes básicos

En lugar de elementos HTML, React Native usa componentes específicos para móvil:

```jsx
// React Web
<div>
  <h1>Título</h1>
  <p>Párrafo de texto</p>
  <button onClick={handlePress}>Botón</button>
</div>

// React Native
<View>
  <Text style={styles.title}>Título</Text>
  <Text>Párrafo de texto</Text>
  <TouchableOpacity onPress={handlePress}>
    <Text>Botón</Text>
  </TouchableOpacity>
</View>
```

### 2. Componentes principales

| Componente | Propósito | Equivalente Web |
|------------|-----------|-----------------|
| `View` | Contenedor básico | `<div>` |
| `Text` | Mostrar texto | `<p>`, `<span>`, `<h1>`, etc. |
| `Image` | Mostrar imágenes | `<img>` |
| `ScrollView` | Área con scroll | `<div>` con overflow |
| `TouchableOpacity` | Elemento clickeable | `<button>` |
| `TextInput` | Campo de entrada | `<input>` |
| `FlatList` | Lista optimizada | `<ul>` con virtualización |

### 3. Estilos con StyleSheet

React Native usa un sistema de estilos similar a CSS pero con diferencias importantes:

```jsx
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
  }
});
```

**Diferencias clave en estilos**:

- Se usa `flex` por defecto (no `display: flex`)
- Propiedades en camelCase: `backgroundColor` en lugar de `background-color`
- No hay herencia de estilos (excepto en `Text`)
- Dimensiones sin unidades (se asumen píxeles)

## Configuración inicial

### Opciones para crear proyectos React Native

Existen dos formas principales de crear proyectos React Native:

#### 1. Expo CLI (Recomendado para principiantes)

**Ventajas de Expo:**

- ✅ Configuración cero - no necesitas Android Studio ni Xcode inicialmente
- ✅ Desarrollo rápido con Expo Go en tu teléfono
- ✅ Muchas APIs nativas pre-configuradas (cámara, ubicación, notificaciones)
- ✅ Builds automáticos en la nube
- ✅ Actualizaciones over-the-air (OTA)
- ✅ Documentación excelente y comunidad activa

**Limitaciones de Expo:**

- ❌ No puedes usar librerías nativas personalizadas
- ❌ Tamaño de app más grande
- ❌ Menos control sobre configuraciones nativas

```bash
# Instalar Expo CLI
npm install -g @expo/cli

# Crear nuevo proyecto con JavaScript (JSX)
npx create-expo-app MiApp --template blank
cd MiApp

# Ejecutar en desarrollo
npx expo start
```

#### 2. React Native CLI (Para desarrolladores avanzados)

**Ventajas de React Native CLI:**

- ✅ Control total sobre el proyecto
- ✅ Acceso completo a APIs nativas
- ✅ Puedes usar cualquier librería nativa
- ✅ Tamaño de app más pequeño

**Desventajas:**

- ❌ Configuración compleja (Android Studio + Xcode)
- ❌ Más tiempo de setup inicial
- ❌ Más propenso a errores de configuración

```bash
# Instalar React Native CLI
npm install -g @react-native-community/cli

# Crear nuevo proyecto
npx react-native@latest init MiApp
cd MiApp

# Ejecutar en desarrollo (requiere emulador/dispositivo configurado)
npx react-native run-android
npx react-native run-ios
```

**Recomendación**: Para aprender React Native, usa **Expo**. Puedes migrar a React Native CLI más adelante si necesitas funcionalidades nativas específicas.

## Cómo ejecutar tu aplicación

### Opción 1: Expo Go (Más fácil - Recomendada para principiantes)

Esta es la forma más simple sin necesidad de configurar Android SDK:

1. **Instala Expo Go en tu teléfono**:
   
   - Android: [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)
   - iOS: [App Store](https://apps.apple.com/app/expo-go/id982107779)

2. **Ejecuta el proyecto**:
   ```bash
   npx expo start
   ```

3. **Conecta tu dispositivo**:
   
   - Escanea el código QR que aparece en la terminal con la cámara (iOS) o con la app Expo Go (Android)
   - Asegúrate de que tu teléfono y computadora estén en la misma red WiFi

### Opción 2: Modo túnel (Solución para problemas de conectividad)

Si tienes problemas de conectividad entre tu computadora y teléfono (común en Linux con Node.js v17+):

```bash
npx expo start --tunnel
```

Esta opción:
- Crea un túnel público usando ngrok
- Funciona independientemente de configuraciones IPv4/IPv6
- Es especialmente útil cuando el sistema usa IPv6 pero el teléfono necesita IPv4
- Permite conectar desde cualquier red

### Opción 3: Desarrollo en navegador web

Para desarrollo inicial, puedes probar tu app en el navegador:

```bash
npx expo start --web
```

**Recomendación**: 
- Para desarrollo normal: Empieza con **Expo Go** en tu teléfono
- Para problemas de conectividad: Usa **modo túnel** (`--tunnel`)

### Estructura básica de un proyecto Expo

```
MiApp/
├── App.js              # Componente principal
├── app.json           # Configuración de la app
├── package.json       # Dependencias
├── components/        # Componentes reutilizables
├── screens/          # Pantallas de la app
└── assets/           # Imágenes y recursos
```

## Ejemplo básico: Primera app

```jsx
// App.js
import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert
} from 'react-native';

export default function App() {
  const [nombre, setNombre] = useState('');
  const [contador, setContador] = useState(0);

  const saludar = () => {
    if (nombre.trim()) {
      Alert.alert('Saludo', `¡Hola ${nombre}!`);
    } else {
      Alert.alert('Error', 'Por favor ingresa tu nombre');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Mi Primera App</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Ingresa tu nombre"
        value={nombre}
        onChangeText={setNombre}
      />
      
      <TouchableOpacity style={styles.button} onPress={saludar}>
        <Text style={styles.buttonText}>Saludar</Text>
      </TouchableOpacity>
      
      <View style={styles.counter}>
        <Text style={styles.counterText}>Contador: {contador}</Text>
        <TouchableOpacity 
          style={styles.smallButton} 
          onPress={() => setContador(contador + 1)}
        >
          <Text style={styles.buttonText}>+</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 30,
    color: '#333',
  },
  input: {
    width: '100%',
    height: 50,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    paddingHorizontal: 15,
    marginBottom: 20,
    backgroundColor: 'white',
  },
  button: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
    marginBottom: 20,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  counter: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 15,
  },
  counterText: {
    fontSize: 18,
    color: '#333',
  },
  smallButton: {
    backgroundColor: '#34C759',
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
```

## Navegación entre pantallas

Para navegar entre pantallas, se usa React Navigation:

```bash
npm install @react-navigation/native @react-navigation/stack
npx expo install react-native-screens react-native-safe-area-context
```

```jsx
// App.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from './screens/HomeScreen';
import DetailScreen from './screens/DetailScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Detail" component={DetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// screens/HomeScreen.js
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Pantalla Principal</Text>
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.navigate('Detail', { mensaje: 'Hola desde Home' })}
      >
        <Text style={styles.buttonText}>Ir a Detalle</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 30,
    color: '#333',
  },
  button: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

// screens/DetailScreen.js
import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function DetailScreen({ route, navigation }) {
  const { mensaje } = route.params || {};

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Pantalla de Detalle</Text>
      
      {mensaje && (
        <View style={styles.messageContainer}>
          <Text style={styles.messageLabel}>Mensaje recibido:</Text>
          <Text style={styles.messageText}>{mensaje}</Text>
        </View>
      )}
      
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.buttonText}>Volver</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f8f9fa',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 30,
    color: '#333',
  },
  messageContainer: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 8,
    marginBottom: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  messageLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
  },
  messageText: {
    fontSize: 18,
    color: '#333',
    fontStyle: 'italic',
  },
  button: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
  },
});
```

## Listas optimizadas con FlatList

Para listas grandes, siempre usa `FlatList` en lugar de `ScrollView`:

```jsx
import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';

const datos = [
  { id: '1', nombre: 'Juan', edad: 25 },
  { id: '2', nombre: 'María', edad: 30 },
  { id: '3', nombre: 'Pedro', edad: 28 },
];

export default function ListaUsuarios() {
  const renderItem = ({ item }) => (
    <View style={styles.item}>
      <Text style={styles.nombre}>{item.nombre}</Text>
      <Text style={styles.edad}>{item.edad} años</Text>
    </View>
  );

  return (
    <FlatList
      data={datos}
      renderItem={renderItem}
      keyExtractor={item => item.id}
      style={styles.lista}
    />
  );
}

const styles = StyleSheet.create({
  lista: {
    flex: 1,
    padding: 20,
  },
  item: {
    backgroundColor: 'white',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  nombre: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  edad: {
    fontSize: 14,
    color: '#666',
  },
});
```

## APIs nativas comunes

React Native proporciona acceso a funcionalidades nativas:

```jsx
import { Alert, Dimensions, Platform } from 'react-native';

// Alertas nativas
Alert.alert('Título', 'Mensaje', [
  { text: 'Cancelar', style: 'cancel' },
  { text: 'OK', onPress: () => console.log('OK') }
]);

// Dimensiones de la pantalla
const { width, height } = Dimensions.get('window');

// Detectar plataforma
if (Platform.OS === 'ios') {
  // Código específico para iOS
} else {
  // Código específico para Android
}
```

## Consumo de APIs

React Native permite consumir APIs REST usando `fetch` igual que en React web:

```jsx
// components/UserList.js
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Alert
} from 'react-native';

export default function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await fetch('https://jsonplaceholder.typicode.com/users');
      
      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor');
      }
      
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
      Alert.alert('Error', 'No se pudieron cargar los usuarios');
    } finally {
      setLoading(false);
    }
  };

  const renderUser = ({ item }) => (
    <View style={styles.userCard}>
      <Text style={styles.userName}>{item.name}</Text>
      <Text style={styles.userEmail}>{item.email}</Text>
      <Text style={styles.userPhone}>{item.phone}</Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Cargando usuarios...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Lista de Usuarios</Text>
      <FlatList
        data={users}
        renderItem={renderUser}
        keyExtractor={item => item.id.toString()}
        showsVerticalScrollIndicator={false}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#333',
  },
  userCard: {
    backgroundColor: 'white',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  userName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  userEmail: {
    fontSize: 14,
    color: '#666',
    marginBottom: 3,
  },
  userPhone: {
    fontSize: 14,
    color: '#666',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
});
```

### Conceptos importantes del consumo de APIs:

- **async/await**: Manejo de operaciones asíncronas
- **try/catch**: Manejo de errores
- **ActivityIndicator**: Indicador de carga nativo
- **FlatList**: Lista optimizada para grandes cantidades de datos
- **Alert**: Alertas nativas del sistema

### APIs populares para practicar:

- **JSONPlaceholder**: `https://jsonplaceholder.typicode.com/` (usuarios, posts, comentarios)
- **OpenWeatherMap**: Datos meteorológicos
- **The Cat API**: `https://api.thecatapi.com/v1/images/search` (imágenes de gatos)
- **REST Countries**: `https://restcountries.com/v3.1/all` (información de países)

1. **Usa StyleSheet.create()** para mejor rendimiento
2. **FlatList para listas grandes** en lugar de ScrollView
3. **Optimiza imágenes** usando formatos web (WebP) cuando sea posible
4. **Maneja el estado** igual que en React web
5. **Usa hooks** como `useState`, `useEffect`, etc.
6. **Separa componentes** en archivos diferentes
7. **Prueba en ambas plataformas** (iOS y Android)

## Diferencias de desarrollo

| Aspecto | React Web | React Native |
|---------|-----------|--------------|
| Depuración | DevTools del navegador | React Native Debugger |
| Hot Reload | Sí | Fast Refresh |
| CSS | Archivos CSS/SCSS | StyleSheet API |
| Routing | React Router | React Navigation |
| Almacenamiento | localStorage | AsyncStorage |

## Recursos útiles

- **Documentación oficial**: https://reactnative.dev/
- **Expo**: https://expo.dev/
- **React Navigation**: https://reactnavigation.org/
- **UI Libraries**: NativeBase, Shoutem UI, React Native Elements

## Ejercicios propuestos

1. **App de tareas**: Lista de tareas con agregar/eliminar
2. **Calculadora**: Calculadora básica con operaciones
3. **App del clima**: Consumir API meteorológica
4. **Lista de contactos**: CRUD completo con navegación

