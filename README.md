# Prueba Técnica – Django + Next.js (Dockerizado)

Este repositorio contiene una **aplicación fullstack** desarrollada como **prueba técnica**, compuesta por:

- **Backend:** Django + Django REST Framework + JWT
- **Frontend:** Next.js (App Router)
- **Infraestructura:** Docker + Docker Compose

El objetivo es que **cualquier evaluador pueda levantar el proyecto fácilmente** sin configuraciones adicionales.

---

## 🚀 Levantar el proyecto (Setup rápido)

### Requisitos
- Docker
- Docker Compose

> No es necesario tener Python, Node.js ni dependencias instaladas localmente.

---

### Pasos

```bash
git clone https://github.com/DiegoDefault04/PruebaEthical.git
cd PruebaEthical
docker compose up --build
```

Una vez finalizado el proceso:

Frontend: http://localhost:3000

Backend API: http://localhost:8000

##  🌐 Acceso al Frontend

El frontend está desarrollado en Next.js y se accede desde el navegador en:

http://localhost:3000


Desde esta interfaz, el usuario puede registrarse, validar su identidad por correo electrónico y realizar una denuncia anónima.

## 👤 Registro de Usuario y Verificación por Correo

Para poder realizar una denuncia, el usuario debe seguir el siguiente flujo:

### Registro

El usuario se registra proporcionando un correo electrónico válido.

No se solicitan datos personales sensibles.

### Código de verificación

Al registrarse, el sistema envía automáticamente un código de verificación al correo electrónico proporcionado.

Este código es necesario para confirmar que el correo es válido.

### Validación

El usuario ingresa el código recibido.

Una vez validado, su cuenta queda habilitada.

⚠️ El correo electrónico no se muestra públicamente ni se asocia a la denuncia de forma visible.