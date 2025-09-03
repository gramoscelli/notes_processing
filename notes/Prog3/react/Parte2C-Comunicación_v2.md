# Parte 2C: Comunicación entre componentes y fórmularios

## 🔄 Comunicación entre Componentes

> **💡 Concepto clave**: En React, los componentes necesitan comunicarse entre sí para compartir datos y funcionalidad. Hay diferentes patrones según la relación entre componentes.

### Props: Comunicación de Padre a Hijo

> **📝 Explicación**: Las props son la forma más básica de pasar información de un componente padre a sus hijos. Es como entregar parámetros a una función - el hijo recibe datos que puede usar pero no modificar directamente.

```jsx
// Componente Padre
function Parent() {
  const [message, setMessage] = useState('Hola desde el padre');
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <h1>Componente Padre</h1>
      <input 
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Mensaje para el hijo"
      />
      <button onClick={() => setCount(count + 1)}>
        Incrementar: {count}
      </button>
      
      {/* Pasando props al hijo */}
      <Child 
        message={message}
        count={count}
        isEven={count % 2 === 0}
      />
    </div>
  );
}

// Componente Hijo
function Child({ message, count, isEven }) {
  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', margin: '10px' }}>
      <h2>Componente Hijo</h2>
      <p>Mensaje recibido: {message}</p>
      <p>Contador recibido: {count}</p>
      <p>El número es {isEven ? 'par' : 'impar'}</p>
    </div>
  );
}
```

### Callbacks: Comunicación de Hijo a Padre

> **📝 Explicación**: Los callbacks son funciones que el padre pasa al hijo para que este pueda "comunicarse hacia arriba". El hijo ejecuta la función cuando algo sucede, permitiendo que el padre reaccione a eventos del hijo.

```jsx
// Componente Padre
function TodoApp() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'Aprender React', completed: false },
    { id: 2, text: 'Hacer ejercicios', completed: true }
  ]);
  
  // 🔧 Estas funciones se pasan como callbacks a los hijos
  const addTodo = (text) => {
    const newTodo = {
      id: Date.now(),
      text,
      completed: false
    };
    setTodos([...todos, newTodo]);
  };
  
  const toggleTodo = (id) => {
    setTodos(todos.map(todo => 
      todo.id === id 
        ? { ...todo, completed: !todo.completed }
        : todo
    ));
  };
  
  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };
  
  return (
    <div>
      <h1>Lista de Tareas</h1>
      
      {/* Componente para agregar todos */}
      <AddTodo onAddTodo={addTodo} />
      
      {/* Lista de todos */}
      <div>
        {todos.map(todo => (
          <TodoItem 
            key={todo.id}
            todo={todo}
            onToggle={toggleTodo}
            onDelete={deleteTodo}
          />
        ))}
      </div>
    </div>
  );
}

// Componente hijo para agregar todos
function AddTodo({ onAddTodo }) {
  const [text, setText] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      // 🔥 Aquí llamamos al callback del padre
      onAddTodo(text.trim());
      setText('');
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Nueva tarea..."
      />
      <button type="submit">Agregar</button>
    </form>
  );
}

// Componente hijo para cada todo
function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center', 
      padding: '5px',
      textDecoration: todo.completed ? 'line-through' : 'none'
    }}>
      <input 
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)} // 🔥 Callback al padre
      />
      <span style={{ flex: 1, marginLeft: '10px' }}>
        {todo.text}
      </span>
      <button onClick={() => onDelete(todo.id)}> {/* 🔥 Callback al padre */}
        Eliminar
      </button>
    </div>
  );
}
```

### Lifting State Up (Elevar el Estado)

> **📝 Explicación**: Cuando dos componentes hermanos necesitan compartir datos, movemos el estado al componente padre más cercano. Esto se llama "elevar el estado" - el padre maneja los datos y ambos hijos pueden acceder a ellos.

```jsx
// Estado compartido entre hermanos
function TemperatureApp() {
  // 🎯 El estado vive aquí, en el padre común
  const [temperature, setTemperature] = useState('');
  
  return (
    <div>
      <h1>Calculadora de Temperatura</h1>
      {/* Ambos hijos comparten el mismo estado */}
      <CelsiusInput 
        temperature={temperature}
        onTemperatureChange={setTemperature}
      />
      <FahrenheitInput 
        temperature={temperature}
        onTemperatureChange={setTemperature}
      />
      <BoilingVerdict celsius={parseFloat(temperature)} />
    </div>
  );
}

function CelsiusInput({ temperature, onTemperatureChange }) {
  return (
    <fieldset>
      <legend>Temperatura en Celsius:</legend>
      <input 
        value={temperature}
        onChange={(e) => onTemperatureChange(e.target.value)}
      />
    </fieldset>
  );
}

function FahrenheitInput({ temperature, onTemperatureChange }) {
  // 🔢 Convertimos de Celsius a Fahrenheit para mostrar
  const fahrenheit = temperature ? (parseFloat(temperature) * 9/5) + 32 : '';
  
  return (
    <fieldset>
      <legend>Temperatura en Fahrenheit:</legend>
      <input 
        value={fahrenheit}
        onChange={(e) => {
          // 🔢 Convertimos de Fahrenheit a Celsius antes de actualizar
          const celsius = (parseFloat(e.target.value) - 32) * 5/9;
          onTemperatureChange(celsius.toString());
        }}
      />
    </fieldset>
  );
}

function BoilingVerdict({ celsius }) {
  if (celsius >= 100) {
    return <p>El agua herviría.</p>;
  }
  return <p>El agua NO herviría.</p>;
}
```

## 📝 Manejo de Formularios

> **💡 Concepto clave**: En React manejamos formularios de manera diferente a HTML tradicional. En lugar de que el navegador controle los campos, React mantiene el control total del estado del formulario.

### Diferencia con HTML Tradicional

**HTML tradicional:**
```html
<!-- El navegador maneja el estado del input -->
<form>
  <input type="text" id="name" />
  <button type="submit">Enviar</button>
</form>

<script>
// Solo podemos leer el valor cuando necesitamos
document.querySelector('form').addEventListener('submit', (e) => {
  const name = document.getElementById('name').value;
  console.log(name);
});
</script>
```

**React (Componentes Controlados):**
```jsx
// React controla el estado del input
function ContactForm() {
  const [name, setName] = useState(''); // React tiene el valor
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(name); // Ya tenemos el valor
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text"
        value={name}           // React controla el valor
        onChange={(e) => setName(e.target.value)} // React maneja los cambios
      />
      <button type="submit">Enviar</button>
    </form>
  );
}
```

### Componentes Controlados vs No Controlados

> **📝 Explicación**: Un componente controlado tiene su valor controlado por React state. Un componente no controlado deja que el navegador maneje el valor. **Siempre prefiere componentes controlados** porque te dan más control y permiten validación en tiempo real.

```jsx
function FormComparison() {
  const [controlledValue, setControlledValue] = useState('');
  
  return (
    <div>
      <h3>✅ Componente Controlado (Recomendado)</h3>
      <input 
        type="text"
        value={controlledValue}                    // React controla el valor
        onChange={(e) => setControlledValue(e.target.value)}
        placeholder="Escribe aquí..."
      />
      <p>Valor actual: {controlledValue}</p>
      
      <h3>❌ Componente No Controlado (Evitar)</h3>
      <input 
        type="text"
        placeholder="Escribe aquí también..."     // El navegador controla el valor
      />
      <p>No sabemos qué valor tiene hasta que consultemos el DOM</p>
    </div>
  );
}
```

### Formulario Completo con Múltiples Campos

> **📝 Explicación**: En formularios grandes, es común usar un objeto para manejar todos los datos y una función genérica para todos los cambios. Esto evita tener muchas variables de estado separadas.

```jsx
function UserRegistrationForm() {
  // 🎯 Un solo objeto para todos los datos del formulario
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    age: '',
    country: 'mexico',
    newsletter: false,
    terms: false
  });
  
  // 🔧 Manejador genérico para todos los inputs
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    setFormData(prevData => ({
      ...prevData,
      // Para checkboxes usamos 'checked', para el resto 'value'
      [name]: type === 'checkbox' ? checked : value
    }));
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('📋 Datos del formulario:', formData);
    
    // Aquí enviarías los datos a un servidor
    // fetch('/api/register', { method: 'POST', body: JSON.stringify(formData) })
  };
  
  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: '0 auto' }}>
      <h2>📝 Registro de Usuario</h2>
      
      {/* Inputs de texto */}
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="firstName">Nombre:</label>
        <input 
          type="text"
          id="firstName"
          name="firstName"                        // 🔑 Importante: coincide con la key del estado
          value={formData.firstName}
          onChange={handleChange}                 // 🔧 Función genérica
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        />
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="lastName">Apellido:</label>
        <input 
          type="text"
          id="lastName"
          name="lastName"
          value={formData.lastName}
          onChange={handleChange}
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        />
      </div>
      
      {/* Input de email */}
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="email">Email:</label>
        <input 
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        />
      </div>
      
      {/* Inputs de password */}
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="password">Contraseña:</label>
        <input 
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        />
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="confirmPassword">Confirmar Contraseña:</label>
        <input 
          type="password"
          id="confirmPassword"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        />
      </div>
      
      {/* Input numérico */}
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="age">Edad:</label>
        <input 
          type="number"
          id="age"
          name="age"
          value={formData.age}
          onChange={handleChange}
          min="18"
          max="120"
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        />
      </div>
      
      {/* Select */}
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="country">País:</label>
        <select 
          id="country"
          name="country"
          value={formData.country}
          onChange={handleChange}
          style={{ width: '100%', padding: '8px', marginTop: '5px' }}
        >
          <option value="mexico">México</option>
          <option value="usa">Estados Unidos</option>
          <option value="spain">España</option>
          <option value="argentina">Argentina</option>
          <option value="colombia">Colombia</option>
        </select>
      </div>
      
      {/* Checkboxes */}
      <div style={{ marginBottom: '15px' }}>
        <label>
          <input 
            type="checkbox"
            name="newsletter"
            checked={formData.newsletter}    // 🔑 Para checkboxes usamos 'checked'
            onChange={handleChange}
          />
          <span style={{ marginLeft: '8px' }}>Suscribirme al newsletter</span>
        </label>
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label>
          <input 
            type="checkbox"
            name="terms"
            checked={formData.terms}
            onChange={handleChange}
            required
          />
          <span style={{ marginLeft: '8px' }}>Acepto los términos y condiciones *</span>
        </label>
      </div>
      
      {/* Mostrar datos en tiempo real */}
      <div style={{ backgroundColor: '#f5f5f5', padding: '10px', marginBottom: '15px', fontSize: '12px' }}>
        <strong>Vista previa de datos:</strong>
        <br />Nombre completo: {formData.firstName} {formData.lastName}
        <br />Email: {formData.email}
        <br />País: {formData.country}
        <br />Newsletter: {formData.newsletter ? 'Sí' : 'No'}
      </div>
      
      <button 
        type="submit"
        disabled={!formData.terms} // Botón deshabilitado si no acepta términos
        style={{ 
          width: '100%', 
          padding: '12px', 
          backgroundColor: formData.terms ? '#4CAF50' : '#ccc',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: formData.terms ? 'pointer' : 'not-allowed'
        }}
      >
        Registrarse
      </button>
    </form>
  );
}
```

### Validación en Tiempo Real

> **📝 Explicación**: La validación en tiempo real mejora la experiencia del usuario al mostrar errores inmediatamente. Usamos diferentes estados para tracking: qué campos han sido "tocados", qué errores existen, y cuándo mostrar validaciones.

```jsx
import { useState } from 'react';

function ValidatedRegistrationForm() {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: '',
        username: ''
    });

    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({}); // 🎯 Para saber qué campos han sido tocados

    // 🔍 Validaciones en tiempo real
    const validateField = (name, value) => {
        switch (name) {
            case 'email':
                if (!value) return 'El email es requerido';
                if (!/\S+@\S+\.\S+/.test(value)) return 'Email inválido';
                return '';

            case 'password':
                if (!value) return 'La contraseña es requerida';
                if (value.length < 6) return 'Mínimo 6 caracteres';
                if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
                    return 'Debe contener mayúsculas, minúsculas y números';
                }
                return '';

            case 'confirmPassword':
                if (!value) return 'Confirma tu contraseña';
                if (value !== formData.password) return 'Las contraseñas no coinciden';
                return '';

            case 'username':
                if (!value) return 'El nombre de usuario es requerido';
                if (value.length < 3) return 'Mínimo 3 caracteres';
                if (!/^[a-zA-Z0-9_]+$/.test(value)) return 'Solo letras, números y guiones bajos';
                return '';

            default:
                return '';
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;

        // Actualizar datos del formulario
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));

        // 🔥 Validar en tiempo real si el campo ya fue tocado
        if (touched[name]) {
            const error = validateField(name, value);
            setErrors(prev => ({
                ...prev,
                [name]: error
            }));
        }
    };

    // 🎯 Se ejecuta cuando el usuario sale del campo
    const handleBlur = (e) => {
        const { name, value } = e.target;

        // Marcar el campo como tocado
        setTouched(prev => ({
            ...prev,
            [name]: true
        }));

        // Validar cuando el usuario sale del campo
        const error = validateField(name, value);
        setErrors(prev => ({
            ...prev,
            [name]: error
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // Validar todos los campos
        const newErrors = {};
        Object.keys(formData).forEach(field => {
            const error = validateField(field, formData[field]);
            if (error) newErrors[field] = error;
        });

        setErrors(newErrors);
        setTouched({
            email: true,
            password: true,
            confirmPassword: true,
            username: true
        });

        // Solo enviar si no hay errores
        if (Object.keys(newErrors).length === 0) {
            console.log('✅ Formulario válido:', formData);
            alert('Registro exitoso!');
            // Aquí enviarías los datos al servidor
        } else {
            console.log('❌ Formulario con errores:', newErrors);
        }
    };

    // Función auxiliar para mostrar el estado del campo
    const getFieldStatus = (fieldName) => {
        if (!touched[fieldName]) return '';
        return errors[fieldName] ? 'error' : 'success';
    };

    return (
        <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
            <h2>📝 Registro con Validación</h2>

            {/* Username */}
            <div style={{ marginBottom: '20px' }}>
                <label htmlFor="username" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                    Nombre de usuario:
                </label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    onBlur={handleBlur}                                    // 🔥 Validar al salir del campo
                    style={{
                        width: '100%',
                        padding: '8px',
                        border: `2px solid ${getFieldStatus('username') === 'error' ? '#f44336' :
                                getFieldStatus('username') === 'success' ? '#4CAF50' : '#ddd'
                            }`,
                        borderRadius: '4px',
                        fontSize: '14px',
                        boxSizing: 'border-box'
                    }}
                />
                {/* 🚨 Mostrar error solo si el campo fue tocado */}
                {errors.username && touched.username && (
                    <span style={{ color: '#f44336', fontSize: '12px', display: 'block', marginTop: '5px' }}>
                        ❌ {errors.username}
                    </span>
                )}
                {/* ✅ Mostrar éxito solo si no hay error y fue tocado */}
                {!errors.username && touched.username && formData.username && (
                    <span style={{ color: '#4CAF50', fontSize: '12px', display: 'block', marginTop: '5px' }}>
                        ✅ Nombre de usuario válido
                    </span>
                )}
            </div>

            {/* Email */}
            <div style={{ marginBottom: '20px' }}>
                <label htmlFor="email" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                    Email:
                </label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    style={{
                        width: '100%',
                        padding: '8px',
                        border: `2px solid ${getFieldStatus('email') === 'error' ? '#f44336' :
                                getFieldStatus('email') === 'success' ? '#4CAF50' : '#ddd'
                            }`,
                        borderRadius: '4px',
                        fontSize: '14px',
                        boxSizing: 'border-box'
                    }}
                />
                {errors.email && touched.email && (
                    <span style={{ color: '#f44336', fontSize: '12px', display: 'block', marginTop: '5px' }}>
                        ❌ {errors.email}
                    </span>
                )}
                {!errors.email && touched.email && formData.email && (
                    <span style={{ color: '#4CAF50', fontSize: '12px', display: 'block', marginTop: '5px' }}>
                        ✅ Email válido
                    </span>
                )}
            </div>

            {/* Password */}
            <div style={{ marginBottom: '20px' }}>
                <label htmlFor="password" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                    Contraseña:
                </label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    style={{
                        width: '100%',
                        padding: '8px',
                        border: `2px solid ${getFieldStatus('password') === 'error' ? '#f44336' :
                                getFieldStatus('password') === 'success' ? '#4CAF50' : '#ddd'
                            }`,
                        borderRadius: '4px',
                        fontSize: '14px',
                        boxSizing: 'border-box'
                    }}
                />
                {errors.password && touched.password && (
                    <span style={{ color: '#f44336', fontSize: '12px', display: 'block', marginTop: '5px' }}>
                        ❌ {errors.password}
                    </span>
                )}

                {/* 💪 Indicador de fortaleza de contraseña */}
                {formData.password && (
                    <div style={{ marginTop: '8px' }}>
                        <div style={{
                            height: '4px',
                            backgroundColor: '#eee',
                            borderRadius: '2px',
                            overflow: 'hidden'
                        }}>
                            <div style={{
                                height: '100%',
                                width: `${Math.min((formData.password.length / 8) * 100, 100)}%`,
                                backgroundColor:
                                    formData.password.length < 6 ? '#f44336' :
                                        formData.password.length < 8 ? '#ff9800' : '#4CAF50',
                                transition: 'all 0.3s'
                            }} />
                        </div>
                        <small style={{ color: '#666' }}>
                            Fortaleza: {
                                formData.password.length < 6 ? 'Débil' :
                                    formData.password.length < 8 ? 'Media' : 'Fuerte'
                            }
                        </small>
                    </div>
                )}
            </div>

            {/* Confirm Password */}
            <div style={{ marginBottom: '25px' }}>
                <label htmlFor="confirmPassword" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                    Confirmar Contraseña:
                </label>
                <input
                    type="password"
                    id="confirmPassword"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    style={{
                        width: '100%',
                        padding: '8px',
                        border: `2px solid ${getFieldStatus('confirmPassword') === 'error' ? '#f44336' :
                                getFieldStatus('confirmPassword') === 'success' ? '#4CAF50' : '#ddd'
                            }`,
                        borderRadius: '4px',
                        fontSize: '14px',
                        boxSizing: 'border-box'
                    }}
                />
                {errors.confirmPassword && touched.confirmPassword && (
                    <span style={{ color: '#f44336', fontSize: '12px', display: 'block', marginTop: '5px' }}>
                        ❌ {errors.confirmPassword}
                    </span>
                )}
                {!errors.confirmPassword && touched.confirmPassword && formData.confirmPassword && (
                    <span style={{ color: '#4CAF50', fontSize: '12px', display: 'block', marginTop: '5px' }}>
                        ✅ Las contraseñas coinciden
                    </span>
                )}
            </div>

            {/* Submit Button */}
            <button
                type="button"
                onClick={handleSubmit}
                style={{
                    width: '100%',
                    padding: '12px',
                    backgroundColor: '#2196F3',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '16px',
                    fontWeight: 'bold',
                    transition: 'background-color 0.3s'
                }}
                onMouseOver={(e) => e.target.style.backgroundColor = '#1976D2'}
                onMouseOut={(e) => e.target.style.backgroundColor = '#2196F3'}
            >
                Registrarse
            </button>

            {/* 📊 Resumen de validación */}
            <div style={{ 
                marginTop: '20px', 
                padding: '15px', 
                backgroundColor: '#f5f5f5', 
                fontSize: '14px',
                borderRadius: '4px'
            }}>
                <strong>Estado del formulario:</strong>
                <br />
                <span style={{ color: '#4CAF50' }}>
                    ✅ Campos válidos: {Object.keys(formData).filter(key => 
                        touched[key] && !errors[key] && formData[key]
                    ).length}
                </span>
                <br />
                <span style={{ color: '#f44336' }}>
                    ❌ Campos con errores: {Object.keys(errors).filter(key => errors[key]).length}
                </span>
            </div>
        </div>
    );
}

export default ValidatedRegistrationForm;
```

## 💻 Ejercicios Prácticos

> **📝 Explicación**: Estos ejercicios te ayudarán a practicar los conceptos aprendidos. Comienza con el contador avanzado y ve progresando hacia ejercicios más complejos.

### Ejercicio 1: Contador Avanzado

> **🎯 Objetivo**: Practicar manejo de estado múltiple y arrays de historial. Este ejercicio combina varios conceptos: estado local, eventos, y manipulación de arrays.

```jsx
function AdvancedCounter() {
  const [count, setCount] = useState(0);
  const [step, setStep] = useState(1);
  const [history, setHistory] = useState([0]); // 📜 Guardamos historial de valores
  
  const increment = () => {
    const newCount = count + step;
    setCount(newCount);
    setHistory(prev => [...prev, newCount]); // 🔥 Agregamos al historial
  };
  
  const decrement = () => {
    const newCount = count - step;
    setCount(newCount);
    setHistory(prev => [...prev, newCount]);
  };
  
  const reset = () => {
    setCount(0);
    setHistory([0]); // 🔄 Reiniciamos historial también
  };
  
  const undo = () => {
    if (history.length > 1) {
      const newHistory = history.slice(0, -1); // 🔙 Removemos último elemento
      setHistory(newHistory);
      setCount(newHistory[newHistory.length - 1]); // 📍 Volvemos al valor anterior
    }
  };
  
  return (
    <div>
      <h2>Contador Avanzado</h2>
      <p>Valor actual: {count}</p>
      
      <div>
        <label>
          Paso: 
          <input 
            type="number"
            value={step}
            onChange={(e) => setStep(parseInt(e.target.value) || 1)}
            min="1"
          />
        </label>
      </div>
      
      <div>
        <button onClick={increment}>+{step}</button>
        <button onClick={decrement}>-{step}</button>
        <button onClick={reset}>Reset</button>
        <button onClick={undo} disabled={history.length <= 1}>
          Deshacer
        </button>
      </div>
      
      <div>
        <h3>Historial:</h3>
        <p>{history.join(' → ')}</p> {/* 🔍 Mostramos todo el historial */}
      </div>
    </div>
  );
}
```

### Ejercicio 2: Buscador con API

> **🎯 Objetivo**: Practicar useEffect, estados de carga, y debouncing. Este ejercicio simula una búsqueda real con delays y manejo de errores.

```jsx
function UserSearch() {
  const [query, setQuery] = useState('');
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // 🔍 Si no hay query, no buscamos nada
    if (!query.trim()) {
      setUsers([]);
      return;
    }
    
    const searchUsers = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // 🕐 Simulando delay de red
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 📊 Datos simulados
        const mockUsers = [
          { id: 1, name: 'Juan Pérez', email: 'juan@example.com' },
          { id: 2, name: 'Ana García', email: 'ana@example.com' },
          { id: 3, name: 'Pedro López', email: 'pedro@example.com' },
          { id: 4, name: 'María Martínez', email: 'maria@example.com' },
          { id: 5, name: 'Carlos Rodríguez', email: 'carlos@example.com' }
        ];
        
        // 🔎 Filtrar por nombre
        const filteredUsers = mockUsers.filter(user =>
          user.name.toLowerCase().includes(query.toLowerCase())
        );
        
        setUsers(filteredUsers);
      } catch (err) {
        setError('Error al buscar usuarios');
      } finally {
        setLoading(false);
      }
    };
    
    // 🚀 Debounce: esperamos 300ms antes de buscar
    const timeoutId = setTimeout(searchUsers, 300);
    
    // 🧹 Cleanup: cancelamos búsqueda anterior si el usuario sigue escribiendo
    return () => clearTimeout(timeoutId);
  }, [query]);
  
  return (
    <div>
      <h2>🔍 Buscador de Usuarios</h2>
      
      <input 
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Buscar usuarios..."
        style={{ 
          width: '100%', 
          padding: '10px', 
          marginBottom: '20px',
          border: '1px solid #ccc',
          borderRadius: '4px'
        }}
      />
      
      {/* 🔄 Estados de carga */}
      {loading && <p>🔄 Buscando...</p>}
      {error && <p style={{ color: 'red' }}>❌ {error}</p>}
      
      {/* 📋 Resultados */}
      <div>
        {users.map(user => (
          <div key={user.id} style={{ 
            border: '1px solid #eee', 
            padding: '15px', 
            margin: '10px 0',
            borderRadius: '4px',
            backgroundColor: '#f9f9f9'
          }}>
            <h3 style={{ margin: '0 0 5px 0' }}>{user.name}</h3>
            <p style={{ margin: '0', color: '#666' }}>{user.email}</p>
          </div>
        ))}
      </div>
      
      {/* 📭 Sin resultados */}
      {query && !loading && users.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666' }}>
          📭 No se encontraron usuarios para "{query}"
        </p>
      )}
    </div>
  );
}
```

### Ejercicio 3: Aplicación de Notas

> **🎯 Objetivo**: Proyecto completo que combina múltiples conceptos: comunicación entre componentes, formularios, localStorage, búsqueda, y manejo de listas complejas.

```jsx
function NotesApp() {
  const [notes, setNotes] = useState([]);
  const [currentNote, setCurrentNote] = useState({
    id: null,
    title: '',
    content: '',
    createdAt: null
  });
  const [searchTerm, setSearchTerm] = useState('');
  
  // 💾 Cargar notas desde localStorage al iniciar
  useEffect(() => {
    const savedNotes = localStorage.getItem('notes');
    if (savedNotes) {
      setNotes(JSON.parse(savedNotes));
    }
  }, []);
  
  // 💾 Guardar notas en localStorage cuando cambien
  useEffect(() => {
    localStorage.setItem('notes', JSON.stringify(notes));
  }, [notes]);
  
  const saveNote = () => {
    // 🚫 No guardar notas vacías
    if (!currentNote.title.trim() && !currentNote.content.trim()) {
      return;
    }
    
    if (currentNote.id) {
      // ✏️ Actualizar nota existente
      setNotes(notes.map(note => 
        note.id === currentNote.id 
          ? { ...currentNote, updatedAt: new Date().toISOString() }
          : note
      ));
    } else {
      // ➕ Crear nueva nota
      const newNote = {
        ...currentNote,
        id: Date.now(), // ID simple basado en timestamp
        createdAt: new Date().toISOString()
      };
      setNotes([newNote, ...notes]); // 📌 Nuevas notas al principio
    }
    
    // 🧹 Limpiar formulario
    setCurrentNote({
      id: null,
      title: '',
      content: '',
      createdAt: null
    });
  };
  
  const editNote = (note) => {
    setCurrentNote(note); // 📝 Cargar nota en el editor
  };
  
  const deleteNote = (id) => {
    setNotes(notes.filter(note => note.id !== id));
    // 🗑️ Si estamos editando la nota eliminada, limpiar editor
    if (currentNote.id === id) {
      setCurrentNote({
        id: null,
        title: '',
        content: '',
        createdAt: null
      });
    }
  };
  
  const newNote = () => {
    setCurrentNote({
      id: null,
      title: '',
      content: '',
      createdAt: null
    });
  };
  
  // 🔍 Filtrar notas basado en búsqueda
  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    note.content.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  return (
    <div style={{ display: 'flex', height: '500px', fontFamily: 'Arial, sans-serif' }}>
      {/* 📋 Panel izquierdo - Lista de notas */}
      <div style={{ 
        width: '300px', 
        borderRight: '1px solid #ccc', 
        padding: '15px',
        backgroundColor: '#f8f9fa'
      }}>
        <h2 style={{ margin: '0 0 15px 0' }}>📝 Mis Notas</h2>
        
        <button onClick={newNote} style={{ 
          width: '100%', 
          marginBottom: '15px',
          padding: '12px',
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
          fontWeight: 'bold'
        }}>
          ➕ Nueva Nota
        </button>
        
        <input 
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="🔍 Buscar notas..."
          style={{ 
            width: '100%', 
            padding: '10px', 
            marginBottom: '15px',
            border: '1px solid #ddd',
            borderRadius: '6px',
            boxSizing: 'border-box'
          }}
        />
        
        {/* 📚 Lista de notas */}
        <div style={{ maxHeight: '350px', overflowY: 'auto' }}>
          {filteredNotes.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#666', fontStyle: 'italic' }}>
              {searchTerm ? '🔍 Sin resultados' : '📭 No hay notas'}
            </p>
          ) : (
            filteredNotes.map(note => (
              <div 
                key={note.id}
                onClick={() => editNote(note)}
                style={{ 
                  padding: '12px',
                  border: '1px solid #e0e0e0',
                  marginBottom: '8px',
                  cursor: 'pointer',
                  backgroundColor: currentNote.id === note.id ? '#e3f2fd' : 'white',
                  borderRadius: '6px',
                  transition: 'all 0.2s',
                  position: 'relative'
                }}
                onMouseEnter={(e) => {
                  if (currentNote.id !== note.id) {
                    e.target.style.backgroundColor = '#f5f5f5';
                  }
                }}
                onMouseLeave={(e) => {
                  if (currentNote.id !== note.id) {
                    e.target.style.backgroundColor = 'white';
                  }
                }}
              >
                <h4 style={{ 
                  margin: '0 0 6px 0', 
                  fontSize: '14px',
                  color: '#333',
                  fontWeight: 'bold'
                }}>
                  {note.title || '📄 Sin título'}
                </h4>
                <p style={{ 
                  margin: '0 0 8px 0', 
                  fontSize: '12px', 
                  color: '#666',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap'
                }}>
                  {note.content || 'Nota vacía...'}
                </p>
                <small style={{ color: '#999', fontSize: '11px' }}>
                  📅 {new Date(note.createdAt).toLocaleDateString()}
                </small>
                <button 
                  onClick={(e) => {
                    e.stopPropagation(); // 🛑 Evitar que se active editNote
                    if (window.confirm('¿Eliminar esta nota?')) {
                      deleteNote(note.id);
                    }
                  }}
                  style={{ 
                    position: 'absolute',
                    top: '8px',
                    right: '8px',
                    background: 'none',
                    border: 'none',
                    color: '#dc3545',
                    cursor: 'pointer',
                    fontSize: '16px',
                    width: '20px',
                    height: '20px',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                  title="Eliminar nota"
                >
                  🗑️
                </button>
              </div>
            ))
          )}
        </div>
      </div>
      
      {/* ✏️ Panel derecho - Editor */}
      <div style={{ flex: 1, padding: '15px', backgroundColor: 'white' }}>
        <div style={{ marginBottom: '15px' }}>
          <input 
            type="text"
            value={currentNote.title}
            onChange={(e) => setCurrentNote(prev => ({
              ...prev,
              title: e.target.value
            }))}
            placeholder="✏️ Título de la nota..."
            style={{ 
              width: '100%',
              padding: '12px',
              fontSize: '18px',
              border: '1px solid #ddd',
              borderRadius: '6px',
              boxSizing: 'border-box',
              fontWeight: 'bold'
            }}
          />
        </div>
        
        <textarea 
          value={currentNote.content}
          onChange={(e) => setCurrentNote(prev => ({
            ...prev,
            content: e.target.value
          }))}
          placeholder="📝 Escribe tu nota aquí..."
          style={{ 
            width: '100%',
            height: '320px',
            padding: '12px',
            border: '1px solid #ddd',
            borderRadius: '6px',
            resize: 'none',
            fontFamily: 'Arial, sans-serif',
            fontSize: '14px',
            lineHeight: '1.5',
            boxSizing: 'border-box'
          }}
        />
        
        <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
          <button 
            onClick={saveNote}
            disabled={!currentNote.title.trim() && !currentNote.content.trim()}
            style={{ 
              padding: '12px 24px',
              backgroundColor: (!currentNote.title.trim() && !currentNote.content.trim()) 
                ? '#ccc' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: (!currentNote.title.trim() && !currentNote.content.trim()) 
                ? 'not-allowed' : 'pointer',
              fontWeight: 'bold'
            }}
          >
            💾 {currentNote.id ? 'Actualizar' : 'Guardar'}
          </button>
          
          <button 
            onClick={newNote}
            style={{ 
              padding: '12px 24px',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer'
            }}
          >
            🔄 Limpiar
          </button>
        </div>
        
        {/* 📊 Info de la nota actual */}
        {currentNote.id && (
          <div style={{ 
            marginTop: '20px', 
            padding: '10px', 
            backgroundColor: '#f8f9fa', 
            borderRadius: '6px',
            fontSize: '12px',
            color: '#666'
          }}>
            📊 <strong>Editando:</strong> Creada el {new Date(currentNote.createdAt).toLocaleString()}
            {currentNote.updatedAt && (
              <span> • Última modificación: {new Date(currentNote.updatedAt).toLocaleString()}</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
```

## 🎯 Conceptos Clave Resumidos

### Comunicación entre Componentes:
- **Props**: Padre → Hijo (solo lectura)
- **Callbacks**: Hijo → Padre (mediante funciones)
- **Lifting State Up**: Compartir estado entre hermanos

### Formularios en React:
- **Componentes Controlados**: React maneja el estado
- **Validación en Tiempo Real**: Feedback inmediato al usuario
- **Manejo de Múltiples Campos**: Un objeto para todo el estado

### Mejores Prácticas:
- Siempre usar componentes controlados
- Validar en `onBlur` y `onChange`
- Manejar estados de carga y error
- Usar nombres de atributos `name` que coincidan con las keys del estado
- Implementar debouncing para búsquedas
- Persistir datos importantes en localStorage

---

**🚀 ¡Siguientes pasos!** 
1. Implementa los ejercicios paso a paso
2. Experimenta agregando nuevas funcionalidades
3. Practica validaciones más complejas
4. Explora patrones avanzados como Context API para comunicación global