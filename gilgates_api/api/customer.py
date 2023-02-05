from typing import Optional
from fastapi import Depends, APIRouter
from sqlmodel import Session
from pydantic import BaseModel
from gilgates_api.deps import current_user, get_session
from gilgates_api.model import User, Customer, Address
from gilgates_api import dao_factory
from geopy.geocoders import Nominatim

router = APIRouter()


class CustomerIn(BaseModel):
    name: str
    phone: str
    lat: Optional[float]
    lng: Optional[float]


@router.post("/", response_model=Customer)
async def create_customer(
    data: CustomerIn,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    dao = dao_factory(session)

    if data.lat and data.lng:
        geolocator = Nominatim()
        location = geolocator.reverse(str(data.lat) + "," + str(data.lng))
        address = location.raw["address"]
        city = address.get("city", "")
        state = address.get("state", "")
        addr = Address(lat=data.lat, lng=data.lng, city=city, state=state)

    customer = Customer(
        employee=user,
        name=data.name,
        phone=data.phone,
        address=addr
    )

    return customer
