# ✅ Lumix Blender Pipeline - Checklist

## Initial Setup
- [ ] Create `services/lumix-blender/`
- [ ] Add `docker-compose.yml`
- [ ] Create `workspace/` folder with subfolder `output/`

## Python Script
- [ ] Write `main.py` with CLI args parsing
- [ ] Create `utils.py` for:
  - [ ] scene setup
  - [ ] camera setup
  - [ ] light setup
  - [ ] neutral background setup
  - [ ] loading transparent image
  - [ ] positioning image on plane
  - [ ] adding shadow catcher

## Docker Compose
- [ ] Configure `docker-compose.yml` to use `blender -b -P ...`
- [ ] Verify volume mounting and working directory

## Testing
- [ ] Run `docker-compose up`
- [ ] Verify output in `workspace/output/final.png`
- [ ] Adjust light or camera position if necessary
