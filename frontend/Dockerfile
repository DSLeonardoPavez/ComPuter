# Etapa de desarrollo
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package.json package-lock.json* ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Exponer puerto
EXPOSE 3000

# Variables de entorno
ENV REACT_APP_API_URL=http://localhost:8000

# Comando por defecto para desarrollo
CMD ["npm", "start"]

# Para producción, usar multi-stage build:
# RUN npm run build
# FROM nginx:alpine
# COPY --from=0 /app/build /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]