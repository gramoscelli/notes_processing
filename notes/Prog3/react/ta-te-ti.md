# Explicación del Tic-Tac-Toe en React

## Introducción

Este proyecto implementa un juego de Tic-Tac-Toe (tres en raya) usando React con hooks. Es un ejemplo perfecto para aprender conceptos fundamentales de React como estado, eventos y renderizado condicional.

## Estructura del Código

### 1. Importaciones y Estado Inicial

```javascript
import { useState } from 'react';

const [board, setBoard] = useState(Array(9).fill(null));
const [isXNext, setIsXNext] = useState(true);
```

**¿Por qué esta estructura?**
- Usamos un array de 9 elementos para representar el tablero 3x3
- `isXNext` controla de quién es el turno (true = X, false = O)
- `useState` es el hook que nos permite manejar estado en componentes funcionales

### 2. Función para Detectar Ganador

```javascript
const calculateWinner = (squares) => {
  const lines = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // filas
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // columnas
    [0, 4, 8], [2, 4, 6]             // diagonales
  ];
  // ...
};
```

**Conceptos clave:**
- Define todas las combinaciones ganadoras posibles
- Recorre cada combinación para verificar si hay tres símbolos iguales
- Retorna el ganador ('X' o 'O') o null si no hay ganador

### 3. Manejo de Clics

```javascript
const handleClick = (index) => {
  if (board[index] || calculateWinner(board)) {
    return; // Prevenir movimientos inválidos
  }

  const newBoard = [...board];  // Crear copia del estado
  newBoard[index] = isXNext ? 'X' : 'O';
  setBoard(newBoard);
  setIsXNext(!isXNext);
};
```

**Principios importantes:**
- **Inmutabilidad**: Creamos una nueva copia del array en lugar de modificar el original
- **Validación**: Verificamos que la casilla esté vacía y no haya ganador
- **Cambio de turno**: Alternamos entre X y O después de cada movimiento

### 4. Renderizado del Tablero

```javascript
<div className="grid grid-cols-3 gap-2 mb-6">
  {board.map((square, index) => (
    <button
      key={index}
      onClick={() => handleClick(index)}
    >
      {square}
    </button>
  ))}
</div>
```

**Técnicas utilizadas:**
- `map()` para renderizar cada casilla dinámicamente
- `key` prop para optimización de React
- Event handlers con parámetros usando arrow functions

## Conceptos de React Aplicados

### Hooks
- **useState**: Manejo de estado local del componente
- **No necesitamos useEffect**: El estado se actualiza de forma síncrona

### Renderizado Condicional
```javascript
let status;
if (winner) {
  status = `¡Ganador: ${winner}!`;
} else if (isBoardFull) {
  status = '¡Empate!';
} else {
  status = `Siguiente jugador: ${isXNext ? 'X' : 'O'}`;
}
```

### Props y Event Handling
- Cada botón recibe su propio `onClick` handler
- Usamos closures para pasar el índice correcto

## Flujo del Juego

1. **Inicialización**: Tablero vacío, turno de X
2. **Clic del usuario**: Se ejecuta `handleClick` con el índice de la casilla
3. **Validación**: Verificar si el movimiento es válido
4. **Actualización**: Modificar el estado del tablero y cambiar turno
5. **Re-renderizado**: React actualiza la interfaz automáticamente
6. **Verificación**: Comprobar si hay ganador o empate

## Ventajas de esta Implementación

### Simplicidad
- Solo dos estados simples
- Lógica clara y fácil de seguir
- Sin dependencias externas

### Escalabilidad
- Fácil de modificar el tamaño del tablero
- Simple agregar nuevas características
- Código modular y reutilizable

### Buenas Prácticas
- **Inmutabilidad**: No mutar el estado directamente
- **Separación de responsabilidades**: Cada función tiene un propósito específico
- **Validación**: Prevenir estados inválidos

## Posibles Extensiones

1. **Historial de movimientos**: Poder deshacer jugadas
2. **Jugador vs IA**: Implementar algoritmo para jugador automático
3. **Marcador**: Llevar cuenta de victorias
4. **Animaciones**: Agregar transiciones visuales
5. **Multijugador online**: Conexión con otros jugadores

## Conceptos para Profundizar

- **Virtual DOM**: Cómo React optimiza las actualizaciones
- **Lifting State Up**: Mover estado a componentes padre cuando sea necesario
- **Pure Functions**: Funciones sin efectos secundarios como `calculateWinner`
- **Controlled Components**: Todos los inputs controlados por React state

Archivo `App.css`:

```css
/* Tic‑Tac‑Toe – app.css */

/* Layout wrapper */
.game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  min-height: 100vh;
  padding: 1rem;
  background: #f1f5f9; /* slate‑50 */
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif;
}

/* Heading */
.game-title {
  margin: 0.25rem 0 0.75rem;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b; /* slate‑800 */
  text-align: center;
}

/* Status banners */
.game-status {
  min-height: 2.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  text-align: center;
  user-select: none;
}

.current-player {
  background: #e2e8f0; /* slate‑200 */
  color: #334155;       /* slate‑700 */
}

.winner {
  background: #16a34a; /* green‑600 */
  color: #ffffff;
}

.draw {
  background: #fbbf24; /* amber‑400 */
  color: #433520;       /* neutral dark for contrast */
}

/* Game board grid */
.game-board {
  display: grid;
  grid-template-columns: repeat(3, 100px);
  gap: 0.5rem;
}

@media (max-width: 500px) {
  .game-board {
    grid-template-columns: repeat(3, 80px);
  }
}

/* Squares */
.game-square {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 700;
  background: #ffffff;
  border: 2px solid #334155; /* slate‑700 */
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  user-select: none;
}

@media (max-width: 500px) {
  .game-square {
    width: 80px;
    height: 80px;
    font-size: 2rem;
  }
}

.game-square:hover:not(:disabled) {
  background: #e2e8f0; /* slate‑200 */
  transform: scale(1.05);
}

.game-square:disabled {
  background: #f1f5f9; /* slate‑50 */
  cursor: default;
}

/* Player mark colours */
.game-square.x {
  color: #1d4ed8; /* blue‑600 */
}

.game-square.o {
  color: #dc2626; /* red‑600 */
}

/* Buttons */
.game-button {
  margin-top: 0.5rem;
  padding: 0.6rem 1.25rem;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  background: #3b82f6; /* blue‑500 */
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

.game-button:hover {
  background: #2563eb; /* blue‑600 */
}

.game-button:active {
  transform: scale(0.97);
}

.reset-button {
  /* additional styles reserved for future buttons */
}
}
```

Archivo `App.js`:

```jsx
import { useState } from 'react';
import './App.css'; 

function App() {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [isXNext, setIsXNext] = useState(true);

  const calculateWinner = (squares) => {
    const lines = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8], // filas
      [0, 3, 6], [1, 4, 7], [2, 5, 8], // columnas
      [0, 4, 8], [2, 4, 6]             // diagonales
    ];
    
    for (let i = 0; i < lines.length; i++) {
      const [a, b, c] = lines[i];
      if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
        return squares[a];
      }
    }
    return null;
  };

  const handleClick = (index) => {
    if (board[index] || calculateWinner(board)) {
      return; // no hacer nada si ya hay un valor o ya hay ganador
    }

    const newBoard = [...board];
    newBoard[index] = isXNext ? 'X' : 'O';
    setBoard(newBoard);
    setIsXNext(!isXNext);
  };

  const resetGame = () => {
    setBoard(Array(9).fill(null));
    setIsXNext(true);
  };

  const winner = calculateWinner(board);
  const isBoardFull = board.every(square => square !== null);
  
  let status;
  if (winner) {
    status = `¡Ganador: ${winner}!`;
  } else if (isBoardFull) {
    status = '¡Empate!';
  } else {
    status = `Siguiente jugador: ${isXNext ? 'X' : 'O'}`;
  }

  return (
    <div className="game-container">
      <h1 className="game-title">Tic-Tac-Toe</h1>
      
      <div className={`game-status ${winner ? 'winner' : isBoardFull ? 'draw' : 'current-player'}`}>
        {status}
      </div>

      <div className="game-board">
        {board.map((square, index) => (
          <button
            key={index}
            className={`game-square ${square ? square.toLowerCase() : ''}`}
            onClick={() => handleClick(index)}
            disabled={square || winner}
          >
            {square}
          </button>
        ))}
      </div>

      <button
        onClick={resetGame}
        className="game-button reset-button"
      >
        Nuevo Juego
      </button>
    </div>
  );
}

export default App;
```