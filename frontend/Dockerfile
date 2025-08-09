FROM node:18-alpine

WORKDIR /app
COPY . .

# Force clean install and ensure all deps are built
RUN npm install --legacy-peer-deps

CMD ["npm", "start"]
