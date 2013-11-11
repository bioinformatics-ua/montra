
END_POINT="http://bioinformatics.ua.pt/emif-dev"
FINGERPRINT_ID="9ec67af76878230d46951443d0e3c8d2"
TOKEN="270a6979313c1597c1f49eddd887da6633a12402"

curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Sex\":\" Male and Female \" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Age\":\"12-14\" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Demographics+Country\":\" Portugal \" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Outcome\":\"Progression\" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Outcome\":\"Death\" }}" $END_POINT/api/metadata
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token $TOKEN" -d "{\"fingerprintID\":\"$FINGERPRINT_ID\",\"values\":{\"Clinical+Data+Outcome\":\"OMS_Score\" }}" $END_POINT/api/metadata
