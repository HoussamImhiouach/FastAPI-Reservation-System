from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Client, Room, Reservation



Base.metadata.create_all(bind=engine)

# initialisation
app = FastAPI()

# database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST: client
@app.post("/clients/")
def create_client(name: str, email: str, db: Session = Depends(get_db)):
    new_client = Client(name=name, email=email)
    db.add(new_client)
    db.commit()
    return {"message": "Client created successfully!"}

# POST:room
@app.post("/rooms/")
def create_room(number: str, room_type: str, price: float, db: Session = Depends(get_db)):
    new_room = Room(number=number, type=room_type, price=price)
    db.add(new_room)
    db.commit()
    return {"message": "Room created successfully!"}

# POST: reservation
@app.post("/reservations/")
def create_reservation(client_id: int, room_id: int, date: str, db: Session = Depends(get_db)):
    #client existence
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # room existence
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    new_reservation = Reservation(client_id=client_id, room_id=room_id, date=date)
    db.add(new_reservation)
    db.commit()
    return {"message": "Reservation created successfully!"}

# GET:clients
@app.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

# GET:  rooms
@app.get("/rooms/")
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

# GET: reservations
@app.get("/reservations/")
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()
