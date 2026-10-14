from pydantic import BaseModel, Field

class GenerateDataRequest(BaseModel):
    """
    Request model for generating data.
    """
    count: int = Field(gt=0, le=1000, description="The number of data items to generate.")
    scenario: str = Field('valid', description="The scenario for which to generate data.")