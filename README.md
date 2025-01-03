# Boodschappen App

A full-stack application for managing grocery shopping lists with advanced features like price tracking and store comparisons.

## Project Structure

### Backend (`/app`)
```
app/
├── main.py
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
├── api/
│   └── v1/
│       └── endpoints/
│           ├── auth.py
│           ├── products.py
│           ├── stores.py
│           └── shopping_lists.py
├── services/
│   ├── advanced_analytics.py
│   ├── store_integrations.py
│   ├── list_sharing_service.py
│   ├── email_service.py
│   └── scraper_service.py
└── models/
    ├── user.py
    ├── product.py
    └── shopping_list.py
```

### Frontend (`/src`)
```
src/
├── components/
│   ├── layout/
│   │   └── Navbar.tsx
│   ├── shopping/
│   │   ├── ShareListModal.tsx
│   │   └── ShoppingListCard.tsx
│   └── charts/
│       ├── PriceTrendChart.tsx
│       └── StoreHeatmap.tsx
├── services/
│   ├── api.ts
│   ├── shareService.ts
│   └── pushNotificationService.ts
└── pages/
    └── app/
        └── layout.tsx
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/boodschappen-app.git
cd boodschappen-app
```

2. Install backend dependencies:
```bash
cd app
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ../src
npm install
```

4. Start the development environment:
```bash
docker-compose up
```

## Development

- Backend API runs on: http://localhost:8000
- Frontend dev server runs on: http://localhost:3000
- API documentation available at: http://localhost:8000/docs

## Production Deployment

Use the production Docker Compose file:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Features

- User authentication and authorization
- Shopping list management
- Store price comparisons
- Price trend analysis
- List sharing capabilities
- Push notifications
- Store integration services
- Advanced analytics

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details