# Apunte de Redes de Computadoras

## 1. Introducción a las Redes de Computadoras

Una **red de computadoras** es un conjunto de dispositivos conectados entre sí que pueden **compartir información y recursos**. Estas conexiones pueden hacerse mediante **cables** (redes cableadas) o **ondas de radio** (redes inalámbricas).

En la vida cotidiana usamos redes constantemente: cuando enviamos un mensaje por WhatsApp, vemos un video en YouTube o accedemos a una base de datos en la nube. Todo eso es posible gracias a redes y protocolos de comunicación.



### 1.1 ¿Por qué existen las redes?

Las redes existen principalmente para:

- **Compartir información**: archivos, bases de datos, páginas web.
- **Compartir recursos**: impresoras, servidores, almacenamiento.
- **Comunicarse**: email, videollamadas, mensajería.
- **Centralizar servicios**: autenticación de usuarios, copias de seguridad, monitoreo.
- **Interconectar sistemas**: microservicios, APIs, IoT.



### 1.2 Conceptos básicos

Antes de avanzar, es importante conocer algunos términos que usaremos a lo largo del apunte:

| Término | Definición |
|----------|------------|
| **Host** | Un dispositivo conectado a la red (PC, servidor, celular) |
| **Nodo** | Punto de conexión dentro de la red (puede ser host o dispositivo de red) |
| **Enlace** | Medio físico o lógico que conecta dos nodos |
| **Paquete** | Unidad de datos enviada en una red |
| **Puerto** | Número lógico que identifica servicios dentro de un dispositivo |
| **Protocolo** | Conjunto de reglas para la comunicación entre dispositivos |



### 1.3 Tipos de redes según alcance

| Tipo | Características | Ejemplo |
|------|------------------|---------|
| **LAN** (*Local Area Network*) | Red local, pequeña área | Oficina, casa |
| **MAN** (*Metropolitan Area Network*) | Red de alcance urbano | Red municipal |
| **WAN** (*Wide Area Network*) | Cobertura geográfica amplia | Internet |

> 💡 **Internet es una WAN mundial**, una red que conecta miles de redes.



### 1.4 Redes cableadas vs inalámbricas

| Característica | Cableada (Ethernet) | Inalámbrica (WiFi) |
|---------------|--------------------|--------------------|
| Velocidad | Alta y estable | Variable |
| Estabilidad | Muy estable | Afectada por interferencias |
| Seguridad | Alta | Menor (requiere cifrado WPA2/WPA3) |
| Movilidad | Baja | Alta |
| Latencia | Baja | Media/alta |



### 1.5 Internet, Intranet y Extranet

| Tipo | Descripción |
|------|-------------|
| **Internet** | Red pública mundial |
| **Intranet** | Red privada de una organización |
| **Extranet** | Parte de la intranet compartida con terceros |



### 1.6 Representación de una red simple (diagrama ASCII)

```text
                   ┌───────────────┐
                   │   Internet    │
                   └───────┬───────┘
                           │
                      ┌────┴─────┐
                      │  Router  │
                      └────┬─────┘
           ┌───────────────┼─────────────┐
     ┌─────┴────────┐┌─────┴─────┐┌──────┴─────┐
     │ PC Escritorio││ Notebook  ││ Smartphone │
     └──────────────┘└───────────┘└────────────┘
```
### ✅ Resumen del tema

* Una red conecta dispositivos.

* Se usan para comunicar, compartir y trabajar colaborativamente.

* Los conceptos clave iniciales son: host, nodo, enlace, paquetes y protocolos.

* LAN = red local; WAN = red amplia como Internet.

* WiFi es una forma de red inalámbrica dentro de una LAN.

### 🔧 Actividad rápida

¿Qué redes usás en tu vida diaria?

¿Qué dispositivos en tu casa tienen acceso a Internet?

¿Todos los dispositivos están conectados por cable?

## 2. Topologías y Arquitecturas de Red

Las topologías describen cómo se conectan físicamente los dispositivos de una red.

### 2.1 Topologías físicas

| Topología    | Diagrama                  | Ventajas            | Desventajas                         |
| ------------ | ------------------------- | ------------------- | ----------------------------------- |
| **Bus**      | A ─ B ─ C ─ D             | Simple y barata     | Un corte afecta a todos             |
| **Anillo**   | A ○ B ○ C ○ D             | Ordenada            | Si se corta, se pierde comunicación |
| **Estrella** | central ─ A, B, C         | Fácil de mantener   | Depende del nodo central            |
| **Malla**    | Todos conectados entre sí | Alta disponibilidad | Costosa                             |

### 2.2 Arquitectura Cliente-Servidor y Peer-to-Peer (P2P)

En una red, los dispositivos pueden organizarse de diferentes maneras según cómo comparten información o servicios.

#### ✅ Cliente-Servidor

En este modelo, uno o más equipos actúan como **servidores**, ofreciendo servicios a otros equipos llamados **clientes**.

```text
        ┌─────────────┐
        │   Cliente   │───┐
        └─────────────┘   │
                          │   Solicita servicio (ej: página web)
        ┌─────────────┐   ▼
        │  Servidor   │
        └─────────────┘   ▲
                          │   Respuesta
        ┌─────────────┐   │
        │   Cliente   │───┘
        └─────────────┘
```

✔ Ventajas:

* Control centralizado
* Mejora la administración de datos
* Mejor seguridad

✘ Desventajas:

* Depende del servidor
* Puede requerir hardware poderoso

Ejemplos: páginas web (HTTP), servicios de base de datos (MySQL), correo electrónico.

### ✅ Peer-to-Peer (P2P)

En este modelo **todos los equipos son iguales** y comparten recursos entre sí sin servidores centrales.

```text
   ┌─────────┐        ┌─────────┐
   │  Nodo A │────────│  Nodo B │
   └─────────┘        └─────────┘
        │                 │
        └───────┬─────────┘
                │
           ┌─────────┐
           │  Nodo C │
           └─────────┘
```

✔ Ventajas:

* Fácil de implementar
* No requiere servidor
* Ideal para redes pequeñas

✘ Desventajas:

* Difícil de administrar
* Seguridad débil
* No escala bien

Ejemplos: Torrent (BitTorrent), redes locales simples.


## 2.3 Representación de Redes (Diagramas Básicos)

Las redes se representan visualmente con **diagramas** que muestran dispositivos y conexiones. Estos diagramas utilizan **símbolos comunes** como:

| Símbolo | Representa               |
| ------- | ------------------------ |
| 🖥️     | PC o estación de trabajo |
| 📱      | Dispositivo móvil        |
| 🌐      | Internet                 |
| 📶      | WiFi                     |
| 🔌      | Switch                   |
| 📡      | Router                   |

### Ejemplo de diagrama de red doméstica:

```text
                      🌐 Internet
                           │
                     📡 Router WiFi
                   ┌───────┴─────────┐
                   │                 │
               🖥️ PC           📱 Smartphone
                   │
               🔌 Switch
             ┌─────┴───────┐
             │             │
           🖨️ Impresora   💾 NAS
```


### ✅ Resumen del Tema 2

* Las topologías definen cómo se conectan los dispositivos.
* Arquitectura Cliente-Servidor es la más usada en empresas.
* P2P se usa en redes simples y sistemas distribuidos.
* Los diagramas de red ayudan a planificar y entender sistemas.

### 🔧 Actividad práctica

1. Dibujá el diagrama de red de tu casa o lugar de estudio.
2. ¿Qué arquitectura usa WhatsApp? ¿Y Google Drive?
3. ¿Por qué la topología estrella es la más usada hoy?



## 3. Infraestructura de Hardware de Red

Para que una red funcione no alcanza con cables o WiFi: necesitamos **dispositivos de red** que permitan enviar datos, reenviarlos y dirigirlos correctamente. En esta sección vamos a conocer los equipos más importantes de cualquier red moderna.



### 3.1 Tarjeta de Red (NIC)

La **NIC** (*Network Interface Card*) es el componente que permite que un dispositivo se conecte a una red.

- Puede ser **Ethernet** (cableada) o **WiFi** (inalámbrica).
- Cada NIC tiene una dirección única llamada **MAC**.
- Hoy vienen integradas en la mayoría de las placas madre.

```text
Ejemplo de MAC: 00:1A:92:AF:23:8B
```



### 3.2 Hub, Switch y Router — ¿Cuál es la diferencia?

| Dispositivo | Capa           | Función                                   | Inteligencia           | ¿Se usa hoy?     |
| ----------- | -------------- | ----------------------------------------- | ---------------------- | ---------------- |
| **Hub**     | Física (OSI 1) | Repite señales a todos                    | ❌ No distingue equipos | Casi obsoleto    |
| **Switch**  | Enlace (OSI 2) | Reenvía datos dentro de la LAN usando MAC | ✅ Media                | ✅ Muy usado      |
| **Router**  | Red (OSI 3)    | Conecta redes diferentes e Internet       | ✅✅ Alta                | ✅ Imprescindible |



#### ¿Qué hace un Switch?

El switch **recibe tramas Ethernet** y las envía solo al dispositivo correcto dentro de una red local (LAN), usando una tabla interna.


```text
PC A ──┐
       │       ┌─────────┐
PC B ──┼─────▶│  Switch  │───────▶ Impresora
       │       └─────────┘
PC C ──┘
```

#### ¿Qué hace un Router?

El router permite **salir de la red local** hacia otras redes o Internet, usando **direcciones IP**.

```text
          LAN                  WAN
┌───────────────┐          ┌───────────────┐
│  Red Hogar    │--------> │    Internet   │
└───────────────┘          └───────────────┘
         ▲
         │
    ┌─────────┐
    │ Router  │
    └─────────┘

```
### 3.3 Módem

El módem es el dispositivo que convierte la señal de tu proveedor de Internet (ISP) para que pueda ser entendida por el router.

* Si el servicio es **ADSL**, usa línea telefónica.
* Si es **cable**, usa coaxial.
* Si es **fibra óptica**, puede venir con ONT (Terminal Óptica).

> Hoy muchos equipos hogareños son **Módem + Router + WiFi en uno solo** (los que entrega el ISP).



### 3.4 Access Point (AP)

Un **Punto de Acceso** permite conectar dispositivos **por WiFi** dentro de una red local.

* Se usa mucho en oficinas y escuelas para ampliar la cobertura.
* No enruta tráfico; solo conecta de forma inalámbrica.

```text
  ┌─────────┐
  │ Switch  │──────┐
  └─────────┘      │
                   ▼
             📶 Access Point
                   │
     ┌─────────────┴─────────────┐
     📱 Smartphone      💻 Notebook
```

### 3.5 Firewall

Un **firewall** controla qué tráfico entra o sale de una red.

Tipos:

* **Hardware** (generalmente en empresas)
* **Software** (firewall de Linux, Windows Defender, UFW)

Funciones:

* Filtrar puertos
* Bloquear IPs maliciosas
* Evitar accesos no autorizados



### 3.6 Tabla comparativa rápida

| Equipo   | Función principal      | ¿Trabaja con IP? | ¿Trabaja con MAC? |
| -------- | ---------------------- | ---------------- | ----------------- |
| NIC      | Conectar a red         | ❌                | ✅                 |
| Hub      | Repetir señal          | ❌                | ❌                 |
| Switch   | Conmutar dentro de LAN | ❌                | ✅                 |
| Router   | Enrutar entre redes    | ✅                | ✅                 |
| AP       | Conexión WiFi          | ❌                | ✅                 |
| Firewall | Seguridad              | ✅                | ✅                 |


#### ✅ Resumen del Tema 3

* Los switches conectan dispositivos dentro de una LAN.
* Los routers conectan redes entre sí (por ejemplo, LAN con Internet).
* El firewall protege el tráfico.
* El Access Point conecta por WiFi.


#### 🔧 Ejercicio rápido

1. ¿Qué dispositivo permite salir a Internet?
2. ¿Cuál es la diferencia entre switch y router?
3. ¿Podés tener WiFi sin un Access Point?

## 4. Protocolos de Red

En una red, los dispositivos deben “ponerse de acuerdo” para comunicarse. Ese acuerdo se define mediante **protocolos**.

Un **protocolo de red** es un conjunto de **reglas y formatos** que permiten que dos dispositivos se entiendan al intercambiar datos, sin importar su sistema operativo o fabricante.



### 4.1 ¿Qué es un protocolo?

Un protocolo define:

- Cómo se inicia una comunicación
- Cómo se estructuran los datos
- Qué hacer si hay errores
- Cómo finaliza la comunicación

Ejemplos de protocolos:

| Protocolo | Función | Capa TCP/IP |
|-----------|---------|-------------|
| HTTP | Navegación web | Aplicación |
| DNS | Resolución de nombres | Aplicación |
| SSH | Acceso remoto seguro | Aplicación |
| TCP | Comunicación confiable | Transporte |
| UDP | Comunicación rápida | Transporte |
| IP | Direccionamiento y entrega | Internet |
| ARP | Resolver IP → MAC | Acceso a red |
| ICMP | Diagnóstico de red | Internet |


### 4.2 Encapsulamiento de Datos

Cuando los datos viajan por una red, **cada capa agrega información extra** para poder enviarlos correctamente. Ese proceso se llama **encapsulamiento**.

| Aplicación  |     Datos |
|---|---|
|Transporte   |    Segmento (TCP/UDP)|
|Internet      |   Paquete (IP)|
|Acceso a red   |  Trama (Ethernet)|

📦 **Metáfora:** Es como enviar un paquete por correo:
primero lo envolvés (capa de datos), le agregás dirección (IP), luego etiqueta de envío (MAC), etc.


#### Ejemplo de encapsulamiento simplificado


### 4.3 Unidades de datos por capa

| Capa TCP/IP  | Unidad de datos | Dirección |
| ------------ | --------------- | --------- |
| Aplicación   | Datos           | N/A       |
| Transporte   | Segmento        | Puerto    |
| Internet     | Paquete         | IP        |
| Acceso a red | Trama           | MAC       |


### 4.4 Estándares en redes

Internet funciona gracias a organismos que definen estándares:

| Organización | Función                                 |
| ------------ | --------------------------------------- |
| **IETF**     | Estándares de Internet (define TCP/IP)  |
| **IEEE**     | Protocolos como Ethernet y WiFi (802.x) |
| **ISO**      | Modelo OSI y normativas                 |
| **ICANN**    | Administración de nombres de dominio    |


#### ✅ Resumen del Tema 4

* Un protocolo es un conjunto de reglas para comunicarse.
* Cada capa del modelo TCP/IP agrega encabezados → **encapsulamiento**.
* Protocolos importantes: IP, TCP, UDP, ARP, DNS, HTTP, SSH.
* IETF e IEEE son claves en el mundo de las redes.



#### 🔧 Actividad

1. ¿Qué pasaría si no existieran protocolos?
2. ¿Por qué creés que existen distintos protocolos en vez de uno solo?
3. ¿Quién define cómo funciona TCP/IP?

## 5. Modelo TCP/IP

El modelo TCP/IP es la base de las comunicaciones en Internet. Define **cómo deben transmitirse los datos** entre computadoras. Está compuesto por **4 capas**, cada una con funciones específicas.



### 5.1 ¿Qué es el modelo TCP/IP?

Es un conjunto de protocolos creados por el Departamento de Defensa de EE.UU. en los años 70 para permitir comunicaciones **confiables** entre redes distintas.  
Hoy es el **modelo oficial de Internet**.



### 5.2 Capas del modelo TCP/IP

| Capa | Función principal | Ejemplos de protocolos |
|------|-------------------|------------------------|
| **Aplicación** | Interacción con el usuario | HTTP, DNS, SSH, FTP |
| **Transporte** | Comunicación extremo a extremo | TCP, UDP |
| **Internet** | Direccionamiento y ruteo | IP, ICMP |
| **Acceso a Red** | Comunicación con el hardware | Ethernet, WiFi, ARP |



#### Diagrama general

```text
┌───────────────────────┐ 
│   Datos de Usuario    │ ← Aplicación (HTTP, DNS, SSH)
├───────────────────────┤ 
│   Segmentos           │ ← Transporte (TCP, UDP)
├───────────────────────┤ 
│   Paquetes            │ ← Internet (IP)
├───────────────────────┤ 
│   Tramas              │ ← Acceso a red (Ethernet)
└───────────────────────┘
```

### 5.3 Comparación con el modelo OSI

Aunque **TCP/IP es el modelo usado en la práctica**, muchas personas mencionan el **modelo OSI** (teórico, de 7 capas). Esta tabla muestra la equivalencia aproximada:

| Modelo OSI (teórico, 7 capas) | Modelo TCP/IP (real, 4 capas) |
| ----------------------------- | ----------------------------- |
| 7. Aplicación                 | **Aplicación**                |
| 6. Presentación               | **Aplicación**                |
| 5. Sesión                     | **Aplicación**                |
| 4. Transporte                 | **Transporte**                |
| 3. Red                        | **Internet**                  |
| 2. Enlace de datos            | **Acceso a red**              |
| 1. Física                     | **Acceso a red**              |


### 5.4 Flujo de datos entre capas

Cuando un usuario envía datos:

1. La información baja desde la **Aplicación** hasta el hardware (**Acceso a Red**).
2. Se transmite por la red física.
3. En el destino, los datos suben capa por capa hasta llegar a la aplicación.

```text
Origen                        Destino
---------                     ----------
Aplicación  ──────────────▶   Aplicación
Transporte ───────────────▶   Transporte
Internet   ───────────────▶   Internet
Acceso red ───────────────▶   Acceso red
```


### 5.5 Ejemplo real: Enviar un mensaje por WhatsApp Web

| Capa TCP/IP  | ¿Qué pasa en esta capa?      |
| ------------ | ---------------------------- |
| Aplicación   | WhatsApp usa HTTP/HTTPS      |
| Transporte   | Se abre conexión TCP         |
| Internet     | Se enruta el paquete con IP  |
| Acceso a red | Se envía por WiFi o Ethernet |


#### ✅ Resumen del Tema 5

* TCP/IP es el modelo real usado hoy en redes.
* Tiene 4 capas y organiza cómo viajan los datos.
* Cada capa tiene protocolos específicos.
* Funciona de forma modular: cada capa resuelve un problema distinto.


#### 🔧 Preguntas rápidas

1. ¿Cuál es la capa responsable de las direcciones IP?
2. ¿Qué capa permite enviar datos por Internet?
3. ¿En qué capa están HTTP y DNS?
4. ¿Qué modelo es práctico y cuál es teórico: TCP/IP u OSI?

## 6. Capa de Acceso a Red (Link Layer)

La **Capa de Acceso a Red** es la más cercana al hardware. Se encarga de **enviar datos entre dispositivos dentro de la misma red local (LAN)** usando direcciones **MAC** y tramas **Ethernet** o **WiFi**.


### 6.1 Dirección MAC

Cada dispositivo de red tiene una dirección física única llamada **MAC** (*Media Access Control*).  
Ejemplo:

```
3C:A6:F6:12:BC:8E
```

📌 Características:
- Tiene **48 bits** (6 pares hexadecimales).
- Es **única en el mundo**, asignada por el fabricante.
- Se usa **dentro de la red local**, no en Internet.
- No cambia (en teoría).

#### 📌 Ejemplo: Ver dirección MAC en Linux

Podemos ver las interfaces de red del sistema desde linux con:

```bash
ip link show
```

O desde la consola PowerShell de Windows con:

```powershell
Get-NetAdapter
```

Salida típica:

```
2: enp0s3: <BROADCAST,MULTICAST,UP> mtu 1500 ...
    link/ether 08:00:27:4a:59:3b brd ff:ff:ff:ff:ff:ff
```

➡ `08:00:27:4a:59:3b` es la **dirección MAC**.



### 6.2 Tramas Ethernet

En esta capa los datos viajan encapsulados en **tramas**:

```
┌────────┬────────┬────────┬──────────────┬─────────┐
│ MAC OR │ MAC DES│  Tipo  │    Datos     │   FCS   │
└────────┴────────┴────────┴──────────────┴─────────┘
```

| Campo       | Descripción                             |
| ----------- | --------------------------------------- |
| MAC ORIGEN  | Dirección MAC del dispositivo que envía |
| MAC DESTINO | A quién se envía                        |
| Tipo        | Define el contenido (ej: IPv4 = 0x0800) |
| Datos       | Información a enviar                    |
| FCS         | Control de errores                      |



### 6.3 Protocolo ARP (Address Resolution Protocol)

Las computadoras necesitan saber **qué MAC corresponde a qué IP** dentro de la red.
Para eso existe **ARP**.

Ejemplo:

> "Quiero enviar a la IP 192.168.0.5. ¿Cuál es su MAC?"

```text
PC A: "¿Quién tiene 192.168.0.5?" → Broadcast
PC B: "Yo, mi MAC es AA:BB:CC:DD:EE:FF"
```

Cada PC guarda esta información en una **tabla ARP** para no preguntar siempre.


#### 🔧 Comandos útiles en Linux (ARP)

Ver la tabla AR (linux):

```bash
ip neigh
```

o (linux):

```bash
arp -n
```

Ejemplo de salida:

```
192.168.0.10 dev enp0s3 lladdr 8c:85:90:12:4f:aa REACHABLE
```


Desde PowerShell (Windows) el comando es:

```Powershell
Get-NetNeighbor
```

Ejemplo de salida:

```
ifIndex IPAddress      LinkLayerAddress  State       PolicyStore
------- ---------      ----------------  -----       ------------
12      192.168.1.1    00-14-22-01-23-45 Reachable   ActiveStore
12      192.168.1.15   3C-52-82-9A-4B-11 Stale       ActiveStore
```
### 6.4 MTU y fragmentación

La **MTU** (*Maximum Transmission Unit*) define el **máximo tamaño** de datos que puede enviarse en una trama.

* En Ethernet normalmente es **1500 bytes**.
* Si se envía más, se **fragmenta**.

Ver MTU en Linux:

```bash
ip link show
```

Ver MTU en Windows (Powershell):

```Powershell
Get-NetIPInterface
```
### ✅ Resumen del Tema 6

* La capa de acceso usa **MAC** y **tramas** para enviar datos localmente.
* **ARP** vincula direcciones IP ↔ MAC.
* Podés ver interfaces y MAC con `ip link show`.
* `ip neigh` muestra la tabla ARP.

### 🔧 Práctica Linux #1 (hands-on)

1. Listar interfaces de red:

```bash
ip link show
```
2. Obtener tu MAC:

```bash
ip addr show
```
3. Ver la tabla ARP:

```bash
ip neigh
```
4. Limpiar la tabla ARP:

```bash
sudo ip neigh flush all
```
5. Probar reconexión al reenviar tráfico:

```bash
ping google.com
```

### 💻 Práctica Windows #1 — Redes (Hands-on)

1. **Listar interfaces de red:**
```powershell
Get-NetAdapter
```

2. **Obtener la dirección MAC:**

```powershell
Get-NetAdapter | Select-Object Name, MacAddress
```

3. **Ver la tabla ARP (vecinos de red):**

```powershell
Get-NetNeighbor
```

4. **Limpiar la tabla ARP:**

```powershell
Get-NetNeighbor | Remove-NetNeighbor -Confirm:$false
```

5. **Probar la reconexión reenviando tráfico:**

```powershell
Test-Connection google.com
```

## 7. Capa de Internet (Network Layer)

La **Capa de Internet** es responsable de **direccionar y enrutar paquetes** desde el origen hasta el destino, incluso si están en redes diferentes. Su protocolo principal es **IP (Internet Protocol)**.

### 7.1 Dirección IP

Una **dirección IP** identifica de forma lógica a un dispositivo dentro de una red. Existen dos versiones activas:

| Versión | Formato | Ejemplo |
|----------|----------|---------|
| **IPv4** | 32 bits (4 números) | 192.168.0.15 |
| **IPv6** | 128 bits (hexadecimal) | 2001:db8::ff00:42:8329 |

Nos enfocaremos primero en **IPv4**, ya que sigue siendo la más usada.

### 7.2 IPv4: cómo funciona

Una dirección IPv4 está formada por 4 números (octetos) entre 0 y 255:

```text
192.168.1.10
```

Cada IP tiene **dos partes**:

| Parte    | Función                                     |
| -------- | ------------------------------------------- |
| **Red**  | Identifica la red                           |
| **Host** | Identifica el dispositivo dentro de esa red |

Ejemplo:

| Red       | Host |
| --------- | ---- |
| 192.168.1 | .10  |


### 7.3 Máscara de Subred (Subnet Mask)

La **máscara** indica **cuántos bits corresponden a la red** y cuántos al host.

Ejemplo típico:

| IP           | Máscara       | Red       |
| ------------ | ------------- | --------- |
| 192.168.1.10 | 255.255.255.0 | Red `/24` |

📌 `/24` significa que los **primeros 24 bits** son de red.

### 7.4 Tipos de IP

| Tipo         | Ejemplo      | Uso                        |
| ------------ | ------------ | -------------------------- |
| **Privada**  | 192.168.0.5  | Dentro de LAN              |
| **Pública**  | 181.44.56.10 | Visible desde Internet     |
| **Loopback** | 127.0.0.1    | Localhost (máquina propia) |
| **APIPA**    | 169.254.x.x  | Sin DHCP (error)           |

Rangos privados oficiales:

```
10.0.0.0      – 10.255.255.255
172.16.0.0    – 172.31.255.255
192.168.0.0   – 192.168.255.255
```
### 7.5 Gateway (Puerta de Enlace)

El **gateway** es la dirección IP **del router**.
Es el dispositivo que permite **salir de la red local** hacia otras redes o Internet.

Ejemplo:

```text
PC: 192.168.1.20
Gateway: 192.168.1.1  ← Router
```

### 7.6 ICMP (ping y traceroute)

**ICMP** es un protocolo usado para **diagnóstico de red**.

Comando para verificar conectividad:

```bash
ping 8.8.8.8
```

Comando para ver el recorrido de los paquetes:

```bash
traceroute google.com     # Linux
tracert google.com        # Windows
```

### 7.7 IPv6 (introducción)

IPv6 nació porque IPv4 **se quedó sin direcciones**. Usa direcciones más largas.

Ejemplo de IPv6:

```text
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

Se acorta así:

```text
2001:db8:85a3::8a2e:370:7334
```

Ventajas:
✅ Más direcciones
✅ Soporte nativo para seguridad (IPSec)
✅ Mejor routing

### ✅ Resumen del Tema 7

* IP identifica dispositivos lógicamente.
* IPv4 sigue siendo muy usado; IPv6 viene creciendo.
* Gateway permite salir de la red local.
* ICMP sirve para diagnosticar conectividad.
* Ping y traceroute son herramientas clave.

### 🔧 Práctica Linux #2

1. Ver tu dirección IP:

```bash
ip addr show
```
2. Ver tabla de rutas:

```bash
ip route
```
3. Probar conexión con Google:

```bash
ping -c 4 8.8.8.8
```
4. Ver recorrido de paquetes:

```bash
traceroute google.com
```
5. Ver IPv6 local:

```bash
ip -6 addr
```

### 💻 Práctica Windows #2 — Redes (Hands-on)

1. **Ver tu dirección IP:**
```powershell
Get-NetIPAddress
```

2. **Ver la tabla de rutas:**

```powershell
Get-NetRoute
```

3. **Probar conexión con Google:**

```powershell
Test-Connection 8.8.8.8 -Count 4
```

4. **Ver el recorrido de paquetes (traceroute):**

```powershell
tracert google.com
```

5. **Ver direcciones IPv6 locales:**

```powershell
Get-NetIPAddress -AddressFamily IPv6
```


## 8. Capa de Transporte (Transport Layer)

La **capa de transporte** permite que dos aplicaciones se comuniquen entre sí a través de la red, sin importar qué dispositivos intermedios haya. En esta capa aparecen dos protocolos clave: **TCP** y **UDP**.



### 8.1 ¿Qué hace la capa de transporte?

- Establece **comunicación extremo a extremo**
- Usa **puertos** para direccionar programas
- Puede asegurar que los datos lleguen completos (TCP) o priorizar velocidad (UDP)
- Divide datos grandes en **segmentos**



### 8.2 Puertos: ¿cómo se identifican las aplicaciones?

Un **puerto** es un número que representa una aplicación en ejecución.  
Por ejemplo:

| Servicio | Puerto | Protocolo |
|----------|--------|-----------|
| HTTP     | 80     | TCP       |
| HTTPS    | 443    | TCP       |
| SSH      | 22     | TCP       |
| DNS      | 53     | UDP       |

> 📌 Una dirección de red completa es: `IP + Puerto`  
Ejemplo: `192.168.0.20:22` → SSH



### 8.3 Protocolo TCP – Confiable

TCP (*Transmission Control Protocol*) garantiza que los datos lleguen completos y en orden.

Características:
✅ Confiable  
✅ Detecta errores  
✅ Reenvía paquetes perdidos  
❌ Más lento que UDP  

Establece una conexión con **"Three-way Handshake"**:

```text
Cliente → SYN → Servidor
Cliente ← SYN/ACK ← Servidor
Cliente → ACK → Servidor
```



### 8.4 Protocolo UDP – Rápido

UDP (*User Datagram Protocol*) **no garantiza** entrega confiable. Se usa cuando importa la velocidad.

Características:
✅ Rápido
✅ Menor latencia
❌ Sin control de errores
❌ Puede perder paquetes

Ejemplos de uso:

* Streaming (YouTube, Twitch)
* Juegos online
* Videollamadas



### 8.5 Diferencias entre TCP y UDP

| Característica | TCP   | UDP  |
| -------------- | ----- | ---- |
| Confiable      | ✅     | ❌    |
| Velocidad      | Media | Alta |
| Orden de datos | ✅     | ❌    |
| Streaming      | ❌     | ✅    |
| Web/SSH        | ✅     | ❌    |



#### 🔧 Práctica Linux #3 – Explorando puertos y conexiones

Ver puertos abiertos en tu máquina:

```bash
ss -tulnp
```

Probar servidor UDP con Netcat:

```bash
nc -u -l 5000
```

Probar servidor TCP simple:

```bash
nc -l 4000
```

Desde otra terminal, enviar datos:

```bash
echo "hola red" | nc localhost 4000
```



#### ✅ Resumen del Tema 8

* La capa de transporte conecta **aplicación con aplicación**.
* Los puertos permiten identificar programas.
* TCP = confiable; UDP = rápido.
* Herramientas útiles: `ss`, `nc`.



#### 🔧 Ejercicio rápido

1. ¿Qué puerto usa HTTP?
2. ¿Qué es más rápido para streaming: TCP o UDP?
3. ¿Qué comando muestra conexiones de red?

## 9. Capa de Aplicación

La **capa de aplicación** es la más cercana al usuario.  
Aquí viven los **protocolos que permiten usar Internet**: navegar, enviar correos, acceder por consola remota o resolver nombres de dominio.

Su función es **proporcionar servicios a las aplicaciones** (navegador, cliente SSH, etc.) usando los protocolos de transporte TCP o UDP.



### 9.1 HTTP y HTTPS

**HTTP (HyperText Transfer Protocol)** permite la transferencia de páginas web.

- Usa el puerto **80** (TCP)
- Cliente: navegador web
- Servidor: Apache, Nginx, etc.

```text
Navegador → Solicita recurso (GET /index.html)
Servidor  → Devuelve página web
```

**HTTPS** es la versión segura, que usa **TLS/SSL** para cifrar los datos.
Usa el puerto **443 (TCP)**.

Ver cabeceras de una página con `curl`:

```bash
curl -I https://www.utn.edu.ar
```



### 9.2 DNS (Domain Name System)

DNS traduce **nombres de dominio** en direcciones IP.

Ejemplo:

```text
www.google.com → 142.250.64.110
```

* Puerto **53 (UDP/TCP)**
* Servidores DNS comunes: 8.8.8.8 (Google), 1.1.1.1 (Cloudflare)

Ver resolución DNS (Linux):

```bash
dig www.google.com
```

o

```bash
   host www.google.com
```

En Windows:

```powershell
Resolve-DnsName www.google.com
```


### 9.3 SSH (Secure Shell)

**SSH** permite conectarse a otra computadora de forma segura (encriptada) mediante una terminal.

* Puerto **22 (TCP)**
* Sustituye al antiguo Telnet

Ejemplo:

```bash
ssh usuario@192.168.0.10
```

Copiar archivos mediante SSH:

```bash
scp archivo.txt usuario@192.168.0.10:/home/usuario/
```



### 9.4 DHCP (Dynamic Host Configuration Protocol)

**DHCP** asigna automáticamente direcciones IP a los dispositivos al conectarse a la red.

Flujo básico:

1. Cliente: “¿Alguien puede darme una IP?”
2. Servidor DHCP: “Sí, tomá 192.168.1.50”
3. Cliente la acepta y la configura.



#### 🔧 Práctica Linux #4

1. Ver cabeceras de una web:

   ```bash
   curl -I https://www.google.com
   ```
2. Resolver un dominio:

   ```bash
   dig openai.com
   ```
3. Verificar IP actual:

   ```bash
   ip addr
   ```
4. Probar conexión SSH (si hay un servidor disponible):

   ```bash
   ssh usuario@host
   ```

#### 💻 Práctica Windows #4 — Redes (Hands-on)

1. **Ver cabeceras de una web:**
```powershell
Invoke-WebRequest -Uri "https://www.google.com" -Method Head
```

2. **Resolver un dominio:**

```powershell
Resolve-DnsName openai.com
```

3. **Verificar IP actual:**

```powershell
Get-NetIPAddress
```

4. **Probar conexión SSH (si hay un servidor disponible):**

```powershell
ssh usuario@host
```


#### ✅ Resumen del Tema 9

* HTTP/HTTPS: navegación web.
* DNS: convierte nombres en IP.
* SSH: conexión segura por terminal.
* DHCP: asigna IP automáticamente.



#### 🔧 Ejercicio rápido

1. ¿Qué puerto usa SSH?
2. ¿Qué hace DNS?
3. ¿Cuál es la diferencia entre HTTP y HTTPS?
4. ¿Qué comando permite resolver un dominio en Linux?

## 10. Redes WiFi (WLAN)

Las **redes WiFi** permiten conectar dispositivos sin cables mediante ondas de radio.  
Su nombre técnico es **WLAN (Wireless Local Area Network)**.



### 10.1 Conceptos básicos

- **SSID (Service Set Identifier):** nombre de la red.
- **Banda de frecuencia:** el rango general de frecuencia de radio utilizado (2.4 GHz o 5 GHz).
- **Canal:** una subdivisión específica dentro de una banda de frecuencia. Los canales permiten que múltiples redes WiFi coexistan en la misma banda sin interferir entre sí directamente.
- **BSSID:** dirección MAC del punto de acceso.
- **Estándares IEEE 802.11:** definen la velocidad y alcance de las redes WiFi.

| Estándar | Frecuencia | Velocidad máx. | Año |
|--|-|-|--|
| 802.11b | 2.4 GHz | 11 Mbps | 1999 |
| 802.11g | 2.4 GHz | 54 Mbps | 2003 |
| 802.11n | 2.4/5 GHz | 600 Mbps | 2009 |
| 802.11ac | 5 GHz | 1.3 Gbps | 2014 |
| 802.11ax (WiFi 6) | 2.4/5 GHz | 9.6 Gbps | 2019 |



### 10.2 Cómo funciona una red WiFi

Un **punto de acceso (Access Point)** actúa como “switch inalámbrico”.  
Cada dispositivo se asocia a ese AP y usa ondas de radio para transmitir datos.

```text
             🌐 Internet
                  │
            ┌───────────────┐
            │   Router/AP   │
            └───────┬───────┘
                    │  WiFi
      ┌─────────────┼─────────────┐
      │             │             │
   📱 Celular     💻 Notebook   🖥️ PC con WiFi
```

El router convierte las señales **inalámbricas (WiFi)** en **cableadas (Ethernet)** para llegar a Internet.



### 10.3 Seguridad WiFi

Las redes WiFi deben estar **cifradas** para evitar accesos no autorizados.

| Tipo     | Seguridad              | Estado actual        |
| -- | - | -- |
| **WEP**  | Muy débil              | Obsoleto             |
| **WPA**  | Mejor, pero vulnerable | Desaconsejado        |
| **WPA2** | Estándar actual        | Seguro si se usa AES |
| **WPA3** | Nueva generación       | Recomendado          |

Consejos:

* Usar contraseñas largas y no triviales.
* Desactivar WPS.
* Actualizar el firmware del router.



### 10.4 Interferencia y cobertura

Factores que afectan el rendimiento:

* Paredes gruesas
* Microondas y teléfonos inalámbricos
* Otros routers cercanos en el mismo canal

Ver redes cercanas (Linux):

```bash
nmcli dev wifi list
```

Ver detalles de tu conexión:

```bash
iwconfig
```

### 💻 Práctica Windows #5 — Redes Wi-Fi (Hands-on)

1. **Ver redes Wi-Fi cercanas:**

```powershell
netsh wlan show networks mode=bssid
```

- *Muestra todas las redes inalámbricas detectadas, junto con SSID, tipo de autenticación y nivel de señal.*

2. **Ver detalles de tu conexión actual:**

```powershell
netsh wlan show interfaces
```

- *Muestra información detallada sobre la interfaz Wi-Fi activa, incluyendo SSID conectado, dirección MAC, canal, velocidad, y más.*



#### 🔧 Práctica Linux #5 

1. Listar redes disponibles:

   ```bash
   nmcli dev wifi
   ```
2. Ver el SSID y BSSID actuales:

   ```bash
   iwgetid
   ```
3. Mostrar información de señal:

   ```bash
   iwconfig wlan0
   ```
4. Ver IP asignada por WiFi:

   ```bash
   ip addr show wlan0
   ```

#### 💻 Práctica Windows #5 (opcional) — Redes Wi-Fi

1. **Listar redes Wi-Fi disponibles:**
```powershell
netsh wlan show networks mode=bssid
```

2. **Ver el SSID y BSSID actuales:**

```powershell
netsh wlan show interfaces | Select-String "SSID","BSSID"
```

3. **Mostrar información de la señal y velocidad:**

```powershell
netsh wlan show interfaces
```

4. **Ver la IP asignada por Wi-Fi:**

```powershell
Get-NetIPAddress -InterfaceAlias "Wi-Fi"
```



#### ✅ Resumen del Tema 10

* WiFi = comunicación inalámbrica dentro de una LAN.
* SSID es el nombre de la red; WPA2/WPA3, los estándares de seguridad.
* La calidad depende del canal y la potencia de señal.
* Comandos útiles: `nmcli`, `iwconfig`, `iwgetid`.



#### 🔧 Actividad breve

1. ¿Qué diferencia hay entre un router y un Access Point?
2. ¿Por qué conviene usar WPA3?
3. ¿Qué comando muestra la intensidad de la señal?

## 11. NAT y Resolución de Nombres

En una red local (LAN), los dispositivos suelen tener **direcciones IP privadas**, que no son válidas en Internet.  
El mecanismo que permite que estos equipos accedan a Internet se llama **NAT (Network Address Translation)**.



### 11.1 ¿Qué es NAT?

**NAT** traduce direcciones **privadas ↔ públicas** para que varios equipos puedan compartir una sola IP pública (la del router).

Ejemplo:

| Dispositivo | IP privada | IP pública (salida) |
|--|---|--|
| PC1 | 192.168.1.10 | 190.17.8.44 |
| PC2 | 192.168.1.11 | 190.17.8.44 |
| Notebook | 192.168.1.12 | 190.17.8.44 |

Todos salen a Internet usando **la misma IP pública** gracias al router.



#### Diagrama NAT (traducción de direcciones)

```text
LAN (Privada)                     WAN (Internet)
                           ┌─────────────────────────────┐
PC1 192.168.1.10 ─┐        │   IP pública: 190.17.8.44   │
PC2 192.168.1.11 ─┼──▶ 🧭 │   NAT (Router)              │
PC3 192.168.1.12 ─┘        │   Traduce IPs               │
                           └─────────────────────────────┘
```



### 11.2 Tipos de NAT

| Tipo                               | Descripción                                    | Uso           |
| - | - | - |
| **SNAT (Source NAT)**              | Traduce IP de origen (salida a Internet)       | Hogares       |
| **DNAT (Destination NAT)**         | Traduce IP de destino (entrada desde Internet) | Servidores    |
| **PAT (Port Address Translation)** | Traduce IP y puerto                            | Uso más común |



#### Ejemplo de PAT

El router recuerda qué puerto usó cada dispositivo:

| IP privada   | Puerto local | IP pública  | Puerto público |
|--|--|--|--|
| 192.168.1.10 | 50000        | 190.17.8.44 | 30001          |
| 192.168.1.11 | 50001        | 190.17.8.44 | 30002          |

Así, cuando vuelven los paquetes, el router sabe a quién corresponden.



### 11.3 Resolución de Nombres (DNS)

Cuando escribimos un dominio en el navegador, el sistema necesita saber **qué IP** tiene ese nombre.
Esto lo hace el **DNS**, que ya vimos en la capa de aplicación.

Flujo típico:

```text
1. PC pregunta: "¿Cuál es la IP de openai.com?"
2. Servidor DNS responde: "104.18.12.110"
3. El navegador se conecta a esa IP.
```

Ver qué DNS usa tu sistema (Linux):

```bash
cat /etc/resolv.conf
```

Para ver los servidores DNS configurados en tu sistema Windows:

```powershell
Get-DnsClientServerAddress
```


#### 🔧 Ejemplo práctico con NAT (Docker)

Podemos simular NAT fácilmente con contenedores Docker.

Listar redes:

```bash
docker network ls
```

Inspeccionar la red *bridge* (que usa NAT por defecto):

```bash
docker network inspect bridge
```

Verás que las IP privadas (172.x.x.x) se traducen al salir a Internet a través del host.



#### ✅ Resumen del Tema 11

* NAT traduce IP privadas a públicas.
* Permite que muchos dispositivos compartan una sola IP.
* DNS traduce nombres a direcciones IP.
* PAT es el tipo de NAT más común.
* En Docker también se usa NAT internamente.



#### 🔧 Actividad breve

1. ¿Qué función cumple el NAT en un router doméstico?
2. ¿Cuál es la diferencia entre SNAT y DNAT?
3. ¿Qué comando te permite ver qué DNS está usando tu PC?
4. ¿Qué relación hay entre Docker y NAT?

## 12. Diagnóstico y Herramientas de Red

Cuando algo falla en una red, los administradores necesitan **ver qué ocurre realmente** con los paquetes que entran y salen.  
Existen herramientas que permiten diagnosticar, analizar y medir el tráfico.



### 12.1 Resolución de problemas de red

Los pasos más comunes para diagnosticar fallos son:

1. **Verificar la conexión física**
   - ¿El cable está conectado?
   - ¿La interfaz WiFi está activa?

2. **Comprobar la configuración IP** 

Linux:
```bash
ip addr 
```
Windows (PowerShell):
```powershell
Get-NetIPAddress
```

3. **Verificar conectividad local**

```bash
ping 192.168.1.1
```

4. **Verificar salida a Internet**

```bash
ping 8.8.8.8
```

5. **Verificar resolución de nombres**

```bash
ping google.com
```

6. **Ver rutas de salida**

Linux:
```bash
ip route
```

Windows (PowerShell):
```powershell
Get-NetRoute
```


### 12.2 Analizador de tráfico: Wireshark

**Wireshark** es una herramienta gráfica que permite **capturar y analizar paquetes** que pasan por una interfaz de red. La podés descargar desde [el sitio oficial de Wireshark](https://www.wireshark.org/download.html).

Muestra cada paquete con:

* Protocolo (IP, TCP, DNS, etc.)
* IP origen/destino
* Puerto
* Tiempo y tamaño

Ejemplo de uso:

1. Abrir Wireshark
2. Seleccionar la interfaz (por ejemplo, `wlan0`)
3. Filtrar por protocolo:

   * `icmp` → solo pings
   * `tcp.port == 80` → solo HTTP
   * `ip.addr == 8.8.8.8` → tráfico con Google DNS

💡 Tip: Podés usarlo en modo “offline” cargando un archivo `.pcap`.



### 12.3 Captura de tráfico en consola: tcpdump (Linux)

Si no tenés entorno gráfico, podés usar **tcpdump**, una versión por terminal.

Ejemplo:

```bash
sudo tcpdump -i any icmp
```

Captura todo el tráfico ICMP (pings).
Para detenerlo: `Ctrl + C`

Guardar la captura en un archivo:

```bash
sudo tcpdump -i wlan0 -w captura.pcap
```

Luego podés abrirla en Wireshark.


### 12.3 Captura de tráfico en Windows (sin entorno gráfico)

Si no tenés entorno gráfico, podés usar **tshark**, la versión por consola de Wireshark.

1. **Capturar tráfico ICMP (pings):**
```powershell
tshark -i 1 icmp
```

🔹 *Captura todo el tráfico ICMP en la interfaz número 1 (podés listar las interfaces con `tshark -D`).*
🔹 Para detener la captura: `Ctrl + C`

2. **Guardar la captura en un archivo:**

```powershell
tshark -i Wi-Fi -w captura.pcap
```

- *Guarda los paquetes en formato `.pcap`, compatible con Wireshark.*

3. **Ver las interfaces disponibles:**

```powershell
tshark -D
```

4. **Abrir la captura en Wireshark (modo gráfico):**

   * Iniciar Wireshark y abrir el archivo `captura.pcap`.

> 💡 **Nota:** `tshark` se instala junto con Wireshark y puede ejecutarse desde PowerShell o CMD.


### 12.4 Otras herramientas útiles

| Herramienta      | Función                       | Ejemplo                 |
| - | -- | -- |
| **ping**         | Verifica conectividad         | `ping 8.8.8.8`          |
| **traceroute**   | Rastrea la ruta de un paquete | `traceroute openai.com` |
| **netstat / ss** | Muestra puertos abiertos      | `ss -tulnp`             |
| **dig / host**   | Consultas DNS                 | `dig google.com`        |
| **nmap**         | Escanea equipos y puertos     | `nmap 192.168.1.0/24`   |

> ⚠️ Usa `nmap` solo en entornos propios o de práctica. Escanear redes ajenas puede ser ilegal.

#### 🔧 Práctica Linux #6

1. Verificar conectividad:

```bash
ping -c 4 google.com
```

2. Analizar tráfico ICMP:

```bash
sudo tcpdump -i any icmp
```

3. Capturar tráfico HTTP:

```bash
sudo tcpdump -i wlan0 port 80
```
4. Filtrar tráfico DNS en Wireshark:

```
udp.port == 53
```

#### 💻 Práctica Windows #6 — Análisis de Red (Hands-on)

1. **Verificar conectividad:**
```powershell
Test-Connection google.com -Count 4
```

2. **Analizar tráfico ICMP:**

```powershell
tshark -i 1 icmp
```

- *Captura paquetes ICMP (pings) en la interfaz número 1. Detener con `Ctrl + C`.*
   *(Listar interfaces con `tshark -D`.)*

3. **Capturar tráfico HTTP:**

```powershell
tshark -i Wi-Fi -f "tcp port 80"
```

- *Muestra o guarda paquetes HTTP. Podés reemplazar `"Wi-Fi"` por el nombre o número de la interfaz.*

4. **Filtrar tráfico DNS en Wireshark:**

```
udp.port == 53
```

- *Usá este filtro dentro de Wireshark o TShark para mostrar solo tráfico DNS.*



#### ✅ Resumen del Tema 12

* Wireshark = análisis gráfico de red.
* tcpdump = captura de paquetes en consola.
* Comandos como ping, traceroute y ss ayudan a diagnosticar.
* Siempre probar primero desde lo local hacia lo externo.

#### 🔧 Actividad breve

1. ¿Qué diferencia hay entre Wireshark y tcpdump?
2. ¿Qué comando te permite ver si tu PC llega a Internet?
3. ¿Qué puerto usa DNS para sus consultas?
4. ¿Qué precaución deberías tener al usar nmap?

## 13. Redes con Docker

Docker no solo aísla procesos y sistemas de archivos, también crea **redes virtuales** para conectar contenedores entre sí o con Internet.  
Comprender su funcionamiento es esencial para quienes desarrollan aplicaciones distribuidas.



### 13.1 Concepto de red virtual

Cuando instalás Docker, automáticamente se crean varias **redes internas**.  
Cada contenedor conectado a una red virtual tiene una **IP privada**, como si fuera una mini-LAN dentro del host.

Ver redes disponibles:

```bash
docker network ls
```

Ejemplo de salida:

```
NETWORK ID     NAME      DRIVER    SCOPE
b11c8d81c1a2   bridge    bridge    local
74b2e1fefb64   host      host      local
a8ff31a3d9f1   none      null      local
```



### 13.2 Tipos de redes Docker

| Nombre      | Descripción               | Dirección IP |
|---|-|-|
| **bridge**       | Red por defecto. Conecta contenedores entre sí y al host mediante NAT. | 172.x.x.x    |
| **host**         | El contenedor usa la red del host directamente (sin aislamiento).      | IP del host  |
| **none**         | Sin red asignada (aislamiento total).                                  | —            |
| **user-defined** | Red personalizada creada por el usuario.                               | Configurable |



### 13.3 Inspeccionar una red

Podemos ver detalles de una red (como las IPs internas de los contenedores):

```bash
docker network inspect bridge
```

Ejemplo de salida abreviada:

```json
"Containers": {
    "a4b32c...": {
        "Name": "web",
        "IPv4Address": "172.17.0.2/16"
    },
    "b7d91a...": {
        "Name": "db",
        "IPv4Address": "172.17.0.3/16"
    }
}
```



### 13.4 Crear una red personalizada

Podemos crear una red propia para aislar un conjunto de contenedores:

```bash
docker network create mi_red
```

Luego, al crear los contenedores:

```bash
docker run -d --name servidor --network mi_red nginx
docker run -d --name cliente --network mi_red alpine sleep infinity
```

Dentro del contenedor `cliente`, podés hacer ping al otro:

```bash
docker exec -it cliente ping servidor
```

> ✅ Docker resuelve automáticamente los nombres por DNS dentro de la red (¡no hace falta usar IPs!).



### 13.5 Cómo Docker usa NAT

Las redes tipo `bridge` usan **NAT** para salir a Internet:
los contenedores tienen IPs privadas (172.x.x.x), pero Docker traduce la salida a la IP pública del host.

```text
[ Contenedor 172.17.0.2 ] ──▶ [ Host NAT ] ──▶ 🌐 Internet
```



### 13.6 Comunicación entre redes

* Los contenedores dentro de **la misma red Docker** pueden comunicarse por nombre.
* Los de **redes distintas** no, salvo que se cree una conexión manual (`docker network connect`).

Ejemplo:

```bash
docker network connect mi_red servidor2
```



#### 🔧 Práctica Docker #1

1. Ver redes existentes:

```bash
docker network ls
```
2. Crear red personalizada:

```bash
docker network create red_app
```
3. Lanzar contenedores conectados:

```bash
docker run -d --name api --network red_app nginx
docker run -it --name cliente --network red_app alpine sh
```
4. Probar conectividad:

```bash
ping api
```
5. Ver direcciones IP:

```bash
docker network inspect red_app
```



#### ✅ Resumen del Tema 13

* Docker crea redes virtuales para sus contenedores.
* `bridge` es la red por defecto (usa NAT).
* Se pueden crear redes personalizadas para aislar aplicaciones.
* Los contenedores dentro de la misma red pueden comunicarse por nombre.



#### 🔧 Actividad breve

1. ¿Qué diferencia hay entre red *bridge* y *host*?
2. ¿Qué hace Docker cuando un contenedor “sale” a Internet?
3. ¿Por qué conviene crear redes personalizadas?
4. ¿Qué comando permite inspeccionar una red?

## 14. Mini Práctica con Python (Sockets)

Los **sockets** permiten a dos programas comunicarse entre sí a través de una red.  
Podemos crear clientes y servidores que usen **TCP (confiable)** o **UDP (rápido)**, igual que los protocolos del modelo TCP/IP.



### 14.1 Concepto de socket

Un **socket** es un punto de comunicación identificado por una **dirección IP** y un **puerto**.

Ejemplo:  
`192.168.1.20:5000` → Socket TCP en la PC con IP 192.168.1.20 escuchando en el puerto 5000.



### 14.2 Servidor TCP en Python

Crea un archivo llamado `servidor_tcp.py` con el siguiente contenido:

```python
import socket

## Crear socket TCP (SOCK_STREAM)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("0.0.0.0", 5000))   ## Escuchar en todas las interfaces
servidor.listen(1)

print("Servidor TCP escuchando en puerto 5000...")

conn, addr = servidor.accept()
print(f"Conexión establecida desde {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Mensaje recibido:", data.decode())
    conn.sendall(b"OK - recibido")

conn.close()
```

Ejecutalo con:

```bash
python3 servidor_tcp.py
```



### 14.3 Cliente TCP en Python

En otra terminal o equipo, creá `cliente_tcp.py`:

```python
import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("127.0.0.1", 5000))

mensaje = input("Escribí un mensaje: ")
cliente.sendall(mensaje.encode())

respuesta = cliente.recv(1024)
print("Servidor respondió:", respuesta.decode())

cliente.close()
```

Probá enviando mensajes entre ambos.
Si todo sale bien, verás en el servidor cada mensaje que llega.



### 14.4 Comunicación UDP en Python

UDP no establece conexión: simplemente envía datagramas.

#### Servidor UDP (`servidor_udp.py`)

```python
import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(("0.0.0.0", 6000))

print("Servidor UDP escuchando en puerto 6000...")

while True:
    data, addr = servidor.recvfrom(1024)
    print(f"Mensaje de {addr}: {data.decode()}")
    servidor.sendto(b"Recibido UDP", addr)
```

#### Cliente UDP (`cliente_udp.py`)

```python
import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.sendto(b"Hola desde UDP", ("127.0.0.1", 6000))

data, addr = cliente.recvfrom(1024)
print("Respuesta:", data.decode())
```



### 14.5 Observá los paquetes en Wireshark

Mientras ejecutás los programas:

* Filtrá por `tcp.port == 5000` o `udp.port == 6000`
* Vas a ver las tramas con tus mensajes

Esto te permitirá visualizar **cómo viajan los datos en tiempo real**.



#### ✅ Resumen del Tema 14

* Un **socket** combina una IP y un puerto.
* TCP requiere conexión; UDP solo envía datagramas.
* Con Python podés crear tus propios clientes y servidores.
* Wireshark permite analizar los paquetes generados.



#### 🔧 Actividad práctica

1. Ejecutá el servidor TCP y el cliente TCP.
2. Capturá el tráfico con Wireshark.
3. Repetí con UDP y compará la diferencia.
4. ¿Qué pasa si cerrás el servidor y el cliente intenta enviar datos?

