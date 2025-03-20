import json
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

User = get_user_model()


class Plan(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    stripe_price_id = models.CharField(_("Stripe Price ID"), max_length=100, unique=True)
    amount = models.DecimalField(
        _("Amount"), 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    currency = models.CharField(_("Currency"), max_length=3, default="USD")
    interval = models.CharField(
        _("Interval"),
        max_length=20,
        choices=[
            ("month", _("Monthly")),
            ("year", _("Yearly")),
            ("once", _("One-time")),
        ],
    )
    active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")
        indexes = [
            models.Index(fields=["active"]),
            models.Index(fields=["interval"]),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_interval_display()} - {self.amount} {self.currency})"


class Subscription(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="subscriptions",
        verbose_name=_("User")
    )
    plan = models.ForeignKey(
        Plan, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=_("Plan")
    )
    stripe_subscription_id = models.CharField(
        _("Stripe Subscription ID"), 
        max_length=100, 
        blank=True, 
        null=True
    )
    status = models.CharField(_("Status"), max_length=20)
    current_period_end = models.DateTimeField(_("Current Period End"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["current_period_end"]),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.plan}"


class ApiService(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    url = models.URLField(_("URL"))
    kong_id = models.CharField(_("Kong ID"), max_length=100, blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("API Service")
        verbose_name_plural = _("API Services")
        indexes = [
            models.Index(fields=["active"]),
        ]
    
    def __str__(self):
        return self.name


class ApiRoute(models.Model):
    service = models.ForeignKey(
        ApiService, 
        on_delete=models.CASCADE, 
        related_name="routes",
        verbose_name=_("Service")
    )
    path = models.CharField(_("Path"), max_length=200)
    name = models.CharField(_("Name"), max_length=100)
    kong_id = models.CharField(_("Kong ID"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("API Route")
        verbose_name_plural = _("API Routes")
        constraints = [
            models.UniqueConstraint(
                fields=["service", "path"],
                name="unique_service_path"
            )
        ]
    
    def __str__(self):
        return f"{self.name} ({self.path})"


class ApiPlan(models.Model):
    plan = models.ForeignKey(
        Plan, 
        on_delete=models.CASCADE,
        verbose_name=_("Plan")
    )
    service = models.ForeignKey(
        ApiService, 
        on_delete=models.CASCADE,
        verbose_name=_("Service")
    )
    rate_limit = models.IntegerField(
        _("Rate Limit"), 
        help_text=_("Requests per minute"),
        validators=[MinValueValidator(1)]
    )
    kong_plugin_id = models.CharField(_("Kong Plugin ID"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("API Plan")
        verbose_name_plural = _("API Plans")
        constraints = [
            models.UniqueConstraint(
                fields=["plan", "service"],
                name="unique_plan_service"
            )
        ]
    
    def __str__(self):
        return f"{self.plan.name} - {self.service.name}"


class PuckPage(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True)
    content = models.JSONField(_("Content"), default=dict)  # Use default=dict
    published = models.BooleanField(_("Published"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        indexes = [
            models.Index(fields=["published"]),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Ensure content is a dictionary/JSON object
        if self.content is None:
            self.content = {"html": "", "css": ""}
        elif isinstance(self.content, str):
            try:
                self.content = json.loads(self.content)
            except json.JSONDecodeError:
                self.content = {"html": "", "css": ""}
        
        # Ensure content has the expected structure
        if not isinstance(self.content, dict):
            self.content = {"html": "", "css": ""}
        
        super().save(*args, **kwargs)