from fastapi import FastAPI
from app.celery_worker import create_order
from app.model import Order
import sys
import uvicorn
from app.config import settings

# Create FastAPI app
app = FastAPI()


# Create order endpoint
@app.post('/order')
def add_order(order: Order):
    # use delay() method to call the celery task
    create_order.delay(order.customer_name, order.order_quantity)
    return {"message": "Order Received! Thank you for your patience."}


if __name__ == "__main__":
    if (len(sys.argv) == 2) and (sys.argv[1] == "openapi"):
        from fastapi.openapi.utils import get_openapi

        with open("openapi.json", "w") as f:
            json.dump(
                get_openapi(
                    title=app.title,
                    version=app.version,
                    openapi_version=app.openapi_version,
                    description=app.description,
                    routes=app.routes,
                ),
                f,
            )

    else:
        uvicorn.run(
            "main:app",
            host="localhost",
            reload=settings.DEBUG_MODE,
            port=settings.PORT,
        )
