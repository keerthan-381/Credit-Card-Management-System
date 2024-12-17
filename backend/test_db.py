import app
import bcrypt
import pytest

p = app.get_cust(3)
print(p)
def test_fname():
    assert p[0][0] == "seshu"
    
def test_email():
    assert p[0][1] == 'seshu@gmail.com'
    
def test_password():
    stored_password = p[0][2]
    password = '12'

    assert bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
    
q = app.get_test_card(1111111)
print(q)
def test_card_holder():
    assert q[0][0] == "joe"
    
def test_credit_limit():
    assert q[0][1] == 123
    
def test_status():
    assert q[0][2] == "Active"

# r = get_test_transaction(card_number,transaction_id)