## Melanoma Detection Tool : REST APIs

#### Technologies & Libraries Used
    Python 3.9
    Flask framework 
    scikit-learn==1.0
    numpy
    pandas
    gunicorn
    flask_cors
    opencv-python-headless==4.5.5.64
    
### How to set up and run
##### Create virtual environment 
###### Windows 
    py -3 -m venv <name of environment>
###### Linux/MaxOS
    python3 -m venv <name of environment>
##### Activate virtual environment 
###### Windows 
    <name of environment>\Scripts\activate
###### Linux/MaxOS
    . <name of environment>/bin/activate
##### Install required libraries
    pip3 install -r requirements.txt
##### Run app locally
    flask run

#### Special Notes
* Use Python 3.9 and scikit-learn==1.0
* If any new library requires to install, after install freeze it to the requirements.txt
* add your virtual environment directory to .gitignore 

### Rest Api Documentation
#### Melanoma detection using PPS
   Method: POST <br/>
   End point: https://melanoma-detection-tool-api.herokuapp.com/predict-melanoma/pps <br/>
   Request body format: JSON <br/>
   Required params in request body: age, gene, tumor, tier, mutated dna <br/><br/>
   Example request body <br/>
   
       { 
            "age" : 45, 
            "gene" : "BRAF",
            "tumor" : "metastasis",
            "tier" : 1,
            "mutated dna" : "ATGGCGGCGCTGAGCGGTGGCGGTGGTGGCGGCGCGGAGCCGGGCCAGGCTCTGTTCAACGGGGACATGGAGCCCGAGGCCGGCGCCGGCGCCGGCGCCGCGGCCTCTTCGGCTGCGGACCCTGCCATTCCGGAGGAGGTGTGGAATATCAAACAAATGATTAAGTTGACACAGGAACATATAGAGGCCCTATTGGACAAATTTGGTGGGGAGCATAATCCACCATCAATATATCTGGAGGCCTATGAAGAATACACCAGCAAGCTAGATGCACTCCAACAAAGAGAACAACAGTTATTGGAATCTCTGGGGAACGGAACTGATTTTTCTGTTTCTAGCTCTGCATCAATGGATACCGTTACATCTTCTTCCTCTTCTAGCCTTTCAGTGCTACCTTCATCTCTTTCAGTTTTTCAAAATCCCACAGATGTGGCACGGAGCAACCCCAAGTCACCACAAAAACCTATCGTTAGAGTCTTCCTGCCCAACAAACAGAGGACAGTGGTACCTGCAAGGTGTGGAGTTACAGTCCAAGACAGTCTAAAGAAAGCACTGATGATGAGAGGTCTAATCCCAGAGTGCTGTGCTGTTTACAGAATTCAGGATGGAGAGAAGAAACCAATTGGTTGGGACACTGATATTTCCTGGCTTACTGGAGAAGAATTGCATGTGGAAGTGTTGGAGAATGTTCCACTTACAACACACAACTTTGTACGAAAAACGTTTTTCACCTTAGCATTTTGTGACTTTTGTCGAAAGCTGCTTTTCCAGGGTTTCCGCTGTCAAACATGTGGTTATAAATTTCACCAGCGTTGTAGTACAGAAGTTCCACTGATGTGTGTTAATTATGACCAACTTGATTTGCTGTTTGTCTCCAAGTTCTTTGAACACCACCCAATACCACAGGAAGAGGCGTCCTTAGCAGAGACTGCCCTAACATCTGGATCATCCCCTTCCGCACCCGCCTCGGACTCTATTGGGCCCCAAATTCTCACCAGTCCGTCTCCTTCAAAATCCATTCCAATTCCACAGCCCTTCCGACCAGCAGATGAAGATCATCGAAATCAATTTGGGCAACGAGACCGATCCTCATCAGCTCCCAATGTGCATATAAACACAATAGAACCTGTCAATATTGATGACTTGATTAGAGACCAAGGATTTCGTGGTGATGGAGGATCAACCACAGGTTTGTCTGCTACCCCCCCTGCCTCATTACCTGGCTCACTAACTAACGTGAAAGCCTTACAGAAATCTCCAGGACCTCAGCGAGAAAGGAAGTCATCTTCATCCTCAGAAGACAGGAATCGAATGAAAACACTTGGTAGACGGGACTCGAGTGATGATTGGGAGATTCCTGATGGGCAGATTACAGTGGGACAAAGAATTGGATCTGGATCATTTGGAACAGTCTACAAGGGAAAGTGGCATGGTGATGTGGCAGTGAAAATGTTGAATGTGACAGCACCTACACCTCAGCAGTTACAAGCCTTCAAAAATGAAGTAGGAGTACTCAGGAAAACACGACATGTGAATATCCTACTCTTCATGGGCTATTCCACAAAGCCACAACTGGCTATTGTTACCCAGTGGTGTGAGGGCTCCAGCTTGTATCACCATCTCCATATCATTGAGACCAAATTTGAGATGATCAAACTTATAGATATTGCACGACAGACTGCACAGGGCATGGATTACTTACACGCCAAGTCAATCATCCACAGAGACCTCAAGAGTAATAATATATTTCTTCATGAAGACCTCACAGTAAAAATAGGTGATTTTGGTCTAGCTACAGTGAAATCTCGATGGAGTGGGTCCCATCAGTTTGAACAGTTGTCTGGATCCATTTTGTGGATGGCACCAGAAGTCATCAGAATGCAAGATAAAAATCCATACAGCTTTCAGTCAGATGTATATGCATTTGGAATTGTTCTGTATGAATTGATGACTGGACAGTTACCTTATTCAAACATCAACAACAGGGACCAGATAATTTTTATGGTGGGACGAGGATACCTGTCTCCAGATCTCAGTAAGGTACGGAGTAACTGTCCAAAAGCCATGAAGAGATTAATGGCAGAGTGCCTCAAAAAGAAAAGAGATGAGAGACCACTCTTTCCCCAAATTCTCGCCTCTATTGAGCTGCTGGCCCGCTCATTGCCAAAAATTCACCGCAGTGCATCAGAACCCTCCTTGAATCGGGCTGGTTTCCAAACAGAGGATTTTAGTCTATATGCTTGTGCTTCTCCAAAAACACCCATCCAGGCAGGGGGATATGGTGCGTTTCCTGTCCACTGA"
       }
       
   Example response body<br/>
       
       Status Code: OK (200)
       
       {
            "age": 45,
            "gene": "BRAF",
            "pps": [0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,1,0],
            "probability": [
                0.06745256458525928,
                0.9325474354147407
            ],
            "tier": 1,
            "tumor": "metastasis"
       }
       
   
   #### pps - protein primary structure 
        The pps attribute contains the changes of amino-acid sequence with order of 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y' respectively
   
   #### probability 
        array location 0 - confidence level for not having melanoma
        array location 1 - confidence level for having melanoma
       
   Response Status <br/>
   200: Request Processed Successfully. <br/>
   400: Bad Request <br/>
   500: Internal Server Error
   

#### Melanoma detection using Dermoscopic Image
   Method: POST <br/>
   End point: https://melanoma-detection-tool-api.herokuapp.com/predict-melanoma/dermoscopic-images <br/>
   Request body format: Form-data <br/>
   Required params in request body: image (Needs to be passed as a file)<br/><br/>
   Example request body <br/>
   
       { 
        	"image" : ISIC_0024554.jpg
   	   }
       
   Example response body<br/>
       
       Status Code: OK (200)
       
       [
            "Positive",
            90.53,
            [ 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0 ]
       ]
       
   
   #### array values description 
        array location 0 - Presence of Dermoscopi Feature Asymmetry
        array location 1 - Presence of Dermoscopi Feature Border Irregularity
        array location 2 - Presence of Dermoscopi Feature Colour Variation
        array location 3 - Presence of Dermoscopi Feature Diameter
        array location 4 - Presence of Dermoscopi Feature Globules
        array location 5 - Presence of Dermoscopi Feature Blotches
        array location 6 - Presence of Dermoscopi Feature Milky-red Areas
        array location 7 - Presence of Dermoscopi Feature Rosettes
        array location 8 - Presence of Dermoscopi Feature Regression Structure
        array location 9 - Presence of Dermoscopi Feature Blue-white Veil
        array location 10 - Presence of Dermoscopi Feature Atypical Network
        array location 11 - Presence of Dermoscopi Feature Irregular Streaks
        
   Response Status <br/>
   200: Request Processed Successfully. <br/>
   400: Bad Request <br/>
   500: Internal Server Error
 
