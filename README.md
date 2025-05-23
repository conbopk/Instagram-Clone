# Instagram Clone API
### Backend API cho Instagram clone project.

## Getting Start
### **1. Clone this repository:**
```shell
git clone https://github.com/conbopk/Instagram-clone.git
cd Instagram-clone
```
### **2. Create and active virtual environment:**
```shell
python -m venv .venv
source .venv/bin/activate #Linux/Mac
# Or
.venv\Scripts\activate  #Windows
```
### **3. Install dependencies:**
```shell
pip install -r requirements.txt
```
### **4. Environmental variable settings:**
```shell
export SECRET_KEY="your_secret_key" #Linux/Mac
# Or
set SECRET_KEY=your_secret_key #Windows
```
### **5. Run app:**
```shell
python run.py
```
## API Endpoints
### Authentication
- **POST /api/auth/register**: New user registration
- **POST /api/auth/login**: Log in user
- **GET /api/auth/me**: Get current user information
- **POST /api/auth/logout**: Log out of user

### User
- **GET /api/users/profile**: get information from users logged in 
- **PUT /api/users/profile**: Update information profile 
- **POST /api/users/\<int:user_id>/profile**: View other user's profile
- **POST /api/users/\<int:user_id>/follow**: Follow users
- **DELETE /api/users/\<int:user_id>/unfollow**: Unfollow users
- **GET /api/users/<user_id>/followers**: List of followers
- **GET /api/users/<user_id>/following**: The list of following
- **GET /api/users/search?q=query**: search user

### Post
- **POST /api/posts/**: Create new post 
- **GET /api/posts/<post_id>**: Get the post detail
- **DELETE /api/posts/<post_id>**: Remove posts 
- **GET /api/posts/users/\<int:user_id>**: view user posts 
- **POST /api/posts/<post_id>/like**: Like posts
- **DELETE /api/posts/<post_id>/unlike**: Unlike posts
- **GET /api/posts/likes**: List of users who liked the posts
- **GET /api/posts/feed**: View news feed

## Authentication
To make the requirements that need authentication, you need to add the JWT token to get from the endpoint login to the Header Authentication with the "Bearer" prefix:
```shell
Authentication: Bearer <token>
```

**This application uses Flask-JWT-Extended to handle JWT (JSON Web Token).**

## Note:
**Project vẫn đang trong giai đoạn phát triển, sẽ sớm có update các module/api còn lại!**