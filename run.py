from app import created_app

app = created_app()

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
