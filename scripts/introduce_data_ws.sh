# Script example to test the API 

# Config data 
ENDPOINT="http://bioinformatics.ua.pt/emif/"
FINGERPRINT_ID="6b043b5c0542689e7ab215a14218f16c"
TOKEN="5b16afcdd4e40fda5e11552f97a0dec838b92d15"


# Demographics 
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Country\":\"Portugal\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"5-10\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"10-15\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"15-20\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"20-25\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"25-30\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"30-35\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Sex\":\"M/F\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Population+Diseases\":\"Cardiac\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Population+Diseases\":\"myocardiopathy\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Population+Diseases+Pediatrics\":\"Cardiac\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Outcome\":\"OMS_Score\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Final\":\"20000\"}}" $ENDPOINT/api/metadata

# Others 
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Demographics+Age\":\"5-10\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Demographics+Age\":\"10-15\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Demographics+Age\":\"15-20\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Demographics+Age\":\"20-25\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Demographics+Age\":\"25-30\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Demographics+Age\":\"30-35\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Demographics+Sex\":\"M/F\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Population+Diseases\":\"Cardiac\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Population+Diseases\":\"myocardiopathy\"}}" $ENDPOINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Other+Data+Population+Diseases+Pediatrics\":\"Cardiac\"}}" $ENDPOINT/api/metadata