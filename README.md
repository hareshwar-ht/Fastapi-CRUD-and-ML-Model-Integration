# FastAPI Learning Repository

A hands-on learning repository demonstrating FastAPI through practical examples.

## � Projects

### 1. CRUD - Patient Management System

Complete patient records management with RESTful API operations.

**Features:**

- Add, view, update, and delete patient records
- Automatic BMI calculation and health verdict
- Sort patients by various attributes
- JSON-based data storage

**Run:**

```bash
cd CRUD
python main.py
```

### 2. ML Model Integration

Insurance category prediction API with machine learning.

**Features:**

- REST API for ML predictions
- Automatic feature engineering (BMI, age groups, lifestyle risk)
- Streamlit web interface
- Pre-trained model deployment

**Run:**

```bash
cd ml_model_integration
python main.py
```

**Streamlit UI:**

```bash
streamlit run ml_model_integration/frontend_streamlit.py
```

## � Quick Start

1. **Setup**

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # Windows: myenv\Scripts\activate
   pip install fastapi uvicorn pydantic pandas scikit-learn streamlit
   ```

2. **Run** either project (see above)

3. **Access API docs** at `http://localhost:8000/docs`

## 🛠️ Technologies

- FastAPI - Web framework
- Pydantic - Data validation
- Uvicorn - ASGI server
- Pandas & Scikit-learn - ML components
- Streamlit - Web UI

## � Learning Focus

- RESTful API design
- Request/response validation
- CRUD operations
- ML model deployment
- Automatic API documentation

---

**API Documentation:** `/docs` (Swagger UI) | `/redoc` (ReDoc)
