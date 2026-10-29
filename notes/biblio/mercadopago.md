## 📦 Backend (Node + Express + TS)
A continuación tenés un boilerplate mínimo en **TypeScript** para backend (Node + Express) y frontend (React + Vite) integrando **Mercado Pago** con Bricks (Wallet).
### 1) Dependencias

```bash
npm i express cors mercadopago dotenv
npm i -D typescript ts-node-dev @types/node @types/express @types/cors
```

### 2) `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020"],
    "module": "ESNext",
    "moduleResolution": "NodeNext",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "resolveJsonModule": true
  },
  "include": ["src"]
}
```

### 3) Scripts en `package.json`

```json
{
  "type": "module",
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js"
  }
}
```

### 4) `.env`

```
MP_ACCESS_TOKEN=APP_USR-XXXXXXXXXXXXXXXXXXXXXXXXX
PORT=3001
ALLOWED_ORIGINS=http://localhost:5173,https://tu-sitio.com
PUBLIC_BASE_URL=https://tu-api.com
```

> `MP_ACCESS_TOKEN` es **secreto** (sólo backend). `PUBLIC_BASE_URL` lo usamos para `notification_url` si no tenés un parámetro custom.

### 5) `src/types.d.ts` (opcional para tipar requests)

```ts
export interface CreatePreferenceItem {
  title: string;
  quantity: number | string;
  unit_price: number | string;
}

export interface CreatePreferenceBody {
  items: CreatePreferenceItem[];
  payer?: Record<string, unknown>;
  notificationUrl?: string;
}

export interface MPWebhookBody {
  id?: string | number;
  action?: string;
  type?: string;      // "payment", etc.
  data?: { id?: string | number };
  topic?: string;     // algunos envían topic
}
```

### 6) `src/server.ts`

```ts
import express, { Request, Response } from "express";
import cors from "cors";
import "dotenv/config";
import mercadopago from "mercadopago";
import type { CreatePreferenceBody, MPWebhookBody } from "./types";

// --- Config básica ---
const app = express();
app.use(express.json());

// CORS seguro (permití múltiples orígenes separados por coma en .env)
const allowed = (process.env.ALLOWED_ORIGINS || "").split(",").map(s => s.trim()).filter(Boolean);
app.use(cors({
  origin: (origin, cb) => {
    if (!origin || allowed.length === 0 || allowed.includes(origin)) return cb(null, true);
    return cb(new Error("Origen no permitido por CORS"));
  }
}));

// SDK MP (Access Token de servidor)
const accessToken = process.env.MP_ACCESS_TOKEN;
if (!accessToken) {
  throw new Error("Falta MP_ACCESS_TOKEN en .env");
}
mercadopago.configure({ access_token: accessToken });

// Healthcheck
app.get("/health", (_req, res) => res.json({ ok: true }));

// Crear preferencia
app.post("/create-preference", async (req: Request<unknown, unknown, CreatePreferenceBody>, res: Response) => {
  try {
    const { items, payer, notificationUrl } = req.body || {};
    if (!items || !Array.isArray(items) || items.length === 0) {
      return res.status(400).json({ error: "items requeridos" });
    }

    // Validación mínima y normalización del precio/cantidad en servidor
    const normalizedItems = items.map(i => ({
      title: String(i.title),
      quantity: Number(i.quantity),
      unit_price: Number(i.unit_price),
      currency_id: "ARS"
    }));

    const baseNotification = notificationUrl || `${process.env.PUBLIC_BASE_URL || ""}/webhooks/mercadopago`;

    const preference = {
      items: normalizedItems,
      payer, // opcional
      back_urls: {
        success: "https://tu-sitio.com/pago/exito",
        failure: "https://tu-sitio.com/pago/error",
        pending: "https://tu-sitio.com/pago/pendiente"
      },
      auto_return: "approved" as const,
      notification_url: baseNotification
    };

    const result = await mercadopago.preferences.create(preference as any);
    return res.json({ id: result.body.id });
  } catch (err) {
    console.error("create-preference error:", err);
    return res.status(500).json({ error: "No se pudo crear la preferencia" });
  }
});

// Webhook: Mercado Pago -> tu servidor
app.post("/webhooks/mercadopago", async (req: Request<unknown, unknown, MPWebhookBody>, res: Response) => {
  try {
    const body = req.body || {};

    // MP puede enviar {type: 'payment', data: {id}} o {topic: 'merchant_order', data: {id}}
    const eventType = body.type || body.topic;
    const id = body.data?.id || body.id;

    if (!eventType) {
      console.warn("Webhook sin tipo:", body);
      return res.sendStatus(200);
    }

    if (eventType === "payment" && id) {
      const paymentResp = await mercadopago.payment.findById(id);
      const payment = paymentResp.body;
      // TODO: actualizar DB/orden según payment.status (approved/pending/rejected)
      console.log("PAYMENT STATUS:", payment.status, "ID:", payment.id);
      return res.sendStatus(200);
    }

    if (eventType === "merchant_order" && id) {
      const orderResp = await mercadopago.merchant_orders.get(id);
      const order = orderResp.body;
      // TODO: consolidar pagos desde order.payments[*].status si preferís
      console.log("MERCHANT_ORDER:", order.id, order.payments?.map(p => p.status));
      return res.sendStatus(200);
    }

    // Otros eventos (chargebacks, etc.) pueden llegar
    console.log("Webhook no manejado:", body);
    return res.sendStatus(200);
  } catch (err) {
    console.error("Webhook error:", err);
    return res.sendStatus(500);
  }
});

const port = Number(process.env.PORT || 3001);
app.listen(port, () => {
  console.log(`API escuchando en http://localhost:${port}`);
});
```

## 💻 Frontend (React + Vite + TS)

### 1) Crear proyecto y dependencias

```bash
npm create vite@latest mp-react -- --template react-ts
cd mp-react
npm i @mercadopago/sdk-react
```

### 2) `.env` del frontend (Vite)

```
VITE_MP_PUBLIC_KEY=TEST-XXXXXXXXXXXXXXXXXXXXXXXX
VITE_API_URL=http://localhost:3001
```

### 3) `src/App.tsx`

```tsx
import { useEffect, useState } from "react";
import { initMercadoPago, Wallet } from "@mercadopago/sdk-react";

interface CreatePrefResponse { id: string }

export default function App() {
  const [preferenceId, setPreferenceId] = useState<string | null>(null);
  const API_URL = import.meta.env.VITE_API_URL as string;

  useEffect(() => {
    const pubKey = import.meta.env.VITE_MP_PUBLIC_KEY as string;
    if (!pubKey) console.warn("Falta VITE_MP_PUBLIC_KEY en .env");
    initMercadoPago(pubKey, { locale: "es-AR" });
  }, []);

  async function crearPreferencia() {
    const resp = await fetch(`${API_URL}/create-preference`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        items: [{ title: "Curso TS", quantity: 1, unit_price: 10000 }],
        notificationUrl: `${API_URL}/webhooks/mercadopago`
      })
    });

    if (!resp.ok) {
      console.error("Error creando preferencia");
      return;
    }
    const data = (await resp.json()) as CreatePrefResponse;
    setPreferenceId(data.id);
  }

  return (
    <div style={{ maxWidth: 520, margin: "2rem auto", fontFamily: "system-ui, sans-serif" }}>
      <h1>Pago con Mercado Pago</h1>
      <p>Flujo mínimo con Wallet Brick (redirect/modal de MP).</p>
      <button onClick={crearPreferencia}>Generar preferencia</button>

      {preferenceId && (
        <div style={{ marginTop: 16 }}>
          <Wallet initialization={{ preferenceId }} />
        </div>
      )}
    </div>
  );
}
```

### 4) Consejos rápidos

* En producción, configurá CORS del backend con tu dominio.
* No expongas **Access Token** en el front (usá **Public Key**).
* Guardá el estado de la orden en tu DB y **confiá en el webhook** para marcar como pagado.
* Probá approved/pending/rejected con **tarjetas de prueba**.


## 📐 Variante Checkout Pro (redirect/popup) – mínimos cambios

En el endpoint `create-preference`, además de `id`, podés leer `result.body.init_point` y redirigir desde el front:

```ts
// backend
const { id, init_point } = result.body; // devolvé ambos si querés
```

```tsx
// frontend
window.location.href = init_point; // o abrir popup según la doc
```

## ✅ Lista de verificación

* [ ] Credenciales: `MP_ACCESS_TOKEN` (server) y `VITE_MP_PUBLIC_KEY` (client)
* [ ] CORS apuntando a tu dominio real
* [ ] URL pública del webhook accesible desde MP (usar ngrok en local)
* [ ] Persistencia de órdenes + actualización por webhook
* [ ] Pruebas con tarjetas/usuarios de test
