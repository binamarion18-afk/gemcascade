### Chooza - Kenyan Youth Platform (MVP)

- Mobile-first Flask PWA with rooms, gigs, matching, and M-Pesa sandbox stub.

#### Quick start

```bash
# System Python install (no venv in this environment)
pip3 install -r requirements.txt
export FLASK_ENV=development
python3 -c "from app import create_app; from app.extensions import db; app=create_app(); app.app_context().push(); db.create_all()"
python3 -m app.main
```

The app runs on `http://localhost:8000`.

#### API (examples)
- POST `/api/auth/register` { email, password, name }
- POST `/api/auth/login` { email, password }
- GET `/api/users/profile`
- POST `/api/users/profile` { bio, county, goals }
- GET `/api/users/match`
- GET `/api/rooms`
- POST `/api/rooms/create` { title, category, is_paid, price_kes }
- POST `/api/rooms/join` { room_id }
- POST `/api/rooms/tip` { room_id, amount }
- GET `/api/gigs`
- POST `/api/gigs/create` { title, description, budget_kes }
- POST `/api/gigs/apply` { gig_id, pitch }
- POST `/api/payments/mpesa/request` { msisdn, amount }

#### Deployment
- Heroku: use `Procfile` and `runtime.txt`
- Docker: `docker-compose up --build`
