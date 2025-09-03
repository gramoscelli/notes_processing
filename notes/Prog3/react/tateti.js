import { useState } from 'react';

export default function TicTacToe() {
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
    <div className="flex flex-col items-center p-8 bg-gray-100 min-h-screen">
      <h1 className="text-4xl font-bold mb-6 text-gray-800">Tic-Tac-Toe</h1>
      
      <div className="mb-4 text-xl font-semibold text-gray-700">
        {status}
      </div>

      <div className="grid grid-cols-3 gap-2 mb-6">
        {board.map((square, index) => (
          <button
            key={index}
            className="w-20 h-20 bg-white border-2 border-gray-400 text-3xl font-bold hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            onClick={() => handleClick(index)}
          >
            {square}
          </button>
        ))}
      </div>

      <button
        onClick={resetGame}
        className="px-6 py-2 bg-blue-500 text-white font-semibold rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Nuevo Juego
      </button>
    </div>
  );
}