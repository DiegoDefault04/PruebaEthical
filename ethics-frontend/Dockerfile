FROM node:20-alpine

WORKDIR /app

# Copiamos package.json primero
COPY package*.json ./

# Instalamos dependencias (AQUÍ estaba el problema)
RUN npm install

# Copiamos el resto del proyecto
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
