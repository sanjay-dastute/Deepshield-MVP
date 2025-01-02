# Build stage
FROM node:20-slim as builder

WORKDIR /app

# Install pnpm globally
RUN npm install -g pnpm

# Copy package files
COPY package*.json ./
COPY pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Set environment variable for API URL
ENV VITE_API_URL=http://localhost:8000

# Build the application
RUN pnpm build

# Production stage
FROM node:20-slim

WORKDIR /app

# Install serve for production
RUN npm install -g serve

# Copy built files from builder stage
COPY --from=builder /app/dist ./dist

# Expose port
EXPOSE 3000

# Start the application
CMD ["serve", "-s", "dist", "-l", "3000"]
