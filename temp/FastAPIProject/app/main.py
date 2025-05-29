from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import logging
from PIL import Image
import tempfile
from app.processing.background_remover import BackgroundRemover
from app.processing.transparency_handler import TransparencyHandler
from app.processing.lighting_adjuster import LightingAdjuster
from app.processing.environment_integrator import EnvironmentIntegrator

app = FastAPI(title="Car Image Processing API")

background_remover = BackgroundRemover()
transparency_handler = TransparencyHandler()
lighting_adjuster = LightingAdjuster()
environment_integrator = EnvironmentIntegrator()

TEMP_DIR = tempfile.gettempdir()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/remove-background")
async def remove_background_endpoint(file: UploadFile = File(...)):
    try:
        temp_input_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.jpg")
        temp_output_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.png")

        with open(temp_input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        car_without_bg = background_remover.remove_background(temp_input_path)

        car_refined = background_remover.refine_edges(car_without_bg)

        car_refined.save(temp_output_path, format="PNG")

        return FileResponse(
            temp_output_path,
            media_type="image/png",
            headers={"X-Process-Status": "background-removed"}
        )
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)

@app.post("/process-car-image")
async def process_car_image(
        car_image: UploadFile = File(...),
        background_image: UploadFile = File(...),
        position_x: float = Form(0.5),
        position_y: float = Form(0.8),
        scale: float = Form(0.7)
):
    try:
        car_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.jpg")
        bg_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.jpg")
        output_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.png")

        with open(car_path, "wb") as buffer:
            shutil.copyfileobj(car_image.file, buffer)

        with open(bg_path, "wb") as buffer:
            shutil.copyfileobj(background_image.file, buffer)

        logger.info("Step 1: Removing background")
        car_without_bg = background_remover.remove_background(car_path)

        logger.info("Step 2: Handling transparency")
        car_with_transparency = transparency_handler.detect_windows(car_without_bg)

        logger.info("Step 3: Analyzing background lighting")
        bg_image = Image.open(bg_path)
        light_map, light_direction = lighting_adjuster.estimate_lighting(bg_image)

        logger.info("Step 4: Applying lighting to car")
        car_lit = lighting_adjuster.apply_lighting(car_with_transparency, light_map)

        logger.info("Step 5: Placing car in background")
        composite = environment_integrator.place_car(
            car_lit, bg_image, position=(position_x, position_y), scale=scale
        )

        logger.info("Step 6: Adding shadow")
        final_image = environment_integrator.add_shadow(composite, light_direction)

        final_image.save(output_path, format="PNG")

        return FileResponse(
            output_path,
            media_type="image/png",
            headers={"X-Process-Status": "complete"}
        )
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        for path in [car_path, bg_path]:
            if os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
