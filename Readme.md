# 🏬 Event-Driven Warehouse & Store Microservices (FastAPI + Redis Streams)

This project implements an event-driven e-commerce workflow using **FastAPI**, **Redis OM**, **Redis Streams**, and background workers. It simulates a warehouse and store system where orders trigger stock updates and conditional refunds.

---

## 🚀 Overview

The system consists of three logical parts:

1. **Store Service (FastAPI)**
   - Accepts orders
   - Calculates price & fee
   - Marks orders as `pending`
   - Emits `order-completed` events via Redis Streams (async)

2. **Warehouse Consumer**
   - Listens for `order-completed` events
   - Decrements inventory stock
   - If stock is insufficient → emits `refund-initiated` event

3. **Refund Consumer**
   - Listens for `refund-initiated` events
   - Updates order status to `refunded` in Redis

A **React frontend** is used to browse products and place orders.

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Backend Framework | FastAPI |
| Event System | Redis Streams |
| Data Models | Redis OM |
| Background Jobs | Redis + Sleep |
| Frontend | React |
| Language | Python & JavaScript |

---

## 📦 Data Models

### Product (Redis OM)
- name
- price
- quantity

### Order (Redis OM)
- product_id
- price
- fee
- total
- quantity
- status: pending → completed → refunded

---

## 🔁 Event Streams

| Stream | Producer | Consumer | Purpose |
|---|---|---|---|
| `order-completed` | Store Service | Warehouse | Apply inventory changes |
| `refund-initiated` | Warehouse | Refund Worker | Mark order as refunded |

Redis Consumer Groups ensure ordered processing and retry support.

---

## 🧩 API Endpoints

### 🏬 Store Service

| Method | Endpoint | Description |
|---|---|---|
| POST | `/orders` | Create order & trigger async stream |
| GET | `/orders` | Get all orders |
| GET | `/orders/{id}` | Get order by ID |

### 📦 Warehouse Service

| Method | Endpoint | Description |
|---|---|---|
| POST | `/product` | Create product |
| GET | `/product/{pk}` | Get product |
| GET | `/products` | List products |
| DELETE | `/product/{pk}` | Delete product |

---

## ▶️ How It Works

1. Client sends `POST /orders`
2. Store calculates fees and saves an `Order(status=pending)`
3. Store triggers async worker `complete_order`
4. Worker updates order to `completed` and pushes event to Redis Stream
5. Warehouse worker consumes event and:
   - Updates stock if available
   - Otherwise pushes `refund-initiated` event
6. Refund worker marks order as `refunded`

---

## ▶️ Running Locally

### 1️⃣ Start Redis

Use Redis Cloud or local Redis with Streams enabled.

### 2️⃣ Run Store Service

```
uvicorn main:app --reload
```

### 3️⃣ Run Warehouse Consumer

```
python warehouse_consumer.py
```

### 4️⃣ Run Refund Consumer

```
python refund_consumer.py
```

### 5️⃣ (Optional) React Frontend

```
npm install
npm start
```

---

## 🧠 Learning Outcomes

This project demonstrates:

- Event-driven microservice communication
- Redis Streams & Consumer Groups
- Redis OM data modeling
- Asynchronous order fulfillment workflows
- Compensation logic via refunds
- Backend-to-frontend integration

---

## 📜 License

MIT — free to learn and modify.
