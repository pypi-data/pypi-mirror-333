# 🚀 PayBuildr 💸✨

A powerful Django application that integrates Stripe payments, Kong API Gateway management, and page building capabilities using GrapeJS and Puck.

## 💥 What is PayBuildr?

PayBuildr is the **all-in-one solution** for Django developers who need:
- 💳 **Payment processing** with Stripe
- 🌉 **API gateway management** with Kong
- 🎨 **Visual page building** with GrapeJS & Puck

Built for Django 5.0+ and Python 3.12+, PayBuildr is the modern way to build payment-enabled web apps! 

## ✨ Features

- 💰 **Stripe Integration**: Process payments, manage subscriptions, and handle webhooks like a boss!
- 🔌 **Kong API Management**: Configure and manage API services, routes, and rate limiting without breaking a sweat
- 🏗️ **Page Builder**: Create and customize stunning pages with GrapeJS or Puck.js without writing a single line of HTML
- 🧠 **Smart Admin Interface**: Comprehensive Django admin integration that just works™
- 🔄 **API Access**: RESTful endpoints for plans, subscriptions, and pages
- 🛠️ **Customizable**: Plug it into your project and extend it however you want!

## 📋 Requirements

- 🐍 Python 3.12+
- 🎸 Django 5.0+
- 🌐 Django REST Framework 3.14+
- 💵 Stripe Python SDK 7.0+
- 🦍 Kong API Gateway
- 📦 Node.js (for building frontend assets)

## 🚀 Installation

```bash
pip install paybuildr  # It's that simple!
```

Add to your `INSTALLED_APPS` (so easy your cat could do it):

```python
INSTALLED_APPS = [
    # ... your other cool apps
    'rest_framework',  # gotta have this!
    'paybuildr',       # 💥 BOOM!
    # ... maybe more apps here
]
```

Add to your `urls.py` (copy & paste, you got this!):

```python
urlpatterns = [
    # ... other URLs
    path('paybuildr/', include('paybuildr.urls')),  # 🎯 Plug and play!
    # ... more URLs maybe?
]
```

## ⚙️ Configuration

### 💳 Stripe Configuration

Add these settings to your `settings.py`:

```python
# 🔑 Your secret keys (don't commit these to git!)
STRIPE_SECRET_KEY = 'your-stripe-secret-key'
STRIPE_PUBLIC_KEY = 'your-stripe-publishable-key'
STRIPE_WEBHOOK_SECRET = 'your-stripe-webhook-secret'
STRIPE_SUCCESS_URL = 'https://your-site.com/success/'  # 🎉
STRIPE_CANCEL_URL = 'https://your-site.com/cancel/'    # 😢
```

### 🦍 Kong Configuration

```python
KONG_ADMIN_URL = 'http://localhost:8001'
KONG_SYNC_ENABLED = True  # Set to False if you're feeling rebellious
```

### 🗄️ Migrations

Run migrations (database tables don't create themselves... yet):

```bash
python manage.py migrate paybuildr
# ✅ Database tables created like magic!
```

## 🧩 Usage

### 🎛️ Admin Interface

The admin interface is where the magic happens:

- 📊 **Plans**: Create and manage subscription plans
- 💼 **Subscriptions**: View and manage user subscriptions
- 🔗 **API Services**: Configure Kong API services
- 🛣️ **API Routes**: Set up routes for your Kong services
- ⏱️ **API Plans**: Configure rate limiting for different plans
- 📄 **Pages**: Create and edit pages with the built-in page builders

### 🔧 Management Commands

```bash
# 🦍 Sync services to Kong
python manage.py setup_kong

# 📥 Import services from Kong to Django
python manage.py sync_from_kong

# 💰 Sync Stripe plans
python manage.py sync_stripe_plans
```

### 🔌 API Endpoints

RESTful goodness at your fingertips:

- `/api/plans/` - List available plans 📋
- `/api/plans/{id}/checkout/` - Create a checkout session 💸
- `/api/subscriptions/` - List user subscriptions 📊
- `/api/pages/` - Access pages created with the page builder 📄

### 🎨 Page Building

Build pages like you're designing in Figma:

1. 🏁 Create pages in the admin interface
2. 🖌️ Use the visual page builder to design like a pro
3. 🚀 Publish and make available via the API or direct URL

## 💻 Development

### 🎭 Frontend Assets

To build the frontend assets:

```bash
cd paybuildr/static/paybuildr/js/puck
npm install    # 📦 Get the packages
npm run build  # 🔨 Build the assets
```

### 🧪 Running Tests

```bash
python manage.py test paybuildr  # 🧠 Because testing is smart
```

## 📜 License

MIT (Go wild! Just don't blame us if something breaks 😉)

## 🤝 Contributing

We 💖 contributions! Let's build something awesome together:

1. 🍴 Fork the repository
2. 🌱 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add some amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔄 Open a Pull Request

## 📋 Development Status & Roadmap

### ✅ Completed Features
- ✅ Stripe payment integration with plans and subscriptions
- ✅ Kong API Gateway service and route management
- ✅ Rate limiting for API services based on subscription plans
- ✅ GrapeJS page builder integration
- ✅ Django admin interface customization
- ✅ RESTful API endpoints for plans and subscriptions
- ✅ Management commands for Kong synchronization
- ✅ Signal handlers for Stripe and Kong events

### 🚧 In Progress & Planned Features
- 🚧 Comprehensive test suite
- 🚧 Documentation and examples
- 🚧 Puck page builder integration
- 📝 User dashboard for managing subscriptions
- 📝 Webhook handler improvements
- 📝 Additional page templates
- 📝 Analytics integration
- 📝 Multi-tenant support
- 📝 Docker setup for development
- 📝 CI/CD pipeline
- 📝 i18n/l10n support

> 💡 Want to help? Pick one of these items and submit a PR!

## 🙏 Acknowledgements

- Kudos to the Django community
- High-fives to the Stripe and Kong teams
- Virtual hugs to all contributors!

---

<p align="center">
  Made with ❤️ by a developer, for whoever.
</p>