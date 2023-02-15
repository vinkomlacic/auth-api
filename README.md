# auth-api
Simple Authentication API made in FastAPI


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
4. Run the server
```bash
python -m uvicorn app.main:app --reload
```
