SERVER=https://dataverse.iit.it
PERSISTENT_ID=doi:10.48557/G2QJDM
VERSION=:latest

# Download the json file
curl $SERVER/api/datasets/:persistentId/versions/$VERSION/files?persistentId=$PERSISTENT_ID > dataset.json

# Download all files in the dataset
NUM_FILES=`cat dataset.json | jq ".data | length - 1"`
for i in $(seq 0 $NUM_FILES); do
    echo "Downloading file $i/$NUM_FILES..."
    file_id=`cat dataset.json | jq ".data[$i].dataFile.id"`
    file_name=`cat dataset.json | jq ".data[$i].dataFile.filename" | tr -d '"'`
    curl -L $SERVER/api/access/datafile/$file_id -o $file_name
done

# Unzip all objects
for object_name in 003_cracker_box 004_sugar_box 005_tomato_soup_can 006_mustard_bottle 009_gelatin_box 010_potted_meat_can 003_cracker_box_real 006_mustard_bottle_real; do
    echo "Unzipping file ${object_name}.zip..."
    zip -qq -F ${object_name}.zip --out tmp.zip
    rm ${object_name}.z*
    unzip -qq tmp.zip
    rm tmp.zip
done
