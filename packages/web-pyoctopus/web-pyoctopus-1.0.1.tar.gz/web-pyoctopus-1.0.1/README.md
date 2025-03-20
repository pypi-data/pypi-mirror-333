# Web-PyOctopus: A Lightweight Python Web Framework

![Purpose](https://img.shields.io/badge/purpose-learning-green.svg)
![PyPI](https://img.shields.io/pypi/v/web-pyoctopus.svg)

**Web-PyOctopus** is a lightweight and easy-to-use Python web framework built for learning purposes. It is a **WSGI framework**, meaning it can be used with any WSGI application server such as **Gunicorn**.

### 🔗 [View on PyPI](https://pypi.org/project/web-pyoctopus/)

---

## 🚀 Installation

Install Web-PyOctopus using **pip**:

```sh
pip install web-pyoctopus
```

---

## 📌 Basic Usage

Create a simple **Web-PyOctopus** app:

```python
from pyoctopus.api import OctopusAPI

app = OctopusAPI()

@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}!"
```

Run it with a WSGI server like **Gunicorn**:

```sh
gunicorn app:app
```

---

## 📚 Routing & Class-Based Views

Define class-based views for better organization:

```python
@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"
```

---

## 🎨 Template Rendering

Use templates for dynamic content:

```python
@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template(
        "index.html", context={"name": "Web-PyOctopus", "title": "Best Framework"}
    ).encode()
```

Change the default template directory:

```python
app = OctopusAPI(templates_dir="custom_templates")
```

Example `index.html`:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>{{ title }}</title>
  </head>
  <body>
    <h1>Welcome to {{ name }}</h1>
  </body>
</html>
```

---

## 📂 Static Files

By default, static files are served from the `static` directory. You can change it:

```python
app = OctopusAPI(static_dir="assets")
```

Use them in HTML:

```html
<link href="/static/styles.css" rel="stylesheet" />
```

---

## 🛠 Middleware Support

Create custom middleware by inheriting from `Middleware`:

```python
from pyoctopus.middleware import Middleware

class SimpleLoggerMiddleware(Middleware):
    def process_request(self, req):
        print("Request received:", req.url)

    def process_response(self, req, res):
        print("Response sent:", req.url)

app.add_middleware(SimpleLoggerMiddleware)
```

---

## 🧪 Unit Testing

Use **pytest** for testing. Fixtures `app` and `client` help in writing tests:

```python
def test_home_route(client):
    response = client.get("/home")
    assert response.text == "Hello from the HOME page"
```

Parameterized route testing:

```python
def test_dynamic_route(client):
    response = client.get("/hello/Alice")
    assert response.text == "Hello, Alice!"
```

---

## 📜 License

Web-PyOctopus is an open-source project for educational purposes.

---

### 🚀 Happy Coding with Web-PyOctopus! 🎉
