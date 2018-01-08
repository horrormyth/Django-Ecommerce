# E-Commerce Application
A simple django based e-commerce application with payment integration (Beta)

## Instruction
- Clone the application
- Create virtualenv 
- Install requirements in the created virtualenv
    `pip install -r requirements.txt`
- Migrate (makemigrations if any tables are missed (create tables))
    - `python manage.py makemigrations`
    - `python manage.py migrate`
- Run the server 
    `pyhton manage.py runserver`