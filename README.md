# GeoPlanner — Backend

Django backend for GeoPlanner, a route planning and optimization application.

## What it does

GeoPlanner allows users to manage their own set of locations and solve logistics problems:

- **Geocoding** — batch import of addresses, automatic coordinate lookup via OpenStreetMap (Nominatim)
- **TSP** (Travelling Salesman Problem) — finds the shortest route visiting all selected points
- **VRP** (Vehicle Routing Problem) — assigns jobs to a fleet of vehicles, optimizing total travel cost

Each user has their own private data: depots, jobs, vehicles, and saved routes.

## Database model

![Database model](docs/DB_Model.jpg)

### Tables

| Table | Description |
|---|---|
| `Depot` | Starting point (e.g. company warehouse) |
| `Job` | Delivery point / order, reusable across routes |
| `Vehicle` | Fleet vehicle with capacity and working time |
| `Route` | Solved TSP or VRP result |
| `RouteStop` | Ordered stops within a route, with optional vehicle assignment |
| `RouteType` | Dictionary: TSP, VRP |
| `VehicleType` | Dictionary: Van, Truck, Bike, ... |
| `RouteStatus` | Dictionary: Draft, Active, Archived |

## Tech stack

- Python 3.13
- Django 5.x
- PostgreSQL
- Leaflet + OpenStreetMap (maps & geocoding)
- Frontend: Django templates (React planned)

## Setup

```bash
# Clone and enter the project
git clone https://github.com/geo-planner/BackEnd.git
cd BackEnd

# Create and activate virtual environment
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

## Project structure

```
BackEnd/
├── BackEnd/          # Project configuration (settings, urls)
├── geoplanner/       # Main application
│   ├── models.py     # Database models
│   ├── views.py      # Views
│   ├── urls.py       # URL routing
│   ├── admin.py      # Admin panel configuration
│   └── templates/    # HTML templates
├── docs/
│   └── DB_Model.jpg  # Database diagram
├── requirements.txt
└── manage.py
```
