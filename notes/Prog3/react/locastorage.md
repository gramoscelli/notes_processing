# Agregando localStorage al Tic-Tac-Toe

## Introducción

El localStorage es una API del navegador que permite guardar datos de forma persistente en el dispositivo del usuario. A diferencia del estado de React que se pierde al recargar la página, localStorage mantiene los datos hasta que el usuario los borre manualmente.

## ¿Por qué Usar localStorage?

### Ventajas
- **Persistencia**: Los datos sobreviven al cierre del navegador
- **Experiencia de usuario**: El juego continúa donde se quedó
- **Sin servidor**: No necesitamos base de datos para guardar progreso simple
- **Fácil implementación**: API simple de usar

### Casos de Uso Comunes
- Guardar configuraciones del usuario
- Mantener carritos de compra
- Recordar progreso en juegos
- Guardar preferencias de tema/idioma

## Implementación en el Tic-Tac-Toe

### 1. Estructura de Datos a Guardar

```javascript
const gameState = {
  board: [null, null, 'X', 'O', null, null, null, null, null],
  isXNext: false,
  gameHistory: ['X', 'O', 'X'],  // opcional: historial de ganadores
  gamesPlayed: 15                // opcional: estadísticas
};
```

### 2. Hook useEffect para Cargar Datos

```javascript
import { useState, useEffect } from 'react';

const [board, setBoard] = useState(Array(9).fill(null));
const [isXNext, setIsXNext] = useState(true);

// Cargar datos al inicializar el componente
useEffect(() => {
  const savedGame = localStorage.getItem('ticTacToeGame');
  if (savedGame) {
    const gameState = JSON.parse(savedGame);
    setBoard(gameState.board);
    setIsXNext(gameState.isXNext);
  }
}, []); // Array vacío = solo se ejecuta una vez al montar
```

**Conceptos clave:**
- `useEffect` se ejecuta después del primer renderizado
- Dependency array vacío `[]` significa que solo se ejecuta una vez
- `JSON.parse()` convierte string a objeto JavaScript

### 3. Guardar Estado Automáticamente

```javascript
// Guardar datos cada vez que cambie el estado
useEffect(() => {
  const gameState = {
    board,
    isXNext
  };
  localStorage.setItem('ticTacToeGame', JSON.stringify(gameState));
}, [board, isXNext]); // Se ejecuta cuando board o isXNext cambien
```

**Puntos importantes:**
- Se ejecuta cada vez que cambian `board` o `isXNext`
- `JSON.stringify()` convierte el objeto a string para almacenarlo
- Se guarda automáticamente sin intervención del usuario

### 4. Función de Reinicio Mejorada

```javascript
const resetGame = () => {
  setBoard(Array(9).fill(null));
  setIsXNext(true);
  // Opcional: también limpiar localStorage
  localStorage.removeItem('ticTacToeGame');
};

// O para limpiar solo el juego actual pero mantener estadísticas:
const resetCurrentGame = () => {
  const savedData = JSON.parse(localStorage.getItem('ticTacToeGame') || '{}');
  const newGameState = {
    ...savedData, // mantener estadísticas si existen
    board: Array(9).fill(null),
    isXNext: true
  };
  localStorage.setItem('ticTacToeGame', JSON.stringify(newGameState));
  setBoard(Array(9).fill(null));
  setIsXNext(true);
};
```

## Manejo de Errores y Edge Cases

### 1. Verificación de Soporte del Navegador

```javascript
const isLocalStorageAvailable = () => {
  try {
    const test = '__localStorage_test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (e) {
    return false;
  }
};
```

### 2. Manejo de Datos Corruptos

```javascript
useEffect(() => {
  try {
    const savedGame = localStorage.getItem('ticTacToeGame');
    if (savedGame) {
      const gameState = JSON.parse(savedGame);
      
      // Validar que los datos sean correctos
      if (gameState.board && Array.isArray(gameState.board) && gameState.board.length === 9) {
        setBoard(gameState.board);
        setIsXNext(gameState.isXNext ?? true);
      }
    }
  } catch (error) {
    console.warn('No se pudieron cargar los datos guardados:', error);
    // Usar valores por defecto si hay error
    localStorage.removeItem('ticTacToeGame');
  }
}, []);
```

## Características Avanzadas

### 1. Estadísticas del Jugador

```javascript
const updateStats = (winner) => {
  const stats = JSON.parse(localStorage.getItem('gameStats') || '{}');
  const newStats = {
    gamesPlayed: (stats.gamesPlayed || 0) + 1,
    xWins: stats.xWins || 0,
    oWins: stats.oWins || 0,
    draws: stats.draws || 0
  };

  if (winner === 'X') newStats.xWins++;
  else if (winner === 'O') newStats.oWins++;
  else newStats.draws++;

  localStorage.setItem('gameStats', JSON.stringify(newStats));
};
```

### 2. Múltiples Juegos Guardados

```javascript
const saveGameToSlot = (slotNumber) => {
  const gameState = { board, isXNext, timestamp: Date.now() };
  localStorage.setItem(`ticTacToe_slot_${slotNumber}`, JSON.stringify(gameState));
};

const loadGameFromSlot = (slotNumber) => {
  const savedGame = localStorage.getItem(`ticTacToe_slot_${slotNumber}`);
  if (savedGame) {
    const gameState = JSON.parse(savedGame);
    setBoard(gameState.board);
    setIsXNext(gameState.isXNext);
  }
};
```

## Consideraciones de Rendimiento

### 1. Throttling de Guardado

```javascript
import { useCallback, useRef } from 'react';

const useDebouncedSave = (delay = 500) => {
  const timeoutRef = useRef(null);
  
  return useCallback((data) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    
    timeoutRef.current = setTimeout(() => {
      localStorage.setItem('ticTacToeGame', JSON.stringify(data));
    }, delay);
  }, [delay]);
};
```

### 2. Límites de Almacenamiento

```javascript
const getStorageSize = () => {
  let total = 0;
  for (let key in localStorage) {
    if (localStorage.hasOwnProperty(key)) {
      total += localStorage[key].length + key.length;
    }
  }
  return total;
};

// Verificar si hay espacio antes de guardar
const saveIfSpace = (key, data) => {
  const currentSize = getStorageSize();
  const newDataSize = JSON.stringify(data).length;
  
  // localStorage típicamente tiene límite de ~5-10MB
  if (currentSize + newDataSize < 5 * 1024 * 1024) {
    localStorage.setItem(key, JSON.stringify(data));
  } else {
    console.warn('No hay suficiente espacio en localStorage');
  }
};
```

## Mejores Prácticas

### 1. Nombres de Claves Consistentes
```javascript
const STORAGE_KEYS = {
  CURRENT_GAME: 'ticTacToe_currentGame',
  STATS: 'ticTacToe_stats',
  SETTINGS: 'ticTacToe_settings'
};
```

### 2. Funciones de Utilidad
```javascript
const storageUtils = {
  save: (key, data) => {
    try {
      localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
      console.error('Error guardando en localStorage:', error);
    }
  },
  
  load: (key, defaultValue = null) => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.error('Error cargando de localStorage:', error);
      return defaultValue;
    }
  },
  
  remove: (key) => {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('Error removiendo de localStorage:', error);
    }
  }
};
```

## Alternativas a localStorage

### 1. sessionStorage
- Se borra al cerrar la pestaña
- Útil para datos temporales de la sesión

### 2. IndexedDB
- Para aplicaciones más complejas
- Maneja grandes cantidades de datos
- Soporte para consultas avanzadas

### 3. Cookies
- Para datos que necesitan enviarse al servidor
- Límite de tamaño muy pequeño (4KB)

## Conclusión

Agregar localStorage al Tic-Tac-Toe mejora significativamente la experiencia del usuario al mantener el progreso del juego. Los conceptos aprendidos aquí se aplican a muchas otras aplicaciones web donde necesitamos persistencia de datos del lado del cliente.

**Puntos clave para recordar:**
- Siempre manejar errores al usar localStorage
- Validar datos antes de usarlos
- Considerar el rendimiento en aplicaciones complejas
- Usar nombres de claves consistentes y descriptivos