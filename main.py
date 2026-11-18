
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()



class Item(BaseModel):
    text: str
    is_done: bool = False


class ItemUpdate(BaseModel):
    text: str | None = None
    is_done: bool | None = None


# Lista de objetos
items: list[Item] = [
    Item(text="apple", is_done=False),
    Item(text="banana", is_done=True),
    Item(text="orange", is_done=False),
    Item(text="pear", is_done=True),
    Item(text="pineapple", is_done=True),
    Item(text="pencil", is_done=False),
    Item(text="sheet", is_done=False),
    Item(text="ruler", is_done=False),
    Item(text="compass", is_done=True),
    Item(text="scissor", is_done=True),
]


@app.get("/")
def root():
    return {"Hello": "World"}


# CREATE
@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    items.append(item)
    return item


# READ ALL
@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    if limit < 0:
        raise HTTPException(
            status_code=400,
            detail="Limit cannot be negative"
        )

    return items[:limit]


# READ ONE
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if not 0 <= item_id < len(items):
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )

    return items[item_id]


# UPDATE
@app.patch("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    if not 0 <= item_id < len(items):
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )

    stored_item = items[item_id]

    update_data = item.model_dump(exclude_unset=True)

    # Validar los datos antes de guardar
    updated_item = Item.model_validate({
        **stored_item.model_dump(),
        **update_data
    })

    items[item_id] = updated_item

    return updated_item


# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if not 0 <= item_id < len(items):
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )

    deleted_item = items.pop(item_id)

    return {
        "message": "Item deleted successfully",
        "deleted_item": deleted_item
    }
