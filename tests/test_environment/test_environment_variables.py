import os

#----- Testea que estén definidas las variables de entorno
def test_environment_variables():
    api_key = os.getenv("API_KEY")
    minio_access_key = os.getenv("MINIO_ACCESS_KEY")
    assert api_key is not None
    assert minio_access_key is not None

