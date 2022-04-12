from email.policy import HTTP
from fastapi import FastAPI, HTTPException, status
from mongita import MongitaClientDisk
from pydantic import BaseModel


class Shape(BaseModel):
	item_name: str
	no_of_sides: int
	id: int


app = FastAPI()

client = MongitaClientDisk()
db = client.db
shapes = db.shapes

@app.get("/")
def root():
	return {"message": "root"}

@app.get("/shapes")
def get_shapes() -> None:
	existing_shapes = shapes.find({})
	return [
		{key:shape[key] for key in shape if key != "_id"}
		for shape in existing_shapes
	]

@app.get("/shapes/{shape_id}")
def get_shape_by_id(shape_id: int) -> dict:
	if shapes.count_documents({"id": shape_id}) > 0:
		shape = shapes.find_one({"id": shape_id})
		return {key:shape[key] for key in shape if key != "_id"}
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no shape with id {shape_id}")

@app.post("/shapes")
def add_shape(shape: Shape):
	shapes.insert_one(shape.dict())
	return shape

@app.put("/shapes/{shape_id}")
def update_shape(shape_id: int, shape: Shape):
	if shapes.count_documents({"id": shape_id}) > 0:
		shapes.replace_one({"id": shape_id}, shape.dict())
		return shape
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"shape with id {shape_id} not found")

@app.delete("/shapes/{shape_id}")
def delete_shape(shape_id: int):
	# if shapes.count_documents({"id": shape_id}):
	# 	shapes.delete_one({"id": shape_id})
	# 	return {"message": f"shape {shape_id} delete"}
	deleted = shapes.delete_one({"id": shape_id})
	if deleted.deleted_count == 0:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"shape with id {shape_id} not found")
	return {"msg": f"shape with id {shape_id} deleted"}
	