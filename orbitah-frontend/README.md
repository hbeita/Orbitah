# Orbitah Frontend

A modern React frontend for the Orbitah application, built with TypeScript, Tailwind CSS, and shadcn/ui components.

## Features

- 🔐 **Authentication System** - Login and registration with JWT tokens
- 🎨 **Modern UI** - Built with shadcn/ui and Tailwind CSS
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🔄 **Real-time Updates** - Automatic token refresh and error handling
- 📊 **Dashboard** - User statistics and navigation to different sections
- 🎯 **Type Safety** - Full TypeScript support with API type definitions

## Tech Stack

- **React 19** - Latest React with hooks and modern patterns
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Beautiful and accessible UI components
- **Axios** - HTTP client for API requests
- **React Hook Form** - Form handling and validation
- **Zod** - Schema validation

## Prerequisites

- Node.js 18+
- pnpm (recommended) or npm
- Orbitah FastAPI backend running on `http://localhost:8001`

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd orbitah-frontend
   ```

2. **Install dependencies**:
   ```bash
   pnpm install
   ```

3. **Start the development server**:
   ```bash
   pnpm dev
   ```

4. **Open your browser** and navigate to `http://localhost:5173`

## Project Structure

```
src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── dashboard/
│   │   └── Dashboard.tsx
│   └── ui/          # shadcn/ui components
├── contexts/
│   └── AuthContext.tsx
├── services/
│   └── api.ts
├── types/
│   └── api.ts
├── App.tsx
└── main.tsx
```

## API Integration

The frontend is designed to work with the Orbitah FastAPI backend. The API service (`src/services/api.ts`) provides methods for:

- **Authentication**: Login, register, get current user
- **Users**: CRUD operations for user profiles
- **Groups**: Manage study groups
- **Goals**: Create and track personal/group goals
- **Focus Sessions**: Track productivity sessions
- **Achievements**: View unlocked achievements
- **Exploration**: Manage exploration state and progress

## Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm preview` - Preview production build
- `pnpm lint` - Run ESLint
- `pnpm type-check` - Run TypeScript type checking

## Configuration

### API Base URL

The API base URL is configured in `src/services/api.ts`. By default, it points to `http://localhost:8000`. Update this if your FastAPI backend runs on a different port or host.

### Environment Variables

Create a `.env` file in the root directory for environment-specific configuration:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Development

### Adding New Components

1. Use shadcn/ui CLI to add new components:
   ```bash
   pnpm dlx shadcn@latest add <component-name>
   ```

2. Create custom components in the appropriate directory under `src/components/`

### Styling

- Use Tailwind CSS classes for styling
- Follow the design system established by shadcn/ui
- Use CSS variables for theming (defined in `src/index.css`)

### State Management

- Use React Context for global state (like authentication)
- Use local state for component-specific data
- Consider using React Query for server state management in the future

## Building for Production

1. **Build the application**:
   ```bash
   pnpm build
   ```

2. **Preview the build**:
   ```bash
   pnpm preview
   ```

3. **Deploy** the `dist` folder to your hosting provider

## Contributing

1. Follow the existing code style and patterns
2. Use TypeScript for all new code
3. Add proper error handling and loading states
4. Test your changes thoroughly
5. Update documentation as needed

## Troubleshooting

### Common Issues

1. **API Connection Errors**: Ensure the FastAPI backend is running on the correct port
2. **Authentication Issues**: Check that JWT tokens are being properly stored and sent
3. **Build Errors**: Clear node_modules and reinstall dependencies
4. **TypeScript Errors**: Run `pnpm type-check` to identify type issues

### Getting Help

- Check the browser console for error messages
- Verify the API endpoints are working with tools like Postman
- Ensure all dependencies are properly installed

## License

This project is part of the Orbitah application suite.
