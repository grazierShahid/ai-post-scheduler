FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 3000

# Set environment variable
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1

# Start the development server
CMD ["npm", "run", "dev"]