**FastAPI Task Manager Implementation Plan (Simplified Jira)**

---

## 📊 Overview

This is the implementation plan for building a FastAPI-based task management system (like a simplified Jira) that includes the following features:

* JWT OAuth2 Authentication
* Admin Panel with Starlette Admin
* CRUD APIs for Projects, Tasks, Users
* Real-Time WebSocket Notifications (Redis Pub/Sub based)
* Email Notifications (via Celery)
* Model-Level and Static Translations (i18n)
* Telegram Bot Integration (Aiogram)

---

## ✅ Phase 1: CRUD APIs + Business Events

**Goal:** Complete all business logic and introduce event publishing pattern

* Implement CRUD for:

  * `User` (profile only)
  * `Project` (with member invites)
  * `Task` (assign, report, update, delete)
  * `Comment`
* Design a simple `event_bus.publish(event_type, payload)` interface
* Publish events like:

  * `project_invited`
  * `task_assigned`
  * `task_commented`

---

## 🌐 Phase 2: WebSocket Real-Time Notifications

**Goal:** Deliver notifications to connected clients via WebSocket using Redis

* Create `ConnectionManager` to manage connected clients
* Add WebSocket endpoint (`/ws/notifications`)
* Implement Redis pub/sub with channels like `user:{id}`
* On published event, send Redis message to user channel
* When WebSocket client connects, subscribe them to their channel
* Decouple delivery logic via:

  * `websockets/`
  * `notifications/`
  * `events/`

---

## ⏰ Phase 3: Email Notifications via Celery

**Goal:** Send async email notifications for important events

* Setup `Celery` with `Redis` as broker
* Create `celery/tasks.py`:

  * `send_invitation_email`
  * `send_task_assignment_email`
* Trigger tasks from event consumers
* Add email config with `aiosmtplib` or provider (Mailgun, etc)

---

## 🔄 Phase 4: Event Bus Architecture

**Goal:** Decouple logic across system with event-driven design

* Create `events/bus.py`:

  * Simple `publish` and `subscribe` logic
* Define event handlers (consumers):

  * Save notification to DB
  * Send email
  * Send real-time WebSocket message
* Allow multiple consumers per event

---

## 🏒 Phase 5: Notification UX

**Goal:** Improve notification system usability

* Store notification in DB on each event
* `GET /notifications/` endpoint with pagination
* `PATCH /notifications/{id}/read` endpoint
* Auto-mark as read on WebSocket delivery (optional)

---

## 🌍 Phase 6: i18n (Internationalization)

**Goal:** Support multilingual interfaces and data

### Static Translations (UI messages)

* Use [`Babel`](https://babel.pocoo.org/) for extraction and message catalogs
* Create `/locales` folder for `.po/.mo` files
* Auto-detect language from headers or user profile
* Use `gettext_lazy` or similar in message strings

### Model-Level Translations

* Create translation tables like:

  * `ProjectTranslation (project_id, lang, name, description)`
  * `TaskTranslation (task_id, lang, summary, description)`
* Use hybrid properties to fetch current-locale version
* On create/update, store translations via separate form/input

---

## 📢 Phase 7: Telegram Bot Integration (Aiogram)

**Goal:** Allow users to interact via Telegram bot

* Use [`Aiogram`](https://github.com/aiogram/aiogram) (async, well-maintained)
* Features:

  * `/start` -> Register and verify user
  * `/mytasks` -> Show list of assigned tasks
  * `/projects` -> Show joined projects
  * Notification push (new task assigned, project invite)
* Bot subscribes to Redis channel `telegram:{user_id}`
* Event system publishes to this channel
* Deploy separately, or inside app via `asyncio.create_task`

---

## 📊 Summary Milestones

| Phase | Feature                 | Folder Structure Affected       |
| ----- | ----------------------- | ------------------------------- |
| 1     | CRUD + Events           | `services/`, `events/`          |
| 2     | WebSockets              | `websockets/`, `notifications/` |
| 3     | Email with Celery       | `celery/`, `notifications/`     |
| 4     | Event Bus Architecture  | `events/`                       |
| 5     | Notification Storage UX | `notifications/`                |
| 6     | Translations            | `locales/`, `models/`           |
| 7     | Telegram Bot            | `telegram_bot/`, `events/`      |
