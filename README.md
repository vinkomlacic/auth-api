# auth-api
Simple Authentication API made in FastAPI

# Endpoints
 * **[POST]** `/users` - registers a new user
 * **[POST]** `/token` - retrieves an access token provided the credentials
 * **[GET]** `/user/me` - retrieves the current user (protected by authentication)


# Quickstart for local development
1. Setup the virtual environment and install packages from `requirements.txt`
```bash
pip install -r requirements.txt
```
2. Copy `example.env` file and fill it out with correct values
3. Start the postgres database - for your convenience you can use `docker/docker-compose.yml`
```bash
cd docker
docker-compose up -d
```
4. Run migrations (do this only the first time)
```bash
alembic upgrade head
```
5. Run the server
```bash
python -m uvicorn app.main:app --reload
```
