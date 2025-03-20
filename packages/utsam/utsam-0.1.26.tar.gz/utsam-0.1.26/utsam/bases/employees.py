from typing import Optional
from pydantic import BaseModel


class Employee(BaseModel):
    employee_id: Optional[str] = None
    employee_first_name: str
    employee_last_name: str
    staff_id: int