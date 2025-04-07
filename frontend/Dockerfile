# Базовый образ с Node.js
FROM node:18-alpine

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json для установки зависимостей
COPY package.json package-lock.json ./

# Установка зависимостей
RUN npm install

# Копирование всего остального кода
COPY . .

# Открытие порта (Vite по умолчанию использует 5173)
EXPOSE 5173

# Команда для запуска dev-сервера
CMD ["npm", "run", "dev"]