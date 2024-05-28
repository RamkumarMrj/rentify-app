# # frontend/Dockerfile
# # Build Angular
# FROM node:20-alpine as builder
# WORKDIR /app
# COPY package.json ./
# RUN npm install
# COPY . .
# RUN npm run build

# # Serve Angular using Nginx
# FROM nginx:alpine
# COPY --from=builder /app/dist /usr/share/nginx/html
# COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
# EXPOSE 80
# EXPOSE 443
# CMD ["nginx", "-g", "daemon off;"]

FROM node:20-alpine as build
WORKDIR /app/src
COPY package*.json ./
RUN npm ci
COPY . ./
RUN npm run build

FROM node:20-alpine
WORKDIR /usr/app
COPY --from=build /app/src/dist/rentify/server ./
CMD node server.mjs
EXPOSE 4000