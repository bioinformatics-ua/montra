

ENDPOINT="http://127.0.0.1:8000"
ENDPOINT="http://127.0.0.1:8000"
FINGERPRINT_ID = "6b043b5c0542689e7ab215a14218f16c"
TOKEN="5b16afcdd4e40fda5e11552f97a0dec838b92d15"

curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Country\":\"PT\"}}" $ENDPOINT/api/metadata



curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"5-10\"}}" $ENDPOINT/api/metadata


curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"10-15\"}}" $ENDPOINT/api/metadata



curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Sex\":\"M/F\"}}" $ENDPOINT/api/metadata


curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Outcome\":\"OMS_Score\"}}" $ENDPOINT/api/metadata


curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Final\":\"20000\"}}" $ENDPOINT/api/metadata

