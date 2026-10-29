# Solución al error del clic del del botón `borrar`
El error sucedió porque al pulsa el botón, también activamos el `<li>`: hay otro `onClick` que llama a `toggleTask(i)`. Por esto, cuando se hace clic en el botón “borrar”, ese clic **se deriva** luego hacia el `<li>` y se ejecuta `toggleTask`. Como ambos llaman a `setTasks(...)` con el estado _“viejo”_, el llamado a `toggleTask` **evita** (accidentalmente) la eliminación y la tarea no se borrará. 

Arreglos rápidos:

1. **Evitar la deriva** hacia `toggleTask` desde la llamada `onclick` del botón borrar usando `e.stopPropagation()`.
```tsx
            <button
              onClick={(e) => {
                e.stopPropagation();   // ← evita que también se dispare toggleTask
                eliminar(t.id);
              }}
            >
              borrar
            </button>
```
2. Usar la **forma funcional** de `setTasks` para evitar estados obsoletos.
```tsx

  const addTask = () => {
    if (text.trim()) {
      setTasks(prev => [...prev, { text, done: false }]); 
      setText('');
    }
  };

  const toggleTask = (id: string) => {
    setTasks(prev => prev.map((t, ind) => ind === id ? { ...t, done: !t.done } : t));
  };

  const eliminar = (id: string) => {
    setTasks(prev => prev.filter((t, ind) => ind !== id);
  };

```
3. (Opcional pero recomendable) Dejar de usar el índice como `key` y darle un `id` único a cada tarea. Esta modificación debe incluir el punto 1 o el punto 2, o incluir _ambos_ puntos:
```tsx
type Task = { id: string; text: string; done: boolean }; // Agregamos un id al estado de la tarea

export default function TodoApp() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [text, setText] = useState('');

  const addTask = () => {
    if (text.trim()) {
      setTasks(prev => [...prev, { id: crypto.randomUUID(), text, done: false }]); // cargamos un valor aleatorio en el id
      setText('');
    }
  };

  const toggleTask = (id: string) => {
    setTasks(prev => prev.map(t => t.id === id ? { ...t, done: !t.done } : t));  // usamos una función 
  };

  const eliminar = (id: string) => {
    setTasks(prev => prev.filter(t => t.id !== id));  // acá también usamos una función
  };

  return (
    <div>
      {tasks.length === 0 && <p>No hay tareas</p>}
      <input
        placeholder="Nueva tarea"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={addTask}>Agregar</button>

      <ul>
        {tasks.map((t) => (
          <li
            key={t.id}
            onClick={() => toggleTask(t.id)}
            style={{ textDecoration: t.done ? 'line-through' : 'none', cursor: 'pointer' }}
          >
            {t.text}
            <button
              onClick={(e) => {
                e.stopPropagation();   // ← evita que también se dispare toggleTask
                eliminar(t.id);
              }}
            >
              borrar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

