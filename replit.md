# Overview

This is a Flask-based project management system designed for managing clients, projects, and tasks with AI-powered features. The system supports user authentication with admin and regular user roles, where admins can manage users and all users can create clients and projects. The application integrates with OpenAI's GPT-5 to automatically process project transcriptions and generate structured project information and tasks.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **Flask**: Core web framework with SQLAlchemy ORM for database operations
- **Flask-Login**: User session management and authentication
- **Flask-WTF**: Form handling and validation with CSRF protection
- **Werkzeug**: Password hashing and security utilities

## Authentication & Authorization
- **Role-based access control**: Admin users can manage other users, while regular users manage clients and projects
- **Session-based authentication**: Uses Flask-Login for user session management
- **Password security**: Werkzeug password hashing for secure credential storage

## Database Architecture
- **SQLAlchemy ORM**: Database abstraction layer with declarative models
- **Relational design**: Users, Clients, Projects, and Tasks with proper foreign key relationships
- **Many-to-many relationships**: Project team members through association table
- **Connection pooling**: Configured with pool recycling and ping for reliability

## Frontend Architecture
- **Server-side rendering**: Jinja2 templates with Bootstrap 5 dark theme
- **Responsive design**: Bootstrap components for mobile-friendly interface
- **Interactive features**: JavaScript for kanban drag-and-drop functionality
- **Modal-based forms**: User-friendly form interfaces for data entry

## AI Integration
- **OpenAI GPT-5**: Processes project transcriptions to extract structured information
- **Automated task generation**: Creates tasks from transcription content
- **JSON-formatted responses**: Structured data extraction for consistent project fields

## Task Management
- **Kanban board**: Three-column layout (Pending, In Progress, Completed)
- **Drag-and-drop interface**: JavaScript-powered task status updates
- **Filtering system**: Project, client, and user-based task filtering
- **Dual creation methods**: Manual task entry and AI-generated tasks from transcriptions

## Data Models
- **User model**: Authentication, roles, and relationships to projects/tasks
- **Client model**: Customer information with project associations
- **Project model**: Core project data with AI-processed fields for scope, objectives, and constraints
- **Task model**: Task management with status tracking and user assignments

# External Dependencies

## AI Services
- **OpenAI API**: GPT-5 model for transcription processing and task generation
- **API Key Management**: Environment variable configuration for secure access

## Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme variant from Replit CDN
- **Font Awesome**: Icon library for UI enhancements
- **JavaScript Libraries**: Native DOM manipulation for kanban functionality

## Python Packages
- **Flask ecosystem**: Core framework with extensions for login, database, and forms
- **SQLAlchemy**: Database ORM and query building
- **OpenAI Python client**: API integration for AI features
- **WTForms**: Form validation and rendering

## Infrastructure
- **Environment Variables**: Database URL, session secrets, and API keys
- **WSGI Configuration**: ProxyFix middleware for deployment compatibility
- **Logging**: Debug-level logging for development and troubleshooting

## RPA Monitor Integration
- **Real-time monitoring**: WebSocket connection to RPA Monitor server
- **Activity logging**: All user actions (login, logout, CRUD operations) are logged
- **Error tracking**: Automatic error capture with severity levels (INFO, WARN, ERROR)
- **Screenshot capability**: Support for screenshot capture on errors
- **Configuration**: Via environment variables (RPA_MONITOR_ID, RPA_MONITOR_HOST, RPA_MONITOR_REGION, RPA_MONITOR_TRANSPORT)
- **Library location**: `/rpa_monitor_client/` folder with `rpa_log` functions

## Database
- **SQL Database**: Configured via DATABASE_URL environment variable
- **Connection Management**: Pool recycling and health checks for stability