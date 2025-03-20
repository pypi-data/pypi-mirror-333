# **Personal Data Validator**  

## **Overview**  
Personal Data Validator is a Python package designed to efficiently validate various types of personal data, including:  
- **Email addresses**  
- **Phone numbers**  
- **Dates**  
- **URLs**  

This package follows **Object-Oriented Programming (OOP)** principles, ensuring modularity, reusability, and easy integration into different projects.  

---

## **Installation**  
Install the package using:  
```bash
pip install datavalidator
```

---

## **Usage**  

### **1️⃣ Import the Validator Class**  
```python
from datavalidator.validator import DataValidator
```

### **2️⃣ Validate an Email**  
```python
data = "example@email.com"
validator = DataValidator(data)
print(validator.validate_email())  # Output: True
```

### **3️⃣ Validate a Phone Number**  
```python
data = "+1-800-555-1234"
validator = DataValidator(data)
print(validator.validate_phone())  # Output: True
```

### **4️⃣ Validate a Date**  
```python
data = "2024-03-14"
validator = DataValidator(data)
print(validator.validate_date())  # Output: True
```

### **5️⃣ Validate a URL**  
```python
data = "https://example.com"
validator = DataValidator(data)
print(validator.validate_url())  # Output: True
```

---

## **Running Tests**  
The package includes unit tests to ensure proper functionality. Run tests using:  
```bash
pytest tests/
```

---

## **Contributing**  
Contributions are welcome! To contribute:  
1. **Fork** the repository  
2. **Create** a feature branch:  
   ```bash
   git checkout -b feature-branch
   ```  
3. **Commit** your changes:  
   ```bash
   git commit -m "Added new feature"
   ```  
4. **Push** to the branch:  
   ```bash
   git push origin feature-branch
   ```  
5. **Open a Pull Request**  

---

## **License**  
This project is licensed under the **MIT License**.  

---

## **Author**  
👤 **Oluwakorede Oyewole**  
📧 Email: damisonoyewole@gmail.com  

---



