SERVER=https://dataverse.iit.it
PERSISTENT_ID=doi:10.48557/YK6RZZ
VERSION=:latest
TOKEN=

# Download the json file
curl -H X-Dataverse-key:$TOKEN $SERVER/api/datasets/:persistentId/versions/$VERSION/files?persistentId=$PERSISTENT_ID > dataset.json

# Download all files in the dataset
NUM_FILES=`cat dataset.json | jq ".data | length - 1"`
for i in $(seq 0 $NUM_FILES); do
    file_id=`cat dataset.json | jq ".data[$i].dataFile.id"`
    file_name=`cat dataset.json | jq ".data[$i].dataFile.filename" | tr -d '"'`
    curl -L -H X-Dataverse-key:$TOKEN $SERVER/api/access/datafile/$file_id -o $file_name
done

# Unzip all objects
for object_name in 003_cracker_box 004_sugar_box 005_tomato_soup_can 006_mustard_bottle 009_gelatin_box 010_potted_meat_can; do
    zip -F ${object_name}.zip --out ${object_name}_all.zip
    unzip ${object_name}_all.zip
done

# Remove temporary files
rm *.z0*
rm *.zip
