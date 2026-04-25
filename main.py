from fastapi import FastAPI
import pandas as pd
import os

App = FastAPI()

@App.get("/")
async def saludo():
    return "welcome to my  login system"

@App.post("/createUser")
async def save_new_user(name : str, password : str, email : str, filename : str="users.csv"):
    """
    Saves a new user to a text file.
    
    Args:
        name (str): User's name
        password (str): User's password
        email (str): User's email
        filename (str): File to save user data (default: "users.txt")
    
    Returns:
        bool: True if successful, False if user already exists
    """
    try:
        # Check if user already exists
        try:
            with open(filename, 'r') as file:
                for line in file:
                    if line.startswith(f"{name},"):
                        return False  # User already exists
        except FileNotFoundError:
            pass  # File doesn't exist yet, that's fine
        
        # Save the new user
        with open(filename, 'a') as file:
            file.write(f"{name},{password},{email}\n")
        return True
    
    except Exception:
        return False  # Error occurred

@App.get("/userAll")
async def userAll( ):
    pass

@App.get("/validateIncome")
async def validateIncome(userEmail , UserPass):
    pass

    



