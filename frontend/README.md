# Frontend Application

This document provides instructions for setting up and running the Next.js frontend application locally.

## Getting Started (Local Development)

To set up and run the frontend application for local development, follow these steps:

### 1. Navigate to the Frontend Dir and Install Dependencies

First, install all the project's dependencies. This will download all necessary packages, including Next.js, into your `node_modules` folder.

```bash
cd frontend
npm install
```

### 2. Run the Development Server

Once dependencies are installed, you can start the development server. This will compile your code, provide hot-reloading, and make the application accessible in your browser.

```bash
npm run dev
```

The frontend application will typically be available at `http://localhost:3000`.

## Troubleshooting

### Common Error: `sh: 1: next: not found` or `command not found`

This error usually indicates that the project's dependencies, including the Next.js framework, have not been installed correctly. Ensure you have run `npm install` in the `frontend` directory.