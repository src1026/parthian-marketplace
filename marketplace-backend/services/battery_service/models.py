from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, Field, condecimal
from typing import Optional
from decimal import Decimal

class Battery(BaseModel):
    batteryId: str = Field(..., description="Battery unique ID")
    capacity: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Capacity in kWh")
    voltage: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Voltage in V")
    state_of_health: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Remaining battery life (%)")
    cycle_count: int = Field(..., description="Number of charge cycles")
    chemistry_type: str = Field(..., description="Battery chemistry type (NMC, LFP, etc.)")
    weight: Optional[condecimal(max_digits=10, decimal_places=2)] = Field(None, description="Weight in kg")
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = Field(None, description="Price in USD")
    location: Optional[str] = Field(None, description="Seller location")
