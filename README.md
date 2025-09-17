# HP Database Search System

This application provides a web interface for searching and analyzing HP strain data with user authentication.

## Features

- User authentication (register, login, password reset)
- Advanced search functionality with filters:
  - Search by strain name or gene sequence
  - Filter by country, region, host disease, and drug resistance
  - Paginated results (20 items per page by default)
  - Download search results as CSV
- Admin dashboard for user management
- Real-time updates
- Responsive design for desktop and mobile

## Prerequisites

- Node.js (v16 or higher)
- PostgreSQL (v12 or higher)
- Python 3.8+ (for data import script)
- npm or yarn (Node.js package manager)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wechat4
   ```

2. **Set up environment variables**
   ```bash
   # Run the setup script (Python 3.8+ required)
   python setup_env.py
   
   # Or manually create a .env file with your configuration
   cp .env.example .env
   # Edit the .env file with your settings
   ```

3. **Install dependencies**
   ```bash
   # Install Node.js dependencies
   npm install
   
   # Install Python dependencies (for data import)
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   # Create the database (PostgreSQL must be running)
   createdb hpdata -U postgres
   
   # Initialize the database schema
   psql -U postgres -d hpdata -f init_db.sql
   
   # Import data from CSV
   python import_data.py
   ```

5. **Start the application**
   ```bash
   # Development mode with hot-reload
   npm run dev
   
   # Production mode
   npm start
   ```

The application will be available at `http://localhost:3000`

## Search Functionality

The search system provides powerful querying capabilities:

### Basic Search
- Enter text in the search box to find matching strains or gene sequences
- Search is case-insensitive and supports partial matches

### Advanced Filters
- **Country**: Filter by country of origin
- **Region**: Filter by specific region within a country
- **Host Disease**: Filter by associated diseases
- **Drug Resistance**: Filter by drug resistance patterns

### Search Results
- Results are paginated (20 items per page by default)
- Each result shows:
  - Strain ID
  - Country and region
  - Associated disease
  - Drug resistance information
  - Gene sequence length

### Data Export
- Select specific strains or export all search results
- Download as CSV for further analysis

## API Documentation

### Authentication
- `POST /api/register` - Register a new user
- `POST /api/login` - User login
- `POST /api/verify` - Verify email
- `POST /api/forgot-password` - Request password reset
- `POST /api/reset-password` - Reset password

### Search API
- `GET /api/search/filters` - Get available search filters and their values
- `POST /api/search/strains` - Search strains with filters and pagination
  ```json
  {
    "query": "search term",
    "filters": {
      "raw_country": ["Country1", "Country2"],
      "host_disease": ["Disease1"]
    },
    "page": 1,
    "pageSize": 20
  }
  ```
- `GET /api/strains/:id` - Get detailed information about a specific strain
- `POST /api/strains/download` - Download selected strains as CSV

## Deployment

### Railway

1. Install the Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login and deploy:
   ```bash
   railway login
   railway link
   railway up
   ```

### Zeabur

1. Push your code to a Git repository
2. Connect the repository to Zeabur
3. Configure environment variables in Zeabur dashboard
4. Deploy the application

## Troubleshooting

- **Database connection issues**:
  - Verify PostgreSQL is running
  - Check credentials in `.env` file
  - Ensure the database and user exist

- **Import script errors**:
  - Ensure the CSV file exists at the correct path
  - Check file permissions
  - Verify CSV format matches expected columns

- **Email not sending**:
  - Verify SMTP settings in `.env`
  - Check spam folder
  - Test with a different email service if needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
