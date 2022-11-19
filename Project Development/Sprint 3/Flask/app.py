from flask import Flask,render_template,request
# Flask-It is our framework which we are going to use to run/serve our application.
#request-for accessing file which was uploaded by the user on our application.
import os
import numpy as np #used for numerical analysis
from tensorflow.keras.models import load_model#to load our trained model
from tensorflow.keras.preprocessing import image
import requests

app = Flask(__name__,template_folder="templates") # initializing a flask app
# Loading the model
model=load_model('nutrition.h5')
print("Loaded model from disk")

@app.route('/')# route to display the home page
def home():
    return render_template('home.html')#rendering the home page

@app.route('/image1',methods=['GET','POST'])# routes to the index html
def image1():
    return render_template("image.html")

@app.route('/predict',methods=['GET', 'POST'])# route to show the predictions in a web UI
def launch():
    if request.method=='POST':
        f=request.files['file'] #requesting the file
        basepath=os.path.dirname('__file__')#storing the file directory
        filepath=os.path.join(basepath,"uploads",f.filename)#storing the file in uploads folder
        f.save(filepath)#saving the file
        
        img=image.load_img(filepath,target_size=(64,64)) #load and reshaping the image
        x=image.img_to_array(img)#converting image to an array
        x=np.expand_dims(x,axis=0)#changing the dimensions of the image

        pred=np.argmax(model.predict(x), axis=1)
        print("prediction",pred)#printing the prediction
        index=['Apple Braeburn','Apple Crimson Snow','Apple Golden','Apple Granny Smith','Apple Pink Lady','Apple Red','Apple Red Delicious','Apple Red Yellow','Apricot','Avocado','Avocado ripe','Banana','Banana Lady Finger','Banana Red','Beetroot','Blueberry','Cactus fruit','Cantaloupe','Carambula','Cauliflower','Cherry','Cherry Rainier','Cherry Wax Black','Cherry Wax Red','Cherry Wax Yellow','Chestnut','Clementine','Cocos','Corn','Corn Husk','Cucumber Ripe','Dates','Eggplant','Fig','Ginger Root','Granadilla','Grape Blue','Grape Pink','Grape White','Grapefruit Pink','Grapefruit White','Guava','Hazelnut','Huckleberry','Kaki','Kiwi','Kohlrabi','Kumquats','Lemon','Lemon Meyer','Limes','Lychee','Mandarine','Mango','Mango Red','Mangostan','Maracuja','Melon Piel de Sapo','Mulberry','Nectarine','Nectarine Flat','Nut Forest','Nut Pecan','Onion Red','Onion Red Peeled', 'Onion White','Orange','Papaya','Passion Fruit','Peach','Peach Flat','Pear','Pear Abate','Pear Forelle','Pear Kaiser','Pear Monster','Pear Red','Pear Stone','Pear Williams','Pepino','Pepper Green','Pepper Orange','Pepper Red','Pepper Yellow','Physalis','Physalis with Husk','Pineapple','Pineapple Mini','Pitahaya Red','Plum','Pomegranate','Pomelo Sweetie','Potato Red', 'Potato Red Washed','Potato Sweet','Potato White','Quince','Rambutan','Raspberry','Redcurrant','Salak','Strawberry','Strawberry Wedge','Tamarillo','Tangelo','Tomato','Tomato Cherry Red','Tomato Heart','Tomato Maroon','Tomato Yellow','Tomato not Ripened','Walnut','Watermelon']
        
        result=str(index[pred[0]])
                    
        x=result
        print(x)
        result=nutrition(result)
        print(result)
        
        return render_template("0.html",showcase=(result),showcase1=(x))
def nutrition(index):
    url = "https://calorieninjas.p.rapidapi.com/v1/nutrition"
    querystring = {"query":index}
    headers = {
        'x-rapidapi-key': "5d797ab107mshe668f26bd044e64p1ffd34jsnf47bfa9a8ee4",
        'x-rapidapi-host': "calorieninjas.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)     
    return response.json()['items']
    
if __name__ == "__main__":
   # running the app
    app.run(debug=False)