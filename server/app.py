from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import tempfile, os
from main import migrate_playlist  # your playlist logic

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
    return {"message": "Server is working!"}

@app.post("/upload")
async def upload_file(playlist: UploadFile = File(...)):
    print("📥 Received upload:", playlist.filename)
    try:
        suffix = os.path.splitext(playlist.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await playlist.read()
            tmp.write(content)
            tmp_path = tmp.name

        playlist_name = os.path.splitext(os.path.basename(tmp_path))[0]
        migrate_playlist(tmp_path, playlist_name)
        os.remove(tmp_path)

        return {"message": "Playlist synced successfully!"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
