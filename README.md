# Mini-Project

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" integrity="sha512-Kc323vGBEqzTmouAECnVceyQqyqdsSiqLQISBL29aUW4U/M7pSPA/gEUZQqv1cwx4OnYxTxve5UMg5GT6L4JJg==" crossorigin="anonymous" referrerpolicy="no-referrer" />


# DrugGenius
 DrugGenius is an intelligent platform that provides personalized drug recommendations using advanced data-driven techniques.

---
<img src="https://github.com/user-attachments/assets/88bb6c65-625a-459c-9410-f40cbc3130cd" alt="description" width="1000px" height="500px">



---
## **Why DrugGenius?**

- Accurate, data-driven recommendations based on symptoms and conditions.
- Personalized suggestions, including allergy and chronic condition considerations.
- Easy-to-use interface with quick and reliable recommendations.

---

## **Features provided for the users**

DrugGenius is an intelligent platform for drug recommendation system. These are few features provided:

### **1. Create an account and login:**
First user can register an account in our website and login so that their data is secured.

<img src="https://github.com/user-attachments/assets/edf157a8-4eb0-4313-b044-73680786fe3f" alt="description" width="500px" height="400px">
<img src="https://github.com/user-attachments/assets/b24d13f0-6bf7-437f-be09-655ea0b7b103" alt="description" width="500px" height="400px">




### **2. Select the Symptoms:**
Once user is logged in he/she can select the symptoms they are currently facing and also provide additional information such as age, blood pressure, temperature.

![Screenshot 2024-11-24 134304](https://github.com/user-attachments/assets/837fcb89-f17b-45e0-8e0b-cd2f13bf3f88)

### **3. Medicine Recommendation:**
After the user enters symptoms and all other details our ai model which is trained with all medicines based on the symptoms it can generate medicines for each symptoms provided by the user and also detect whether the user is suffering from any disease.

![Screenshot 2024-11-24 135705](https://github.com/user-attachments/assets/f80bda89-aa61-4a69-8469-8315e866b713)

### **4. ChatBot:**
We have personalized AI chatBot named "MedBot" , if a user has to checck whether the medicine recommended is genuine or not they can ask our MedBot regarding the medicine uses and side effects.

![image](https://github.com/user-attachments/assets/ec819c66-6c0f-4e16-a8fc-0a9bf4591961)

![image](https://github.com/user-attachments/assets/c3d12845-8061-4bdc-8249-f7877737ca92)

---

## **Getting started**

### **1. Clone the Repository**

To start with the project, first clone the repository to your local machine
![image](https://github.com/user-attachments/assets/3353c306-bf50-4fb2-bccf-0f3d7aa6117d)

copy the https link to your vs code   OR try the terminal 

    
    
```bash
git clone <repository-URL>
git clone https://github.com/Shankar-hacker/DrugGenius.git
```

### **2. Install Packages/ Dependencies**

Install the project packages using pip to run the flask app:

```bash
pip install <package-name>
pip install  flask  render_template request jsonify redirect url_for  session flash flask_mysqldb  MySQL subprocess  pymysql bcrypt

```
You can also install each and every package individually
 ```bash
pip install gunicorn
pip install flask
pip install render_template
pip install flash
pip install flask_mysqldb
pip install MySQL
pip install pymysql
pip install bcrypt
```

You can also run requirements.txt instead of installing individually

1. Basic pip install:
```bash
pip install -r requirements.txt
```

2. If you want to upgrade existing packages:
```bash
pip install --upgrade -r requirements.txt
```

3. For a specific Python environment (recommended):

-Activate your virtual environment first
```bash
python -m pip install -r requirements.txt
```
---
### **3. Database creation**

To store the login /registration information you have to create a database in phpMyAdmin
- Go to http://localhost/phpmyadmin/

  ---
1. Create a database and use:

sql script
```bash
CREATE DATABASE LoginPage;
USE LoginPage;
```
2. Create a table :

sql script
```bash
CREATE TABLE Users (
    ID INT AUTO_INCREMENT PRIMARY KEY,       -- Unique identifier for each user
    Username VARCHAR(50) NOT NULL UNIQUE,        -- Username (must be unique)
    Email VARCHAR(100) NOT NULL UNIQUE,          -- User's email (must be unique)
    Password VARCHAR(255) NOT NULL,          -- Password (stored as a hash for security)
);
```
![image](https://github.com/user-attachments/assets/46343b64-9f89-4fa7-b174-91c246713b6d)


---

### **4. Run The flask app**

Run the flask app in your local server:

```bash
python app.py
```
![Screenshot 2024-12-01 124932](https://github.com/user-attachments/assets/e5faeed9-141f-471f-8e2f-b696b9a37360)

This will open the Website on the local server at `http://127.0.0.1:5000/` (or the specified port).

---

## **Contributing**

We welcome contributions! Here's how you can get started:

1. Fork this repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request to the main repository.

---

## **License**

This project is licensed under the **Apache License**. See the [LICENSE](LICENSE) file for more details.

---

## **Contact**

For any questions, suggestions, or feedback, please contact us at **pvishalkumar544@gmail.com**.
 
---
