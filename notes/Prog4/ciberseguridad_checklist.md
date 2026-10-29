
## Planillas de Seguridad en Código Web

**Instrucciones:** Usa estas listas para revisar tu código o el de tus compañeros. Marca "Sí" si la medida de seguridad está implementada correctamente, "No" si no lo está, y "N/A" si no aplica al contexto. Si marcas "No", asegúrate de corregir la vulnerabilidad.

---

### 📋 **Checklist: Prevención de Inyección SQL (SQLi)**

| Aspecto a Revisar                                          | Sí  | No  | N/A | Notas / Acciones a Tomar                                    |
| :--------------------------------------------------------- | :-- | :-- | :-- | :---------------------------------------------------------- |
| **1. Consultas Parametrizadas/Preparadas:** ¿Todas las consultas SQL utilizan sentencias preparadas (ej. `PDO::prepare`, `mysqli::prepare`, ORMs) en lugar de concatenar cadenas? |     |     |     | **Crítico:** Evitar la construcción dinámica de consultas SQL con entradas de usuario. |
| **2. Validación de Entrada:** ¿Se valida el tipo, formato y longitud de todos los datos antes de ser utilizados en consultas o para cualquier procesamiento? |     |     |     | Rechazar entradas que no cumplan con el formato esperado. |
| **3. Mínimos Privilegios en BD:** ¿La aplicación se conecta a la base de datos con un usuario que tiene los privilegios mínimos necesarios para sus operaciones? |     |     |     | Por ejemplo, no usar el usuario `root` o un admin para operaciones cotidianas. |
| **4. ORMs/Frameworks:** ¿Se están utilizando ORMs (ej. Eloquent en Laravel, SQLAlchemy en Python) o frameworks que gestionan automáticamente las consultas preparadas? |     |     |     | Entender cómo el ORM maneja la seguridad de SQLi es clave. |
| **5. Escapado de Caracteres:** Si, excepcionalmente, no se pueden usar consultas preparadas, ¿se están escapando *todos* los caracteres especiales de las entradas de usuario antes de usarlos en SQL (ej. `mysqli_real_escape_string`)? |     |     |     | **¡Último recurso!** Preferir siempre las consultas preparadas. |
| **6. Mensajes de Error:** ¿Los mensajes de error de la base de datos no exponen información sensible (ej. detalles de la consulta, nombres de tablas/columnas)? |     |     |     | Mensajes genéricos para el usuario, detalles en logs del servidor. |

---

### 📋 **Checklist: Prevención de Cross-Site Scripting (XSS)**

| Aspecto a Revisar                                          | Sí  | No  | N/A | Notas / Acciones a Tomar                                    |
| :--------------------------------------------------------- | :-- | :-- | :-- | :---------------------------------------------------------- |
| **1. Codificación de Salida (Escaping):** ¿Se codifica (escapa) *toda* la salida de datos de usuario antes de insertarla en el HTML (ej. `htmlspecialchars()` en PHP, librerías de templating)? |     |     |     | **Crítico:** Convertir `<` a `&lt;`, `>` a `&gt;`, `"` a `&quot;`, etc. |
| **2. Validación de Entrada Estricta:** ¿Se valida el formato y contenido de las entradas del usuario para rechazar o limpiar caracteres potencialmente maliciosos (ej. etiquetas `<script>`) si no se esperan? |     |     |     | Especialmente en campos que no deberían contener HTML. |
| **3. Content Security Policy (CSP):** ¿Se ha implementado una CSP para restringir las fuentes de scripts, estilos, imágenes y otros recursos que el navegador puede cargar? |     |     |     | Limita el impacto de un XSS exitoso. |
| **4. Cookies HttpOnly:** ¿Las cookies de sesión y otras cookies sensibles están marcadas con la bandera `HttpOnly` para evitar que JavaScript las acceda? |     |     |     | Protege contra el robo de cookies vía XSS. |
| **5. Sanitización de HTML:** Si la aplicación permite HTML enriquecido (ej. editores WYSIWYG), ¿se utiliza una librería de sanitización de HTML robusta (ej. DOMPurify en JS, HTML Purifier en PHP) para limpiar solo las etiquetas y atributos seguros? |     |     |     | **¡Importante!** No basta con `htmlspecialchars()` en estos casos. |
| **6. Atributos de Contexto:** ¿Se aplican las reglas de escape correctas según el contexto HTML (ej. atributos HTML, URLs, bloques JavaScript)? |     |     |     | El escape para un atributo es diferente al escape para contenido de texto. |

---

### 📋 **Checklist: Prevención de Cross-Site Request Forgery (CSRF)**

| Aspecto a Revisar                                          | Sí  | No  | N/A | Notas / Acciones a Tomar                                    |
| :--------------------------------------------------------- | :-- | :-- | :-- | :---------------------------------------------------------- |
| **1. Tokens Anti-CSRF:** ¿Todos los formularios que realizan acciones de cambio de estado (ej. cambiar contraseña, comprar, eliminar) incluyen un token anti-CSRF único, aleatorio y por sesión? |     |     |     | **Crítico:** El servidor debe generar y verificar este token en cada petición relevante. |
| **2. Verificación de Referer/Origin:** ¿Las solicitudes que cambian el estado verifican la cabecera `Referer` o `Origin` para asegurarse de que provienen del dominio esperado? |     |     |     | Una capa de defensa adicional, aunque no infalible por sí sola. |
| **3. Métodos HTTP:** ¿Se utilizan métodos HTTP `POST` (o más específicos como `PUT`/`DELETE`) para operaciones que cambian el estado, y no `GET`? |     |     |     | `GET` no debe tener efectos secundarios. |
| **4. Cookies `SameSite`:** ¿Las cookies de sesión y otras cookies importantes están configuradas con el atributo `SameSite=Lax` o `SameSite=Strict`? |     |     |     | Ayuda a mitigar CSRF enviando cookies solo en contextos de mismo sitio. |
| **5. Confirmación del Usuario:** Para operaciones muy sensibles, ¿se requiere una re-autenticación o una confirmación explícita del usuario (ej. pedir la contraseña actual)? |     |     |     | Añade una capa de seguridad para acciones críticas. |
| **6. Tokens de Sesión:** ¿Los tokens de sesión son aleatorios, de suficiente longitud y se regeneran después de un login exitoso? |     |     |     | Una sesión predecible debilita la protección CSRF. |

---

### 📋 **Checklist: Prevención de Validación de Entrada Débil/Insuficiente**

| Aspecto a Revisar                                          | Sí  | No  | N/A | Notas / Acciones a Tomar                                    |
| :--------------------------------------------------------- | :-- | :-- | :-- | :---------------------------------------------------------- |
| **1. Validación en el Servidor:** ¿Todos los datos de entrada del usuario (de formularios, URLs, cabeceras, archivos) son validados *siempre* en el lado del servidor? |     |     |     | **Crítico:** Nunca confíes solo en la validación del lado cliente. |
| **2. Validación de Tipo:** ¿Se verifica que el tipo de dato sea el esperado (ej. `entero` para ID, `flotante` para precio, `booleano` para flags)? |     |     |     | Evita errores y ataques de inyección. |
| **3. Validación de Longitud:** ¿Se limita la longitud máxima y/o mínima de las entradas de texto a un valor razonable y esperado? |     |     |     | Previene desbordamientos y ataques DoS. |
| **4. Validación de Formato:** ¿Se verifica el formato exacto de las entradas (ej. expresiones regulares para emails, fechas, números de teléfono)? |     |     |     | Asegura que los datos son consistentes y esperados. |
| **5. Validación de Rango:** ¿Los valores numéricos o fechas se validan dentro de un rango lógico y permitido? |     |     |     | Ej. edad entre 0 y 120, fechas en el futuro/pasado apropiado. |
| **6. Listas Blancas de Caracteres/Valores:** ¿Se utilizan listas blancas para definir qué caracteres o valores *están permitidos*, en lugar de intentar prohibir los maliciosos? |     |     |     | Más seguro que las listas negras, que son fáciles de evadir. |
| **7. Sanitización de Archivos Subidos:** Si se permite la carga de archivos, ¿se valida su tipo (MIME), extensión, tamaño y contenido en el servidor? ¿Se almacenan en un directorio fuera del árbol web o con nombres aleatorios? |     |     |     | **Crítico:** Evitar la ejecución de código malicioso subido. |
| **8. Mensajes de Error Claros:** ¿Los mensajes de error por validación fallida son informativos para el usuario, pero no revelan detalles internos de la implementación? |     |     |     | "Formato de email inválido" vs "Error en regex para el campo email." |

---

### 📋 **Checklist: Prevención de Autenticación Insegura y Gestión de Sesiones**

| Aspecto a Revisar                                          | Sí  | No  | N/A | Notas / Acciones a Tomar                                    |
| :--------------------------------------------------------- | :-- | :-- | :-- | :---------------------------------------------------------- |
| **1. Hashing Seguro de Contraseñas:** ¿Todas las contraseñas se almacenan hasheadas utilizando algoritmos robustos con `salt` (ej. BCrypt, Argon2, scrypt, PBKDF2)? |     |     |     | **Crítico:** Nunca texto plano. Nunca hashes rápidos sin salt (MD5, SHA1). |
| **2. Protección Anti-Fuerza Bruta:** ¿Existen mecanismos para prevenir ataques de fuerza bruta (ej. bloqueo temporal de cuentas, retrasos crecientes, CAPTCHA, monitorización de IP)? |     |     |     | Aplicar tras X intentos fallidos en el login. |
| **3. Políticas de Contraseñas Fuertes:** ¿Se aplican políticas que exigen contraseñas con longitud mínima, complejidad (mayúsculas, minúsculas, números, símbolos) y que no se reutilicen? |     |     |     | Educas al usuario y aumentas la seguridad. |
| **4. Regeneración de ID de Sesión:** ¿El ID de sesión se regenera tras un login exitoso y para cualquier cambio significativo de privilegios? |     |     |     | Evita la fijación de sesión. |
| **5. Expiración de Sesión:** ¿Las sesiones tienen un tiempo de expiración adecuado, tanto por inactividad como un límite de tiempo absoluto? |     |     |     | Reduce la ventana de oportunidad para un atacante. |
| **6. Cookies de Sesión Seguras:** ¿Las cookies de sesión están configuradas con las banderas `HttpOnly`, `Secure` y `SameSite`? |     |     |     | Protege contra robo de cookies y envíos cross-site. |
| **7. Cierre de Sesión Seguro:** ¿El `logout` invalida la sesión en el servidor y redirige al usuario de forma segura? |     |     |     | No solo borra la cookie del cliente. |
| **8. Autenticación de Dos Factores (2FA):** Para sistemas críticos, ¿se ofrece o se exige la autenticación de dos factores? |     |     |     | Una capa de seguridad adicional muy efectiva. |
| **9. Mensajes de Error Genéricos:** ¿Los mensajes de error de login son genéricos (ej. "Usuario o contraseña incorrectos") y no especifican si el usuario existe o si la contraseña es la única fallida? |     |     |     | Evita la enumeración de usuarios. |
| **10. Evitar Credenciales por Defecto:** ¿Se eliminan o cambian todas las credenciales por defecto antes de que la aplicación esté en producción? |     |     |     | Un error común en muchos sistemas. |
| **11. Verificación de Permisos (Autorización):** ¿Cada función o recurso sensible verifica los permisos del usuario *después* de la autenticación para asegurar que tiene derecho a acceder a esa acción (previniendo escalada de privilegios)? |     |     |     | La autenticación es *quién eres*, la autorización es *qué puedes hacer*. |
